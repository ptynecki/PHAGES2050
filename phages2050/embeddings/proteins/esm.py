import os
from typing import List, Dict

import pandas as pd

import torch

import esm
from esm import FastaBatchedDataset


class ESMEmbedding:
    """
    Embedding class is responsible to load pre-trained transformer model for proteins
    and execute vectorization on single protein or set of proteins which represent
    single bacteriophage

    In the case of set of proteins the vectorization returns averaged numeric vector
    """

    CPU = "cpu"
    FEATURE_SPACE = 1280
    UNIREF50 = "Uniref50"
    UNIREF100 = "Uniref100"

    def __init__(
        self,
        uniref: str = UNIREF50,
        toks_per_batch: int = 4096,
        extra_toks_per_seq: int = 1,
        repr_layers: int = 34,
        cuda_device: int = None,
    ):
        self.uniref = uniref
        self.toks_per_batch = toks_per_batch
        self.extra_toks_per_seq = extra_toks_per_seq
        self.repr_layers = repr_layers

        # Select GPU card (if you have more than one)
        if cuda_device is not None and torch.cuda.is_available():
            available_devices = self._get_cuda_devices()
            if available_devices.get(cuda_device, None):
                cuda_device = f"cuda:{cuda_device}"
            else:
                cuda_device = self.CPU
        else:
            cuda_device = self.CPU
        self.device = torch.device(cuda_device)

        # Load ESM model once
        self._load_model()

    @staticmethod
    def _get_cuda_devices() -> Dict:
        """
        Return dict with cuda devices (id: name) if exists
        """

        gpu_device_count = torch.cuda.device_count()

        return {
            gpu_id: torch.cuda.get_device_name(gpu_id)
            for gpu_id in range(gpu_device_count)
        }

    def _load_model(self) -> None:
        """
        Download and load selected ESM model (Uniref50 Sparse or Uniref100)

        This procedure should be executed once and the result
        loaded by ESMEmbedding class instance
        """

        if self.uniref == self.UNIREF50:
            # 34 layer transformer model with 670M params, trained on Uniref50 Sparse.
            self.model, self.alphabet = esm.pretrained.esm1_t34_670M_UR50S()
        elif self.uniref == self.UNIREF100:
            # 34 layer transformer model with 670M params, trained on Uniref100.
            self.model, self.alphabet = esm.pretrained.esm1_t34_670M_UR100()
        else:
            raise NotImplemented("Invalid uniref argument value")

        self.model.cuda(device=self.device)

        self.layers = [
            (i + self.model.num_layers + 1) % (self.model.num_layers + 1)
            for i in [self.repr_layers]
        ]

    def _get_data(self, fasta_path):
        """
        Load and process proteins sequences from the FASTA or multi-Fasta file

        Each of the sample label have to be unique, in other case assertion exception is raised
        """

        dataset = FastaBatchedDataset.from_file(fasta_path)
        batch_converter = self.alphabet.get_batch_converter()
        batches = dataset.get_batch_indices(
            self.toks_per_batch, self.extra_toks_per_seq
        )

        return torch.utils.data.DataLoader(
            dataset, collate_fn=batch_converter, batch_sampler=batches
        )

    def _set_column_names(self) -> None:
        """
        Set a list with embedding column names
        """

        self.columns = [f"ESM_{index}" for index in range(self.FEATURE_SPACE)]

    def _get_vectors(self, batched_data, bacteriophage_level: bool = False) -> List:
        """
        Return the embedding result represented by lists or averaged list with 1280 digits
        """

        protein_tensors = []

        with torch.no_grad():
            for batch_idx, (labels, strs, toks) in enumerate(batched_data):
                toks = toks.to(device=self.device, non_blocking=True)

                out = self.model(toks, repr_layers=self.layers)

                representations = {
                    layer: t.to(device=self.device)
                    for layer, t in out["representations"].items()
                }

                for i, label in enumerate(labels):
                    result = {
                        "label": label,
                        "mean_representations": {
                            layer: t[i, 1: len(strs[i]) + 1].mean(0)
                            for layer, t in representations.items()
                        },
                    }

                    protein_tensors.append(result)

        mean_representations = [
            tensor["mean_representations"][self.repr_layers]
            for tensor in protein_tensors
        ]
        vectors = torch.stack(mean_representations, dim=0)

        # Organism level
        if bacteriophage_level:
            vectors = vectors.mean(dim=0).reshape(1, -1)

        return vectors.cpu().numpy()

    def transform(
        self, fasta_path: str, bacteriophage_level: bool = False
    ) -> pd.DataFrame:
        """
        Execute transformer embedding directly based on FASTA input file

        The first case is expected for single protein vectorization
        The second case is expected for set of proteins which represent
        single bacteriophage
        """

        fname, ext = os.path.splitext(os.path.basename(fasta_path))

        batched_data = self._get_data(fasta_path)
        data = self._get_vectors(batched_data, bacteriophage_level)
        self._set_column_names()

        result_df = pd.DataFrame(data, columns=self.columns)

        if bacteriophage_level:
            result_df.insert(0, "name", [fname])
        else:
            proteins_count = result_df.shape[0]
            result_df.insert(
                0, "name", [f"protein_{index}" for index in range(proteins_count)]
            )

        return result_df
