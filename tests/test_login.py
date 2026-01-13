

from driver.driver_factory import get_driver
from pages.login_page import LoginPage
from utils.google_sheet_reader import GoogleSheetReader
from utils.locator_reader import LocatorReader
from utils.csv_writer import CSVWriter
from utils.logger import get_logger
from dotenv import load_dotenv
import os

TEST_NAME = "login"
load_dotenv()
LOCATOR_CSV = os.getenv("LOCATOR_CSV")
LOGIN_DATA_CSV =os.getenv("LOGIN_DATA_CSV")

logger = get_logger(TEST_NAME,"login_log")
logger.info("===== LOGIN TEST STARTED =====")

driver = get_driver()
driver.get("https://dev-portal.ac9ai.com/login")

locator_reader = LocatorReader(LOCATOR_CSV,logger)
login_page = LoginPage(driver, locator_reader)

assert login_page.is_page_displayed(), "Login page not displayed"

df = GoogleSheetReader(LOGIN_DATA_CSV).read_data()

actuals, statuses = [], []
passed = failed = 0

for _, row in df.iterrows():
    row_dict = row.to_dict()
    logger.info(f"Executing test case: {row_dict}")

    login_page.login_dynamic(row_dict)

    status, missing = login_page.verify_expected_locators(
        login_page.PAGE_NAME,
        row_dict["expected_result"]
    )

    if status:
        actuals.append(row_dict["expected_result"])
        statuses.append("PASS")
        passed += 1
        logger.info("TEST PASSED")
    else:
        actuals.append("Missing: " + ",".join(missing))
        statuses.append("FAIL")
        failed += 1
        logger.error("TEST FAILED")


CSVWriter.write_results(TEST_NAME, df, actuals, statuses)
CSVWriter.write_summary(TEST_NAME, len(df), passed, failed)

driver.quit()
logger.info("===== LOGIN TEST COMPLETED =====")
