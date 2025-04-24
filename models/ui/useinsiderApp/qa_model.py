from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from models.ui.base_model import BasePage


class QualityAssurancePage(BasePage):

  url = "https://useinsider.com/careers/quality-assurance/"

  see_all_qa_jobs_button = (By.XPATH, "//a[@href='https://useinsider.com/careers/open-positions/?department=qualityassurance']")


  def click_see_all_qa_jobs(self):
    self.wait.until(EC.element_to_be_clickable(self.see_all_qa_jobs_button)).click()