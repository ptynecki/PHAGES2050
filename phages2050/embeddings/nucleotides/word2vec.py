import os
import base64
from io import BytesIO
from zipfile import ZipFile
from typing import Dict
from pathlib import Path

import requests

from gensim.models.word2vec import Word2Vec

from fake_useragent import UserAgent


class Word2VecModelManager:
    """
    Manager class is responsible to download and unzip
    Word2Vec pre-trained model for nucleotides embedding
    """

    WORD2VEC_URL = base64.b64decode(
        "aHR0cHM6Ly9kZWVwcGV0cmkuYWkvc3RhdGljL3BoYWdlczIwNTAv"
        "d29yZDJ2ZWMtZW1iZWRkaW5nLTIxLjA3LjIwMjAuemlw"
    )
    STATUS_CODE_200 = 200

    def __init__(self, model_dir: str = "word2vec_model"):
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
        Download Word2Vec pre-trained model and unzip it into directory

        This procedure should be executed once and the result
        loaded by Word2VecEmbedding class instance
        """

        path = Path(self.model_dir)
        # If model directory exists then return it immediately
        if os.path.exists(path) and os.listdir(path):
            print("[DEBUG] Word2Vec model exists")
            return path
        else:
            print("[DEBUG] Word2Vec model is downloading now")

        headers = self._get_headers()

        with requests.get(self.WORD2VEC_URL, headers=headers) as response:
            assert response.status_code == self.STATUS_CODE_200

            with ZipFile(BytesIO(response.content)) as zip_file:
                zip_file.extractall(self.model_dir)

        return path


class Word2VecEmbedding:
    """
    Word2Vec instance loader class
    """

    def __init__(self, model_pkl_file: str):
        """
        Pickle file need to be serialized by Word2Vec.save method
        before it will be loader with this class
        """

        self.model_pkl_file = model_pkl_file
        if not os.path.exists(self.model_pkl_file):
            raise Exception("Word2Vec model wasn't downloaded yet")

        self.model = Word2Vec.load(self.model_pkl_file)
        self.feature_space = self.model.vector_size

    def get_train_params(self) -> Exception:
        """
        TODO: return dict with model train parameters
        """
        raise NotImplemented
