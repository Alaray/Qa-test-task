import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class HomePage:
  def __init__(self, driver):
    self.driver = driver
    self.url = "https://useinsider.com/"
    self.company_menu = (By.XPATH, "(//a[@id='navbarDropdownMenuLink']//parent::li)[5]")
    self.accept_cookies = (By.XPATH, "//a[@data-cli_action='accept_all']")

  def open(self):
    self.driver.get(self.url)
    WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.accept_cookies)).click()

  def is_homepage_open(self):
    return self.driver.current_url == self.url

  def hover_company_menu(self):
    company = self.driver.find_element(*self.company_menu)
    ActionChains(self.driver).move_to_element(company).perform()

class CareersPage:
  def __init__(self, driver):
    self.driver = driver
    self.careers_link = (By.XPATH, "//a[@href='https://useinsider.com/careers/']")
    self.locations_block = (By.XPATH, "//section[@id='career-our-location']")
    self.teams_block = (By.XPATH, "//section[@id='career-find-our-calling']")
    self.life_at_insider_block = (By.XPATH, "//section[@data-id='a8e7b90']")

  def click_careers(self):
    self.driver.find_element(*self.careers_link).click()

  def is_locations_block_displayed(self):
    return self.driver.find_element(*self.locations_block).is_displayed()

  def is_teams_block_displayed(self):
    return self.driver.find_element(*self.teams_block).is_displayed()

  def is_life_at_insider_block_displayed(self):
    return self.driver.find_element(*self.life_at_insider_block).is_displayed()

class QualityAssurancePage:
  def __init__(self, driver):
    self.driver = driver
    self.url = "https://useinsider.com/careers/quality-assurance/"
    self.see_all_qa_jobs_button = (By.XPATH, "//a[@href='https://useinsider.com/careers/open-positions/?department=qualityassurance']")

  def open(self):
    self.driver.get(self.url)

  def click_see_all_qa_jobs(self):
    WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.see_all_qa_jobs_button)).click()

class JobsPage:
  def __init__(self, driver):
    self.driver = driver
    self.location_filter = (By.ID, "select2-filter-by-location-container")
    self.filter_options = (By.XPATH, "//select[id@='filter-by-location']")
    self.department_filter = (By.ID, "select2-filter-by-department-container")
    self.quality_assurance_option = (By.XPATH, "//li[contains(text(),'Quality Assurance')]")
    self.job_list = (By.XPATH, "//div[@id='jobs-list']/div")
    self.position_text = (By.XPATH, "//p[contains(@class, 'position-title')]")
    self.department_text = (By.XPATH, "//span[contains(@class, 'position-department')]")
    self.location_text = (By.XPATH, "//div[contains(@class, 'position-location')]")
    self.view_role_button = (By.XPATH, "//a[contains(text(),'View Role')]")

  def filter_by_location(self):
    (WebDriverWait(self.driver, 15, 0.5)
     .until(EC.presence_of_element_located((By.XPATH, "//option[@class='job-location istanbul-turkiye']"))))
    select = Select(self.driver.find_element(By.XPATH, "//select[@id='filter-by-location']"))
    select.select_by_visible_text("Istanbul, Turkiye")


  def filter_by_department(self):
    WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, "//option[@class='job-team qualityassurance']")))
    select = Select(self.driver.find_element(By.XPATH, "//select[@id='filter-by-department']"))
    select.select_by_visible_text("Quality Assurance")

  def is_jobs_list_present(self):
    return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.job_list))

  def get_all_jobs(self):
    WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='jobs-list']/div[@data-location='istanbul-turkiye' and @data-team='qualityassurance']")))
    return self.driver.find_elements(*self.job_list)

  def check_job_details(self, job):
    WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.position_text))
    position = job.find_element(*self.position_text).text
    department = job.find_element(*self.department_text).text
    location = job.find_element(*self.location_text).text
    assert "Quality Assurance" in position, "Quality Assurance is not displayed in position."
    assert "Quality Assurance" == department, "Quality Assurance is not displayed in department."
    assert "Istanbul, Turkiye" == location, "Istanbul, Turkiye is not displayed in location."

  def click_view_role(self, job):
    hover = ActionChains(self.driver).move_to_element(job)
    hover.perform()
    WebDriverWait(job, 10).until(EC.element_to_be_clickable(self.view_role_button)).click()

class LeverApplicationPage:
  def __init__(self, driver):
    self.driver = driver

  def is_lever_application_page(self):
    return "lever.co" in self.driver.current_url

def take_screenshot(driver, filename="screenshot.png"):
  driver.save_screenshot(filename)
  print(f"Screenshot saved: {filename}")

@pytest.fixture(params=["chrome"])
def browser(request):
  browser_name = request.param
  if browser_name == "chrome":
    driver = webdriver.Chrome()
  # elif browser_name == "firefox":
  #   driver = webdriver.Firefox()
  else:
    raise ValueError(f"Unsupported browser: {browser_name}")
  driver.maximize_window()
  yield driver
  driver.quit()

def test_insider_qa_jobs(browser):
  try:
    # Step 1
    home_page = HomePage(browser)
    home_page.open()
    assert home_page.is_homepage_open(), "Insider home page did not open."
    print("Step 1: Insider home page is opened.")

    # Step 2
    home_page.hover_company_menu()
    careers_page = CareersPage(browser)
    careers_page.click_careers()
    assert careers_page.is_locations_block_displayed(), "Locations block is not displayed on Careers page."
    assert careers_page.is_teams_block_displayed(), "Teams block is not displayed on Careers page."
    assert careers_page.is_life_at_insider_block_displayed(), "Life at Insider block is not displayed on Careers page."
    print("Step 2: Career page and its blocks are opened.")

    # Step 3
    qa_page = QualityAssurancePage(browser)
    qa_page.open()
    qa_page.click_see_all_qa_jobs()
    jobs_page = JobsPage(browser)
    assert jobs_page.is_jobs_list_present(), "Jobs list is not present after clicking 'See all QA jobs'."
    jobs_page.filter_by_location()
    jobs_page.filter_by_department()
    assert len(jobs_page.get_all_jobs()) > 0, "No jobs found after filtering."
    print("Step 3: QA jobs filtered by Location - Istanbul, Turkey and department - Quality Assurance. Jobs list is present.")

    # Step 4
    all_jobs = jobs_page.get_all_jobs()
    for job in all_jobs:
      jobs_page.check_job_details(job)
    print("Step 4: All jobs' Position, Department, and Location contain the expected values.")

    # Step 5
    if jobs_page.get_all_jobs():
      first_job = jobs_page.get_all_jobs()[0]
      jobs_page.click_view_role(first_job)
      browser.switch_to.window(browser.window_handles[1])
      lever_page = LeverApplicationPage(browser)
      assert lever_page.is_lever_application_page(), "Clicking 'View Role' did not redirect to Lever Application form page."
      print("Step 5: Clicking 'View Role' redirects to Lever Application form page.")
    else:
      print("Step 5: No jobs found to click 'View Role'. Skipping this step.")

  except Exception as e:
    print(f"Test failed: {e}")
    take_screenshot(browser, f"failed_screenshot_{browser.name}.png")
    raise