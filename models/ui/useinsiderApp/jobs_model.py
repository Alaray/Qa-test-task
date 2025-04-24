from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC

from models.ui.base_model import BasePage


class JobsPage(BasePage):

  url = "https://useinsider.com/careers/open-positions/"

  location_filter = (By.ID, "select2-filter-by-location-container")
  filter_options = (By.XPATH, "//select[id@='filter-by-location']")
  department_filter = (By.ID, "select2-filter-by-department-container")
  quality_assurance_option = (By.XPATH, "//li[contains(text(),'Quality Assurance')]")
  job_list = (By.XPATH, "//div[@id='jobs-list']/div")
  position_text = (By.XPATH, "//p[contains(@class, 'position-title')]")
  department_text = (By.XPATH, "//span[contains(@class, 'position-department')]")
  location_text = (By.XPATH, "//div[contains(@class, 'position-location')]")
  view_role_button = (By.XPATH, "//a[contains(text(),'View Role')]")

  def filter_by_location(self):
    self.wait.until(EC.presence_of_element_located((By.XPATH, "//option[@class='job-location istanbul-turkiye']")))
    select = Select(self.driver.find_element(By.XPATH, "//select[@id='filter-by-location']"))
    select.select_by_visible_text("Istanbul, Turkiye")


  def filter_by_department(self):
    self.wait.until(EC.presence_of_element_located((By.XPATH, "//option[@class='job-team qualityassurance']")))
    select = Select(self.driver.find_element(By.XPATH, "//select[@id='filter-by-department']"))
    select.select_by_visible_text("Quality Assurance")

  def is_jobs_list_present(self):
    return self.wait.until(EC.visibility_of_element_located(self.job_list))

  def get_all_jobs(self):
    self.wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@id='jobs-list']/div[@data-location='istanbul-turkiye' and @data-team='qualityassurance']")))
    return self.driver.find_elements(*self.job_list)

  def check_job_details(self, job):
    self.wait.until(EC.visibility_of_element_located(self.position_text))
    position = job.find_element(*self.position_text).text
    department = job.find_element(*self.department_text).text
    location = job.find_element(*self.location_text).text
    assert "Quality Assurance" in position, "Quality Assurance is not displayed in position."
    assert "Quality Assurance" == department, "Quality Assurance is not displayed in department."
    assert "Istanbul, Turkiye" == location, "Istanbul, Turkiye is not displayed in location."

  def click_view_role(self, job):
    hover = ActionChains(self.driver).move_to_element(job)
    hover.perform()
    self.wait.until(EC.element_to_be_clickable(self.view_role_button)).click()