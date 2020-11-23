from datetime import date
from typing import List

from Bio import Entrez
from Bio import SeqIO

import pandas as pd


class NCBIProteinExtractor:
    """
    NCBI protein sequences and meta-data extractor

    This class allows you to create DataFrame or save it as CSV with columns:
    - Sample accession and Proteins ID
    - Notes and Products (proteins name)
    - Starts, ends and strands
    - Protein sequences and sequences length

    Example usage:

        from phages2050.crawlers.ncbi.proteins import NCBIProteinExtractor

        protein_data = NCBIProteinExtractor(
            accession_number='NC_001609'
        )
        protein_data.to_df()
        protein_data.to_csv()
    """

    COLUMNS = [
        "acc_no",
        "protein_id",
        "note",
        "product",
        "start",
        "end",
        "strand",
        "sequence",
        "sequence_length",
    ]

    def __init__(self, accession_number: str):
        self.df = pd.DataFrame()
        today = date.today()

        self.accession_number = accession_number

        self._init_ncbi_handler()

        self.csv_name = f"ncbi_proteins_{today}.csv"

    def _init_ncbi_handler(self) -> None:
        """
        NCBI handle setup
        """

        Entrez.email = ""

        self.handle = Entrez.efetch(
            db="nucleotide", id=self.accession_number, rettype="gb", retmode="text"
        )

    def _extract_protein_data(self) -> List[list]:
        """
        Extract protein sequences and meta-data
        directly from the NCBI related with the sample
        """

        records = SeqIO.parse(self.handle, "genbank")

        proteins_data = []

        for record in records:
            for feature in record.features:
                # Extract only coding sequences
                if feature.type == "CDS":
                    # Sample accession number
                    acc_no = record.name

                    protein_sequence = feature.qualifiers.get("translation", "")

                    if protein_sequence:
                        # Protein sequence
                        protein_sequence = protein_sequence[0]
                        protein_sequence_length = len(protein_sequence)

                        # Protein ID
                        protein_id = feature.qualifiers.get("protein_id", "")
                        if protein_id:
                            protein_id = protein_id[0]

                        # Protein note
                        note = feature.qualifiers.get("note", "")
                        if note:
                            note = note[0]

                        # Protein product (name)
                        product = feature.qualifiers.get("product", "")
                        if product:
                            product = product[0]

                        # Start genome position
                        start = feature.location.start.position
                        # End genome position
                        end = feature.location.end.position
                        # Strand genome
                        strand = feature.location.strand

                        proteins_data.append(
                            [
                                acc_no,
                                protein_id,
                                note,
                                product,
                                start,
                                end,
                                strand,
                                protein_sequence,
                                protein_sequence_length,
                            ]
                        )

        return proteins_data

    def to_df(self) -> pd.DataFrame:
        """
        Return data as DataFrame
        """

        protein_data = self._extract_protein_data()

        self.df = pd.DataFrame(protein_data, columns=self.COLUMNS)

        return self.df

    def to_csv(self) -> None:
        """
        Return DataFrame as CSV file
        (filename format: ncbi_proteins_<YYYY:MM:DD>.csv)
        """

        self.to_df()

        self.df.to_csv(self.csv_name, index=False)
