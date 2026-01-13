import pandas as pd
from selenium.webdriver.common.by import By
from utils.logger import get_logger

class LocatorReader:

    BY_MAP = {
        "id": By.ID,
        "name": By.NAME,
        "xpath": By.XPATH,
        "css": By.CSS_SELECTOR,
        "class": By.CLASS_NAME
    }

    def __init__(self, csv_url, logger):
        self.df = pd.read_csv(csv_url)
        self.df.columns = [c.strip().lower() for c in self.df.columns]
        self.logger = logger

    def get(self, page, name):
        row = self.df[
            (self.df["page"] == page) &
            (self.df["name"] == name)
        ]

        if row.empty:
            self.logger.error(f"Locator NOT FOUND → {page}.{name}")
            return None, None   #  NO EXCEPTION

        locator_type = str(row.iloc[0]["locator_type"]).lower()
        locator_value = str(row.iloc[0]["locator_value"])

        if locator_type not in self.BY_MAP:
            self.logger.error(
                f"Invalid locator type → {locator_type} for {page}.{name}"
            )
            return None, None

        return self.BY_MAP[locator_type], locator_value

    def get_page_inputs(self, page):
        return self.df[
            (self.df["page"] == page) &
            (self.df["name"].str.endswith("_input"))
        ]["name"].tolist()
