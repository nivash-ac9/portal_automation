from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from datetime import time as dt_time
import time


class LiveDarshanPage(BasePage):

    LIST_PAGE = "live_darshan_list"
    CREATE_PAGE = "create_livedarshan"
    EDIT_PAGE = "edit_livedarshan"
    MSG_PAGE = "live_darshan_msg"

    # ---------------- INIT ----------------
    def __init__(self, driver, locator_reader, timeout=10):
        super().__init__(driver, locator_reader, timeout)

    # ---------------- PAGE DISPLAY ----------------
    def is_page_displayed(self, page=None, element_name=None):
        self.logger.info("Waiting for Live Darshan page to load...")
        return self.find(page, element_name) is not None

    # ==================================================
    # CREATE FLOW
    # ==================================================
    def click_create_now(self):
        btn = self.find(self.LIST_PAGE, "create_now_btn")
        if btn:
            btn.click()
            time.sleep(1)

    def fill_create_form(self, row_dict):
        self.logger.info("Filling Create Live Darshan form")

        for col, val in row_dict.items():
            if col in ["expected_result", "test_id", "action"] or val == "":
                continue

            locator_name = f"{col}_input"
            el = self.find(self.CREATE_PAGE, locator_name)

            if not el:
                continue

            el.click()
            time.sleep(0.2)
            el.send_keys(Keys.CONTROL, "a")
            el.send_keys(Keys.DELETE)
            el.send_keys(str(val))
            time.sleep(0.3)

            if col == "timezone":
                el.send_keys(Keys.ENTER)
                time.sleep(0.4)

                # DO NOT use el again (it is stale now)
                # Close dropdown using BODY
                self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
                time.sleep(0.3)

                continue

            el.send_keys(Keys.TAB)
            time.sleep(0.2)

    def submit_create(self):
        btn = self.find(self.CREATE_PAGE, "create_btn")
        if btn:
            btn.click()
            time.sleep(1)

    def verify_create(self, expected):
        if expected in "create_edit_success_msg":
            return self.verify_expected_locators(self.MSG_PAGE, expected)
        return self.verify_expected_locators(self.CREATE_PAGE, expected)

    def is_create_modal_open(self):
        return self.find(self.CREATE_PAGE, "create_btn") is not None

    # ==================================================
    #  EDIT FLOW
    # ==================================================

    def click_edit_by_row(self, date, time_val, timezone):
        """
        Click EDIT icon for the exact row using row values
        """
        self.logger.info(
            f"Clicking EDIT for row: {date} | {time_val} | {timezone}"
        )

        xpath = (
              f"(//tr["
        f"td[normalize-space()='{date}'] and "
        f"td[normalize-space()='{time_val}'] and "
        f"td[normalize-space()='{timezone}']"
        f"]//button)[3]"
        )
        print(xpath)
        el = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        el.click()
        time.sleep(1)

        self.logger.info("Edit modal opened")

    def fill_edit_form(self, row_dict):
        self.logger.info("Filling Edit Live Darshan form")

        for col, val in row_dict.items():
            if col in [
                "test_id", "expected_result",
                "row_date", "row_time", "row_timezone", "start_time"
            ]:
                continue

            locator_name = f"{col}_input"

            try:
                el = self.safe_click(self.EDIT_PAGE, locator_name)
                el.click()
                time.sleep(0.2)

                if col == "date" and val == "":
                    self.force_clear_date_input(el)
                    continue

                if col == "timezone":
                    el.click()
                    time.sleep(0.2)

                    # Clear existing value
                    el.send_keys(Keys.CONTROL, "a")
                    el.send_keys(Keys.DELETE)
                    time.sleep(0.2)

                    # Type timezone
                    el.send_keys(str(val))
                    time.sleep(0.6)  # allow dropdown to filter
                    # ✅ Click body to close dropdown safely
                    self.driver.find_element(By.TAG_NAME, "body").click()
                    time.sleep(0.4)

                    continue

                # Normal input fields
                else:
                    el.clear()
                    el.send_keys(Keys.CONTROL, "a")
                    el.send_keys(Keys.DELETE)
                    el.send_keys(str(val))
                    time.sleep(0.3)

                    el.send_keys(Keys.TAB)
                    time.sleep(0.2)

            except Exception as e:
                self.logger.warning(
                    f"Edit field skipped due to DOM refresh: {locator_name} → {e}"
                )




    def submit_edit(self):
        btn = self.find(self.EDIT_PAGE, "save_btn")
        if not btn:
            raise Exception("Edit Save button not found")

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);", btn
        )
        time.sleep(0.3)
        self.driver.execute_script(
            "arguments[0].click();", btn
        )
        time.sleep(1)

    def verify_edit(self, expected):
        return self.verify_expected_locators(self.MSG_PAGE, expected)

    # ==================================================
    # PAGINATION
    # ==================================================
    def go_to_page(self, page_no):
        locator_name = f"pagination_{page_no}"
        el = self.find(self.LIST_PAGE, locator_name)
        if el:
            el.click()
            time.sleep(1)

    # ==================================================
    # MANTINE TIME HANDLER
    # ==================================================
    def set_mantine_time_input(self, el, time_24):
        ui_time = datetime.strptime(time_24, "%H:%M").strftime("%I:%M %p")
        el.click()
        time.sleep(0.2)

        el.send_keys(Keys.CONTROL, "a")
        el.send_keys(Keys.DELETE)

        for ch in ui_time:
            el.send_keys(ch)
            time.sleep(0.05)

        el.send_keys(Keys.TAB)
        time.sleep(0.3)

    ## Safe to clear the previous data on field
    def clear_mantine_input(self, el):
        el.click()
        time.sleep(0.2)
        el.send_keys(Keys.CONTROL, "a")
        el.send_keys(Keys.DELETE)
        time.sleep(0.3)

        # click outside to apply clear
        self.driver.find_element(By.TAG_NAME, "body").click()
        time.sleep(0.3)
