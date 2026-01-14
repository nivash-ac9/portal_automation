from pages.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

class LoginPage(BasePage):
    PAGE_NAME = "login"

    def is_page_displayed(self):
        return super().is_page_displayed(self.PAGE_NAME, "Login_title")

    def reset_form(self):
        self.logger.info("Resetting login form")
        for name in self.locator_reader.get_page_inputs(self.PAGE_NAME):
            try:
                el = self.find(self.PAGE_NAME, name,visible=False)
                if not el:
                    continue
                el.click()
                self._select_all(el)
                el.send_keys(Keys.TAB)
            except:
                pass

    def login_dynamic(self, row_dict):
        self.reset_form()

        for col, val in row_dict.items():

            if col in ["expected_result", "test_id"]:
                continue

            if val == "" or val is None:
                continue

            locator_name = f"{col}_input"

            el = self.find(self.PAGE_NAME, locator_name,visible=False)
            if not el:
                self.logger.warning(f"Field skipped: {locator_name}")
                continue

            self.logger.info(f"Typing {col}")
            el.click()
            el.clear()
            el.send_keys(str(val))

        btn = self.find(self.PAGE_NAME, "login_btn",visible=False)
        if btn:
            self.logger.info("Clicking login button")
            btn.click()

        #  MANUAL LOGIN
    def login_manual_dynamic(self, login_data: dict):


        self.logger.info("Performing manual dynamic login")
        self.reset_form()

        for field, value in login_data.items():

            if value in ("", None):
                self.logger.warning(f"Skipping empty login field: {field}")
                continue

            locator_name = f"{field}_input"
            el = self.find(self.PAGE_NAME, locator_name,visible=False)

            if not el:
                self.logger.warning(f"Login field skipped (locator missing): {locator_name}")
                continue

            self.logger.info(f"Typing login field: {field}{value}")
            el.click()
            self._select_all(el)
            el.send_keys(str(value))

        btn = self.find(self.PAGE_NAME, "login_btn",visible=False)
        if btn:
            self.logger.info("Clicking login button")
            btn.click()
        else:
            self.logger.error("Login button not found")

