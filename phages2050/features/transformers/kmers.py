from typing import Set, Union, List

import numpy as np
import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin
from pandas.core.series import Series

from gensim.models.word2vec import Word2Vec
from gensim.models.fasttext import FastText

from pandarallel import pandarallel


# Parallelization has a cost, so parallelization is efficient only
# if the amount of calculation to parallelize is high enough.
# For very little amount of data, using parallelization is not always worth it.
pandarallel.initialize()


class KMersTransformer(BaseEstimator, TransformerMixin):
    """
    K-mer transformer is responsible to extract set of
    words which are subsequences of length (6 by default)
    contained within a biological sequence

    Each of the word is called k-mer and are composed of
    nucleotides (i.e. A, T, G, and C)

    Example:
        fname = 'NC_001604.fasta'
        fr = FastaReader(fname)

        sample = fr.to_df()

        kmt = KMersTransformer()
        kmt.transform(sample)
    """

    def __init__(self, size: int = 6):
        self.accepted_chars: Set[str] = {"A", "C", "T", "G"}
        self.size: int = size

    def _extract_kmers_from_sequence(self, sequence: str) -> str:
        """
        K-mer transformer with sliding window method,
        where each k-mer has size of 6 (by default)

        A sliding window is used to scan the entire sequence,
        if the k-mer contains unsupported character then the
        whole k-mer is ignored (not included in final string)

        Method return a string with k-mers separated by space
        what is expected as input for embedding
        """

        return " ".join(
            [
                sequence[x : x + self.size]
                for x in range(len(sequence) - self.size + 1)
                if not set(sequence[x : x + self.size]) - self.accepted_chars
            ]
        )

    def transform(self, df: pd.DataFrame) -> Series:
        """
        Execute k-mer transformer on each DNA sequence
        and return it as Series with k-mers strings
        """

        # sequence column is expected
        assert list(df.columns) == ["sequence"]

        return df.sequence.parallel_apply(self._extract_kmers_from_sequence)


class GenomeAvgTransformer(TransformerMixin, BaseEstimator):
    """
    Average k-mers to represent Bacteriophage with word embedding

    Most Word2vec or fastText pre-trained models allow to get
    numerical representations of individual words but not of entire documents
    With this class it can average each k-mer of a DNA so that the
    generated Bacteriophage vector is actually a centroid of all k-mers in feature space
    """

    def __init__(self, gensim_model: Union[FastText, Word2Vec]):
        """
        It support Word2Vec as well as fastText embedding model
        """

        self.gensim_model: Union[FastText, Word2Vec] = gensim_model
        self.columns = [
            f"feature_{index}" for index in range(self.gensim_model.vector_size)
        ]

    def average_word_vectors(self, words: List[str], vocabulary: Set) -> np.array:
        """
        Return fixed-length numeric vector for each DNA sequence
        """

        # Filter only words supported by the vocabulary
        supported_words: list = [word for word in words if word in vocabulary]

        if supported_words:
            # Return average fixed-length numeric vector
            # including all the k-mers in the sequence
            feature_vector: np.array = np.mean(
                self.gensim_model[supported_words], axis=0, dtype="float64"
            )
        else:
            # Return fixed-length numeric vector with zeros
            # if the k-mers (words) weren't in the vocabulary
            feature_vector: np.array = np.zeros(
                (self.gensim_model.vector_size,), dtype="float64"
            )

        return feature_vector

    def averaged_word_vectorizer(self, column_with_kmers_seqs) -> np.array:
        """
        Execute DNA averaged vector transformer on each k-mer sequence
        and return as array of numeric values
        """

        # Unique set of words
        vocabulary: set = set(self.gensim_model.wv.index2word)

        features: list = [
            self.average_word_vectors(
                # Split k-mer sequence with spaces into a list with k-mers (words)
                words=sentence.split(),
                vocabulary=vocabulary,
            )
            for sentence in column_with_kmers_seqs
        ]

        return np.array(features)

    def transform(self, column_with_kmers_seqs: Series) -> pd.DataFrame:
        """
        Execute DNA averaged vector transformer on each k-mer sequence
        and return it Pandas DataFrame with fixed-length numeric vector space
        """

        return pd.DataFrame(
            data=self.averaged_word_vectorizer(column_with_kmers_seqs),
            columns=self.columns,
        )
