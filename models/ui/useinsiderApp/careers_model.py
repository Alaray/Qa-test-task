from selenium.webdriver.common.by import By

from models.ui.base_model import BasePage


class CareersPage(BasePage):

    url = "https://useinsider.com/careers/"

    locations_block = (By.XPATH, "//section[@id='career-our-location']")
    teams_block = (By.XPATH, "//section[@id='career-find-our-calling']")
    life_at_insider_block = (By.XPATH, "//section[@data-id='a8e7b90']")


    def is_locations_block_displayed(self):
        return self.driver.find_element(*self.locations_block).is_displayed()

    def is_teams_block_displayed(self):
        return self.driver.find_element(*self.teams_block).is_displayed()

    def is_life_at_insider_block_displayed(self):
        return self.driver.find_element(*self.life_at_insider_block).is_displayed()