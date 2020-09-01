import os

import pandas as pd

from Bio.SeqIO.FastaIO import FastaIterator
from Bio.SeqRecord import SeqRecord


class FastaReader:
    """
    Universal class for reading FASTA files with genome or protein
    sequence or multi-FASTA with chunks of sequences

    Example:

        fname = 'NC_001604.fasta'
        fr = FastaReader(fname)

        kmers_sequence = fr.get_sequence()

        ks_df = fr.to_df()
    """

    def __init__(self, fasta_file_path: str):
        self.fasta_file_path = fasta_file_path
        self.fasta_name = os.path.basename(self.fasta_file_path)

    @staticmethod
    def _fasta_reader(filename: str) -> SeqRecord:
        """
        FASTA file reader as iterator
        """

        with open(filename) as handle:
            for record in FastaIterator(handle):
                yield record

    @staticmethod
    def _normalize(entry: SeqRecord) -> str:
        """
        Each of the sequence is normalized into uppercase
        format without blank chars at the end
        """

        return str(entry.seq).upper().strip()

    def get_sequence(self) -> str:
        """
        Final genome or protein sequence string after normalization
        """

        sequence: str = ""

        for entry in self._fasta_reader(self.fasta_file_path):
            sequence += f"{self._normalize(entry)} "

        return sequence.strip()

    def to_df(self) -> pd.DataFrame:
        """
        Return pandas DataFrame with k-mers sequence
        format what is expected by KMersTransformer
        """

        return pd.DataFrame(data=[self.get_sequence()], columns=["sequence"])
