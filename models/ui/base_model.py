from venv import logger

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:

    driver = None
    wait = None
    url = None

    accept_cookies = (By.XPATH, "//a[@data-cli_action='accept_all']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def open(self):
        self.driver.get(self.url)
        try:
            WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable(self.accept_cookies)).click()
        except:
            logger.info('No accept cookies present')

    def is_opened(self):
        return self.url in self.driver.current_url

def take_screenshot(driver, filename="screenshot.png"):
    driver.save_screenshot(filename)
    print(f"Screenshot saved: {filename}")