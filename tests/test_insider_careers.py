import unittest
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.webdriver import get_driver
from pages.home_page import HomePage
from pages.careers_page import CareersPage
from pages.open_positions_page import OpenPositionsPage
import logging
from datetime import datetime
import time

from pages.home_page import HomePage
from utils import setup_logger

class InsiderTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logger = setup_logger()

    def setUp(self):
        self.driver = get_driver()
        self.driver.maximize_window()
        self.start_time = datetime.now()
        self.logger.info(f"{'='*50}")
        self.logger.info(f"Test started at: {self.start_time}")
        

    def tearDown(self):
        end_time = datetime.now()
        duration = end_time - self.start_time
        self.logger.info(f"Test ended at: {end_time}")
        self.logger.info(f"Test duration: {duration}")

        # Getting the result
        result = self._get_test_result()

        error = self.list2reason(result.errors)
        failure = self.list2reason(result.failures)
        ok = not error and not failure

        if ok:
            self.logger.info("Test result: PASS")
        else:
            self.logger.info("Test result: FAIL")
            if error:
                self.logger.error(f"Error: {error}")
            if failure:
                self.logger.error(f"Failure: {failure}")

        if hasattr(self, 'driver') and self.driver:
            self.driver.quit()

        super().tearDown()  # call the tearDown method of the parent class

    def _get_test_result(self):
        if hasattr(self, '_outcome'):  # Python 3.4+
            result = self.defaultTestResult()
            self._outcome.result = result
            return result
        else:  # Python 3.2 - 3.3 +
            return getattr(self, '_outcomeForDoCleanups', getattr(self, '_resultForDoCleanups', None))

    def list2reason(self, exc_list):
        if exc_list and exc_list[-1][0] is self:
            return exc_list[-1][1]
        return None
    def test_insider_careers(self):
        home_page = HomePage(self.driver, self.logger)
        careers_page = CareersPage(self.driver, self.logger)
        open_positions_page = OpenPositionsPage(self.driver, self.logger)
# Step 1: Check home page
        try:
            home_page.open()
            self.logger.info("Step 1: Home page opened successfully")
        except Exception as e:
            self.logger.error(f"Step 1 failed: {str(e)}")
            raise
# Step 2: Navigate to Careers page and check elements
        try:
            home_page.navigate_to_careers()
            self.logger.info("Step 2: Navigated to Careers page successfully")
            careers_page.check_page_elements()
            self.logger.info("Step 2: page elements checked")
        except Exception as e:
            self.logger.error(f"Step 2 failed: {str(e)}")
            raise
# Step 3: Go to QA jobs page and filter
        try:
            self.driver.get("https://useinsider.com/careers/quality-assurance/")
            
            self.logger.info("Navigated to Quality Assurance careers page")
    # Create a sample of CareersPage
            careers_page = CareersPage(self.driver, self.logger)
    # Click 'See all QA jobs' button
            careers_page.click_see_all_qa_jobs()
            self.logger.info("Step 3: Clicked 'See all QA jobs' successfully") 
    # Wait for Department element to load
            time.sleep(10)
            self.driver.execute_script(f"window.scrollBy(0, 180);")
            careers_page.assert_qa_department_selected()
            careers_page.filter_by_location()
            self.logger.info("Step 3: Filtered Location with 'Istanbul' ") 
            time.sleep(5)
            action = ActionChains(self.driver) # Click empty space
            action.move_by_offset(45, 500).click().perform()
            careers_page.assert_jobs_list_exists_and_not_empty()
        except Exception as e:
            self.logger.error(f"Step 3 failed: {str(e)}")
            raise
# Step 4: Check open positions
        try:
            open_positions_page.check_job_listings()
            self.logger.info("Step 4: All job listings verified successfully")
        except Exception as e:
            self.logger.error(f"Step 4 failed: {str(e)}")
            raise
# Step 5: Check viewrole Button directs
        try:
            time.sleep(2)
            open_positions_page.check_all_view_role_buttons()
            self.logger.info("Step 5: View Role clicked and redirect verified")
        except Exception as e:
            self.logger.error(f"Step 5 failed: {str(e)}")
            raise

if __name__ == "__main__":
    unittest.main()
