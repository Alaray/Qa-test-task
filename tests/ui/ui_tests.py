import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from models.ui.base_model import take_screenshot
from models.ui.leverApp.job_model import LeverApplicationPage
from models.ui.useinsiderApp.careers_model import CareersPage
from models.ui.useinsiderApp.home_model import HomePage
from models.ui.useinsiderApp.jobs_model import JobsPage
from models.ui.useinsiderApp.qa_model import QualityAssurancePage


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
    assert home_page.is_opened(), "Insider home page did not open."
    print("Step 1: Insider home page is opened.")

    # Step 2
    home_page.hover_company_menu()
    home_page.click_careers()
    careers_page = CareersPage(browser)
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
    first_job = jobs_page.get_all_jobs()[0]
    jobs_page.click_view_role(first_job)
    browser.switch_to.window(browser.window_handles[1])
    lever_page = LeverApplicationPage(browser)
    assert lever_page.is_opened(), "Clicking 'View Role' did not redirect to Lever Application form page."
    print("Step 5: Clicking 'View Role' redirects to Lever Application form page.")

  except Exception as e:
    print(f"Test failed: {e}")
    take_screenshot(browser, f"failed_screenshot_{browser.name}.png")
    raise