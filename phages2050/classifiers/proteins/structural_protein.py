import os
import base64
import joblib
from pathlib import Path
from io import BytesIO
from zipfile import ZipFile
from typing import Dict

import pandas as pd
import requests

from fake_useragent import UserAgent


class BacteriophageStructuralProteinManager:
    """
    Manager class is responsible to download and unzip
    pre-trained model and label encoder for Bacteriophage
    Structural Protein classification
    """

    BSP_MODEL_URL = base64.b64decode(
        "aHR0cHM6Ly9kZWVwcGV0cmkuYWkvc3RhdGljL3BoYW"
        "dlczIwNTAvYnNwX21vZGVsXzIxLjA4LjIwMjAuemlw"
    )
    BSP_LABELS_URL = base64.b64decode(
        "aHR0cHM6Ly9kZWVwcGV0cmkuYWkvc3RhdGljL3BoYWdlczIw"
        "NTAvYnNwX2xhYmVsX2VuY29kZXJfMjEuMDguMjAyMC56aXA="
    )
    STATUS_CODE_200 = 200

    def __init__(self, root_dir: str = "bsp_model"):
        self.root_dir = root_dir
        self.model_dir = Path(self.root_dir) / "model"
        self.label_encoder_dir = Path(self.root_dir) / "label_encoder"

        if not os.path.exists(self.root_dir):
            os.makedirs(self.model_dir)
            os.makedirs(self.label_encoder_dir)

    @staticmethod
    def _get_path(dir_path: str):
        """
        Return Path with unzipped file
        """

        files = os.listdir(dir_path)
        if files and len(files) == 1:
            file_path = Path(dir_path) / files[0]

            return file_path
        else:
            raise Exception("BSP model wasn't in the archive")

    @staticmethod
    def _get_headers() -> Dict:
        """
        Return header dict with random User-Agent to support request
        and to avoid being blocked by the server
        """

        ua = UserAgent()
        ua.update()

        return {"User-Agent": ua.random}

    def download_model(self):
        """
        Download pre-trained model and label encoder and unzip them into directories

        This procedure should be executed once and the result
        loaded by BacteriophageStructuralProteinClassifier class instance
        """

        headers = self._get_headers()

        # Download classifier model
        with requests.get(self.BSP_MODEL_URL, headers=headers, timeout=10) as response:
            assert response.status_code == self.STATUS_CODE_200

            with ZipFile(BytesIO(response.content)) as zip_file:
                zip_file.extractall(self.model_dir)

        model_path = self._get_path(self.model_dir)

        # Download labels encoder
        with requests.get(self.BSP_LABELS_URL, headers=headers, timeout=10) as response:
            assert response.status_code == self.STATUS_CODE_200

            with ZipFile(BytesIO(response.content)) as zip_file:
                zip_file.extractall(self.label_encoder_dir)

        label_encoder_path = self._get_path(self.label_encoder_dir)

        return {
            "model_path": model_path,
            "label_encoder_path": label_encoder_path,
        }


class BacteriophageStructuralProteinClassifier:
    """
    Classifier is responsible to load and execute pre-trained model and label encoder
    for phage structural protein prediction. This model support 11 proteins classes:
    - HTJ
    - basplate
    - collar
    - major_capsid
    - major_tail
    - minor_capsid
    - minor_tail
    - other
    - portal
    - tail_fiber
    - tail_shaft

    The model accuracy is 96.92% on training and 95.64% on validation sets after
    10-fold cross-validation. Model was trained with 11 000 samples.
    """

    SUPPORTED_COLUMNS = ["predicted_index", "predicted_class", "accuracy"]
    FEATURE_SPACE = 1024

    def __init__(self, model_path: str, label_encoder_path: str):
        """
        Check if model and label encoder directory exists
        if yes, then load the model into memory

        This method should be executed once
        """

        self.model_dir = model_path
        if not os.path.exists(self.model_dir):
            raise Exception("BSP model wasn't downloaded yet")

        self.le_dir = label_encoder_path
        if not os.path.exists(self.le_dir):
            raise Exception("BSP labels wasn't downloaded yet")

        self._load_classifier()

    def _load_classifier(self) -> None:
        """
        Load Machine Learning pre-trained model with label encoder
        """

        self.classifier = joblib.load(self.model_dir)
        self.le = joblib.load(self.le_dir)

    def predict(self, protein_vector: pd.DataFrame) -> pd.DataFrame:
        """
        Execute classification model and return best prediction
        as DataFrame with three columns:
        - "predicted_index" - predicted protein class index
        - "predicted_class" - predicted protein class name
        - "accuracy" - accuracy of prediction (0-100%)

        This method can be executed many times for different
        protein vectors

        protein_vector is represented by DataFrame with 1024
        numeric values as a result of BERT embedding
        """

        assert protein_vector.shape == self.FEATURE_SPACE

        predicted_index = self.classifier.predict(protein_vector)[0]
        predicted_class = self.le.inverse_transform([predicted_index])[0]

        predict_proba = self.classifier.predict_proba(protein_vector)[0][
            predicted_index
        ]
        accuracy = round(predict_proba * 100.0, 2)

        prediction_data = [predicted_index, predicted_class, accuracy]

        return pd.DataFrame(data=[prediction_data], columns=self.SUPPORTED_COLUMNS)
