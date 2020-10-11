import os
import base64
from io import BytesIO
from zipfile import ZipFile
from typing import List, Dict
from pathlib import Path

import pandas as pd
import requests

from fake_useragent import UserAgent

from bio_embeddings.embed.prottrans_bert_bfd_embedder import ProtTransBertBFDEmbedder

import torch


class BertModelManager:
    """
    Manager class is responsible to download and unzip
    BERT pre-trained model for protein embedding
    """

    BERT_URL = base64.b64decode(
        "aHR0cDovL21haW50ZW5hbmNlLmRhbGxhZ28udXMvcHVibGljL2Vt"
        "YmVkZGluZ3MvZW1iZWRkaW5nX21vZGVscy9iZXJ0L2JlcnQuemlw"
    )
    STATUS_CODE_200 = 200

    def __init__(self, model_dir: str = "bert_model"):
        self.model_dir = model_dir

        if not os.path.exists(model_dir):
            os.mkdir(self.model_dir)

    @staticmethod
    def _get_headers() -> Dict:
        """
        Return header dict with random User-Agent to support request
        and to avoid being blocked by the server
        """

        ua = UserAgent()
        ua.update()

        return {"User-Agent": ua.random}

    def download_model(self) -> Path:
        """
        Download BERT pre-trained model and unzip it into directory

        This procedure should be executed once and the result
        loaded by BertEmbedding class instance
        """

        path = Path(self.model_dir) / "bert"
        # If model directory exists then return it immediately
        if os.path.exists(path):
            print("[DEBUG] BERT model exists")
            return path
        else:
            print("[DEBUG] BERT model is downloading now")

        headers = self._get_headers()

        with requests.get(self.BERT_URL, headers=headers) as response:
            assert response.status_code == self.STATUS_CODE_200

            with ZipFile(BytesIO(response.content)) as zip_file:
                zip_file.extractall(self.model_dir)

        return path


class BertEmbedding:
    """
    Embedding class is responsible to load BERT pre-trained model for proteins
    and execute vectorization on single protein or set of proteins which represent
    single bacteriophage

    In the case of set of proteins the vectorization returns averaged numeric vector
    """

    CPU = "cpu"
    FEATURE_SPACE = 1024
    SUPPORTED_COLUMNS = ["sequence", "class"]
    SUPPORTED_COLUMNS_AVG = ["sequence", "name"]

    def __init__(self, model_dir: str, cuda_device: int = None):
        """
        If you have an access to GPU with CUDA support the embedding will compute it
        on your graphic card If not then CPU and RAM will be consumed
        """

        self.model_dir = model_dir
        if not os.path.exists(self.model_dir):
            raise Exception("BERT model wasn't downloaded yet")

        self.embedder = ProtTransBertBFDEmbedder(model_directory=self.model_dir)

        self.cuda_device = cuda_device
        # Select GPU card (if you have more than one)
        if self.cuda_device and torch.cuda.is_available():
            self.device = f"cuda:{self.cuda_device}"
        else:
            self.device = self.CPU

    def _set_column_names(self) -> None:
        """
        Set a list with embedding column names
        """

        self.columns = [f"BERT_{index}" for index in range(self.FEATURE_SPACE)]

    def _get_vectors(self, df: pd.DataFrame, bacteriophage_level: bool = False) -> List:
        """
        Return the embedding result represented by lists or averaged list with 1024 digits
        """

        with torch.no_grad():
            vectors = []

            for protein in df.itertuples():
                embedding = self.embedder.embed(protein.sequence)
                protein_vector = self.embedder.reduce_per_protein(embedding)
                vectors.append(protein_vector)

            if bacteriophage_level:
                print("[DEBUG] Protein vectors are averaging to form a bacteriophage")

                vectors = [
                    torch.tensor(vectors, device=self.device).mean(dim=0).tolist()
                ]

        return vectors

    def transform(
        self, df: pd.DataFrame, bacteriophage_level: bool = False
    ) -> pd.DataFrame:
        """
        Execute BERT embedding on DataFrame with two supported type of columns:
        - "sequence" and "class"
        - "sequence" and "name"

        The first case is expected for single protein vectorization
        The second case is expected for set of proteins which represent
        single bacteriophage
        """

        if bacteriophage_level:
            # "sequence" and "name" columns are expected
            assert self.SUPPORTED_COLUMNS_AVG == list(
                df[self.SUPPORTED_COLUMNS_AVG].columns
            )
        else:
            # "sequence" and "class" columns are expected
            assert self.SUPPORTED_COLUMNS == list(df[self.SUPPORTED_COLUMNS].columns)

        data = self._get_vectors(df, bacteriophage_level)
        self._set_column_names()

        result_df = pd.DataFrame(data=data, columns=self.columns)

        if bacteriophage_level:
            # Set first value as "name" column value
            result_df[self.SUPPORTED_COLUMNS_AVG[1]] = df[
                self.SUPPORTED_COLUMNS_AVG[1]
            ].values[0]
        else:
            # Set each "class" column value
            result_df[self.SUPPORTED_COLUMNS[1]] = df[self.SUPPORTED_COLUMNS[1]].values

        return result_df
