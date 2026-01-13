import pandas as pd
import time
from utils.logger import get_logger

class GoogleSheetReader:

    def __init__(self, csv_url, test_name=None):
        self.logger = get_logger(test_name)
        self.logger.info("Reading Google Sheet")
        """"
        self.df = pd.read_csv(
            csv_url,
            engine="python",
            on_bad_lines="skip"
        )change this read csv because it will get the data from cache 
        """
        cache_buster = int(time.time())
        fresh_url = f"{csv_url}&_={cache_buster}"

        self.df = pd.read_csv(
            fresh_url,
            engine="python",
            on_bad_lines="skip"
        )
        self.df = self.df.fillna("")

    def read_data(self):
        self.df.columns = [
            c.strip().lower().replace(" ", "_")
            for c in self.df.columns
        ]
        return self.df
