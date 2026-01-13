from datetime import time
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import platform
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
class BasePage:

    def __init__(self, driver, locator_reader, timeout=10):
        self.driver = driver
        self.locator_reader = locator_reader
        self.timeout = timeout
        self.logger = locator_reader.logger

    def find(self, page, name):
        self.logger.info(f"Finding element: {page}.{name}")

        by, value = self.locator_reader.get(page, name)
        #print(value,by)
        if not by or not value:
            self.logger.error(
                f"Element SKIPPED (locator missing): {page}.{name}"
            )
            return None

        try:
            return WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located((by, value))
            )
        except Exception as e:
            self.logger.error(
                f"Element NOT visible: {page}.{name}"
            )
            return None

    # ADD THIS METHOD
    def is_page_displayed(self, page, element_name):
        self.logger.info(f"Checking page display: {page}")

        el = self.find(page, element_name)
        #print(el)#remove

        if el:
            self.logger.info(f"{page} page displayed")
            return True

        self.logger.error(f"{page} page NOT displayed")
        return False

    def _select_all(self, element):
        system = platform.system()

        if system == "Darwin":  # macOS
            element.send_keys(Keys.COMMAND + "a")
        else:  # Windows + Linux
            element.send_keys(Keys.CONTROL + "a")

        element.send_keys(Keys.BACKSPACE)

    def verify_expected_locators(self, page, expected, timeout=10):
        if not expected:
            self.logger.warning("No expected result provided")
            return True, []

        missing = []
        self.logger.info(f"Verifying expected on page [{page}]: {expected}")

        for name in expected.split(","):
            name = name.strip()
            try:
                by, value = self.locator_reader.get(page, name)
                WebDriverWait(self.driver, timeout).until(
                    EC.visibility_of_element_located((by, value))
                )
                self.logger.info(f"Found: {page}.{name}")
            except TimeoutException:
                self.logger.error(f"Missing: {page}.{name}")
                missing.append(name)

        return len(missing) == 0, missing

    def find_by_xpath(self, xpath):
        try:
            return WebDriverWait(self.driver, self.timeout).until(
                lambda d: d.find_element(By.XPATH, xpath)
            )
        except Exception as e:
            self.logger.error(f"XPath not found: {xpath}")
            return None

    def safe_click(self, page, locator_name, retries=3):
        for _ in range(retries):
            try:
                el = self.find(page, locator_name)
                if el:
                    el.click()
                    return el
            except Exception:
                time.sleep(0.3)
        raise Exception(f"Unable to click element: {page}.{locator_name}")

    def force_clear_date_input(self, el):
        self.driver.execute_script("""
            const input = arguments[0];

            // Clear value
            input.value = '';

            // Trigger Mantine / React events
            input.dispatchEvent(new Event('input', { bubbles: true }));
            input.dispatchEvent(new Event('change', { bubbles: true }));
            input.dispatchEvent(new Event('blur', { bubbles: true }));
        """, el)

        time.sleep(0.3)







