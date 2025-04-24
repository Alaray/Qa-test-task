from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from models.ui.base_model import BasePage


class HomePage(BasePage):

    url = "https://useinsider.com/"

    company_menu = (By.XPATH, "(//a[@id='navbarDropdownMenuLink']//parent::li)[5]")
    careers_link = (By.XPATH, "//a[@href='https://useinsider.com/careers/']")
    accept_cookies = (By.XPATH, "//a[@data-cli_action='accept_all']")

    def click_careers(self):
        self.driver.find_element(*self.careers_link).click()


    def hover_company_menu(self):
        company = self.driver.find_element(*self.company_menu)
        ActionChains(self.driver).move_to_element(company).perform()