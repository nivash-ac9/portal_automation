from driver.driver_factory import get_driver
from pages.login_page import LoginPage
from pages.live_darshan_page import LiveDarshanPage
from utils.google_sheet_reader import GoogleSheetReader
from utils.locator_reader import LocatorReader
from utils.csv_writer import CSVWriter
from utils.logger import get_logger
from dotenv import load_dotenv
import os

# --------------------------------------------------
# CONFIG
# --------------------------------------------------
TEST_NAME = "live_darshan"
load_dotenv()

LOCATOR_CSV = os.getenv("LOCATOR_CSV")

CREATE_CSV = os.getenv("LIVE_DARSHAN_CREATE_CSV")
EDIT_CSV = os.getenv("LIVE_DARSHAN_EDIT_CSV")
PAGINATION_CSV = os.getenv("LIVE_DARSHAN_PAGINATION_CSV")

# --------------------------------------------------
# LOGGER
# --------------------------------------------------
logger = get_logger(TEST_NAME, "live_darshan")
logger.info("==============================================")
logger.info(" LIVE DARSHAN AUTOMATION TEST STARTED")
logger.info("==============================================")

# --------------------------------------------------
# DRIVER SETUP
# --------------------------------------------------
driver = get_driver()
driver.get("https://dev-portal.ac9ai.com/login")

locator_reader = LocatorReader(LOCATOR_CSV, logger)

# --------------------------------------------------
# LOGIN
# --------------------------------------------------
logger.info(" LOGIN TEST STARTED")

login_page = LoginPage(driver, locator_reader)
assert login_page.is_page_displayed(), "Login page not displayed"

login_data = {
    "username": "test-tenant-admin-us@abovecloud9.ai",
    "password": "Abovecloud@ac9"
}

login_page.login_manual_dynamic(login_data)
logger.info(" LOGIN SUCCESSFUL")

# --------------------------------------------------
# LIVE DARSHAN PAGE
# --------------------------------------------------
logger.info(" NAVIGATING TO LIVE DARSHAN PAGE")

live_page = LiveDarshanPage(driver, locator_reader)
assert live_page.is_page_displayed("live_darshan_list","title"), "Live Darshan page not displayed"

logger.info(" LIVE DARSHAN PAGE LOADED")
passed_ids,failed_ids=[],[]
# ==================================================
# COMMON EXECUTOR
# ==================================================
def execute_and_report(test_name, df, executor):
    actuals, statuses = [], []
    passed = failed = 0

    logger.info(f"{test_name.upper()} TEST EXECUTION STARTED")
    for _, row in df.iterrows():
        row_dict = row.to_dict()
        logger.info(f"Executing {test_name}: {row_dict}")

        status, missing = executor(row_dict)

        if status:
            actuals.append(row_dict.get("expected_result"))
            statuses.append("PASS")
            passed += 1
            passed_ids.append(row_dict.get("test_id"))
            logger.info(" TEST PASSED")
        else:
            actuals.append("Missing: " + ",".join(missing))
            statuses.append("FAIL")
            failed += 1
            failed_ids.append(row_dict.get("test_id"))
            logger.error(" TEST FAILED")

    CSVWriter.write_results(test_name, df, actuals, statuses)
    CSVWriter.write_summary(test_name, len(df), passed, failed, passed_ids, failed_ids)

    logger.info(
        f"{test_name.upper()} COMPLETED | Passed: {passed}, Failed: {failed}"
    )

    return passed, failed

# ==================================================
# CREATE TESTS
# ==================================================
logger.info(" LIVE DARSHAN CREATE TESTS STARTED")

df_create = GoogleSheetReader(
    CREATE_CSV,
    TEST_NAME
).read_data()

def run_create(row):
    if not live_page.is_create_modal_open():
        live_page.click_create_now()

    live_page.fill_create_form(row)
    live_page.submit_create()
    return live_page.verify_create(row["expected_result"])

p_create, f_create = execute_and_report(
    "live_darshan_create",
    df_create,
    run_create
)

""""
# ==================================================
# EDIT TESTS 
# ==================================================
logger.info(" LIVE DARSHAN EDIT TESTS STARTED")

df_edit = GoogleSheetReader(
    EDIT_CSV,
    TEST_NAME
).read_data()

def run_edit(row):

    if not live_page.is_page_displayed("edit_livedarshan","edit_title"):

        # Click EDIT icon based on row values (date, time, timezone)
        live_page.click_edit_by_row(
            row["row_date"],
            row["row_time"],
            row["row_timezone"]
        )

    # Fill edit form using sheet data
    live_page.fill_edit_form(row)

    # Submit edit
    live_page.submit_edit()

    # Verify expected result
    return live_page.verify_edit(row["expected_result"])

p_edit, f_edit = execute_and_report(
    "live_darshan_edit",
    df_edit,
    run_edit
)
"""
# ==================================================
# PAGINATION TESTS
# ==================================================
""""
logger.info(" LIVE DARSHAN PAGINATION TESTS STARTED")

df_page = GoogleSheetReader(
    PAGINATION_CSV,
    TEST_NAME
).read_data()

def run_pagination(row):
    live_page.go_to_page(row["page_no"])
    return live_page.verify_expected_locators(row["expected_result"])

p_page, f_page = execute_and_report(
    "live_darshan_pagination",
    df_page,
    run_pagination
)
"""
# ==================================================
# OVERALL SUMMARY
# ==================================================
"""
total_passed =  p_create+   p_edit
total_failed = f_create+f_edit
total_tests = total_passed + total_failed
"""
total_passed =  p_create
total_failed = f_create
total_tests = total_passed + total_failed

CSVWriter.write_summary(
    "live_darshan_overall",
    total_tests,
    total_passed,
    total_failed,
    passed_ids,
    failed_ids,
)

logger.info("==============================================")
logger.info(" LIVE DARSHAN AUTOMATION TEST COMPLETED")
logger.info(f"TOTAL: {total_tests} | PASSED: {total_passed} | FAILED: {total_failed}")
logger.info("==============================================")

# --------------------------------------------------
# TEARDOWN
# --------------------------------------------------
driver.quit()
