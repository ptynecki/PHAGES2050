from datetime import date
from typing import List

import pandas as pd

from lxml import html
from lxml.etree import ParserError

import requests


class MillardLabPhagesCrawler:
    """
    MillardLab bacteriophages tabular data crawler
    
    This class allows you to create DataFrame or save it as CSV with columns:
    - Accession
    - Description
    - Classification
    - Genome Length(bp)
    - molGC
    
    Each of the cell is normalised before by strip and upper strings methods

    Example usage:

        from crawlers.millardlab.crawler import MillardLabPhagesCrawler

        ml_pc = MillardLabPhagesCrawler(
            url='http://millardlab.org/bioinformatics/bacteriophage-genomes/phage-genomes-july2020/'
        )
        ml_pc.to_df()
        ml_pc.to_csv()
    """

    def __init__(self, url: str):
        self.url = url
        self.df = None
        today = date.today()
        self.csv_name = f"millardlab_{today}.csv"

        self.columns = [
            "Accession",
            "Description",
            "Classification",
            "Genome Length(bp)",
            "molGC",
        ]

    @staticmethod
    def _extract_text(element) -> str:
        """
        Return string without blank chars
        and in uppercase format
        """

        return element.text.strip().upper()

    def _get_html(self) -> str:
        """
        Request to MillardLab webiste URL
        and return HTML as string if
        status code is 200
        """

        try:
            response = requests.get(self.url)

            if response.status_code == 200:
                return response.text
            else:
                print(f"[DEBUG] Status code is not valid: {response.status_code}")

                return ""
        except requests.exceptions.RequestException as e:
            print(f"[DEBUG] Request exception: {e}")

            return ""

    def _process_element(self, document, xpath: str) -> map:
        """
        Return iterator with normalised elements
        """

        return map(self._extract_text, document.xpath(xpath))

    def _process_html(self) -> List:
        """
        Extract text from each table cell
        """

        try:
            document = html.document_fromstring(self._get_html())

            # Accession (as hyperlink)
            acc_numbers = self._process_element(
                document, "//td[contains(@class, 'column-1')]/a"
            )

            # Description
            descriptions = self._process_element(
                document, "//td[contains(@class, 'column-2')]"
            )

            # Classification
            taxonomies = self._process_element(
                document, "//td[contains(@class, 'column-3')]"
            )

            # Genome Length(bp)
            bps = self._process_element(document, "//td[contains(@class, 'column-4')]")

            # molGC
            gcs = self._process_element(document, "//td[contains(@class, 'column-5')]")

            samples = list(zip(acc_numbers, descriptions, taxonomies, bps, gcs))
        except ParserError:
            return []

        return samples

    def to_df(self) -> pd.DataFrame:
        """
        Return data as DataFrame sorted
        by first column (Accession)
        """

        samples = self._process_html()

        self.df = (
            pd.DataFrame(data=samples, columns=self.columns)
            .sort_values(self.columns[0])
            .reset_index()
            .drop("index", axis=1)
        )

        return self.df

    def to_csv(self) -> None:
        """
        Return DataFrame as CSV file
        (filename format: millardlab_<YYYY:MM:DD>.csv)
        """

        self.to_df()

        self.df.to_csv(self.csv_name, index=False)
