from typing import Mapping, Union, List, Iterator

from Bio.SeqRecord import SeqRecord
from Bio.SeqUtils.ProtParam import ProteinAnalysis
from Bio.SeqIO.FastaIO import FastaIterator

import pandas as pd


class ProteinFeatureExtractor:
    """
    Feature extraction from protein sequence for
    Machine Learning classification or deeper analysis

    Example usage:

        from features.extractors.proteins import ProteinFeatureExtractor

        pfe = ProteinFeatureExtractor(protein_sequence='MAKINELLRESTTTNSNSIGRPNLVALTRATTKLIYSDIVATQRTNQPVAA')
        pfe.get_features()
    """

    FEATURE_NAMES = [
        "protein_length",
        "gravy",
        "molecular_weight",
        "aromaticity",
        "instability_index",
        "isoelectric_point",
        "flexibility",
        "mec_cysteines",
        "mec_cystines",
        "ssf_helix",
        "ssf_turn",
        "ssf_sheet",
    ]

    def __init__(self, protein_sequence: str):
        self.protein_sequence = self._normalize(protein_sequence)

        self.protein_analysis = ProteinAnalysis(self.protein_sequence)

    @staticmethod
    def _normalize(source: Union[str, SeqRecord]) -> str:
        """
        Normalize each protein sequence
        to uppercase and without blank chars
        """

        # If source is a string
        if isinstance(source, str):
            entry = source
        # If source is a BioPython object with seq field
        else:
            entry = source.seq

        return str(entry).upper().strip()

    def _get_protein_length(self) -> int:
        """
        Protein length
        """

        return len(self.protein_sequence)

    def _calculate_gravy(self) -> float:
        """
        GRAVY (Grand Average of Hydropathy) index score
        is calculated by adding the hydropathy value for
        each residue and then dividing by the length of
        the protein sequence

        Negative GRAVY value indicates that the protein
        is non-polar and Positive value indicates that
        the protein is polar
        """

        return self.protein_analysis.gravy()

    def _calculate_molecular_weight(self) -> float:
        """
        Molecular Weight is calculated as the sum
        of atomic masses of all atoms in the molecul
        """

        return self.protein_analysis.molecular_weight()

    def _calculate_aromaticity(self) -> float:
        """
        Aromaticity is used to describe a planar, cyclic
        molecule with a ring of resonance bonds which is
        more stable when compared to other connective or
        geometric arrangements consisting of the same set
        of atoms
        """

        return self.protein_analysis.aromaticity()

    def _calculate_instability_index(self) -> float:
        """
        Instability index gives an estimate of the stability
        of the protein in a test tube

        Any value above 40 means that the protein is unstable
        (has a short half life)
        """

        return self.protein_analysis.instability_index()

    def _calculate_isoelectric_point(self) -> float:
        """
        Isoelectric point (pI) is the pH at which net charge of
        the protein is zero. Isoelectric point is widely useful
        for choosing a buffer system for purification and
        crystallisation of a given protein
        """

        return self.protein_analysis.isoelectric_point()

    def _calculate_flexibility(self) -> float:
        """
        Flexibility is of overwhelming importance for protein function,
        because of the changes in protein structure during interactions
        with binding partners
        """

        return sum(self.protein_analysis.flexibility())

    def _calculate_molar_extinction_coefficient(self) -> Mapping[str, float]:
        """
        Molar extinction coefficient of a protein sequence can be calculated
        from the molar extension coefficient of amino acids which are
        Cystine, Tyrosine and Tryptophan
        """

        cysteines, cystines = self.protein_analysis.molar_extinction_coefficient()

        residues = {self.FEATURE_NAMES[7]: cysteines, self.FEATURE_NAMES[8]: cystines}

        return residues

    def _calculate_secondary_structure_fraction(self) -> Mapping[str, float]:
        """
        This function returns a list of the fraction of amino acids which
        tend to be in Helix, Turn or Sheet

        Amino acids present in Turn are:
        Asparagine (N), Proline (P), Glycine (G), Serine (S)

        Amino acids present in Sheets are:
        Glutamic acid (E), Methionine (M), Alanine (A), Leucine (L)
        """

        helix, turn, sheet = self.protein_analysis.secondary_structure_fraction()

        fractions = {
            self.FEATURE_NAMES[9]: helix,
            self.FEATURE_NAMES[10]: turn,
            self.FEATURE_NAMES[11]: sheet,
        }

        return fractions

    def get_features(self) -> Mapping[str, Union[int, float, None]]:
        """
        Return full feature space for single protein as Python dict
        """

        features = {
            self.FEATURE_NAMES[0]: self._get_protein_length(),
            self.FEATURE_NAMES[1]: self._calculate_gravy(),
            self.FEATURE_NAMES[2]: self._calculate_molecular_weight(),
            self.FEATURE_NAMES[3]: self._calculate_aromaticity(),
            self.FEATURE_NAMES[4]: self._calculate_instability_index(),
            self.FEATURE_NAMES[5]: self._calculate_isoelectric_point(),
            self.FEATURE_NAMES[6]: self._calculate_flexibility(),
        }

        features.update(self._calculate_molar_extinction_coefficient())

        features.update(self._calculate_secondary_structure_fraction())

        return features


class MultifastaProteinFeatureExtractor:
    """
    Feature extraction from proteins sequences from multifasta file

    This class allows you to create DataFrame or save it as CSV

    Example usage:

        from features.extractors.proteins import MultifastaProteinFeatureExtractor

        mpfe = MultifastaProteinFeatureExtractor(protein_sequence='multifasta-example.fasta')
        mpfe.to_df()
        mpfe.to_csv()
    """

    def __init__(self, fasta_path: str):
        self.fasta_path = fasta_path

        self.entries = self._get_entires()

    @staticmethod
    def _fasta_reader(filename: str) -> Iterator:
        """
        Read FASTA file content including multifasta format
        """

        with open(filename) as handle:
            for record in FastaIterator(handle):
                yield record

    def _get_entires(self) -> List:
        """
        Extract each entry (protein) from the multifasta
        """

        entries = list(self._fasta_reader(self.fasta_path))

        return entries

    def to_df(self) -> pd.DataFrame:
        """
        Return extracted features from each proteins as DataFrame
        """

        data = []

        for protein_sequence in self.entries:
            protein_features = ProteinFeatureExtractor(
                protein_sequence=protein_sequence
            ).get_features()

            data.append(protein_features)

        df = pd.DataFrame(data=data, columns=ProteinFeatureExtractor.FEATURE_NAMES)

        return df

    def to_csv(self, csv_fname: str) -> None:
        """
        Return DataFrame as CSV file
        (filename format: <csv_fname>.csv)
        """

        df = self.to_df()
        df.to_csv(csv_fname, index=False)
