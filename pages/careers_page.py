from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import TimeoutException
class CareersPage:

    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.locations_block = (By.ID, "career-our-location")
        self.teams_block = (By.ID, "career-find-our-calling")
        self.life_at_insider_block = (By.XPATH, "//h2[contains(text(), 'Life at Insider')]")
        self.see_all_qa_jobs_button = (By.XPATH, "//a[contains(@href, 'qualityassurance') and contains(text(), 'See all QA jobs')]")
        self.filter_by_location_element = (By.XPATH, "//*[@id='select2-filter-by-location-container']")
        self.filter_by_location_istanbul = (By.XPATH, "//option[contains(text(), 'Istanbul, Turkey')]")
        self.filter_by_department_element = (By.XPATH,"//*[@id='select2-filter-by-department-container']")
        self.filter_by_department_QA = (By.XPATH,"//*[@id='select2-filter-by-department-container'][contains(text(),'Quality Assurance')]") 
        self.qa_department_xpath = '//*[@id="select2-filter-by-department-container"][contains(text(),"Quality Assurance")]'

#Block check with assert
    def check_page_elements(self):
        assert self.driver.find_element(*self.locations_block).is_displayed(), "Locations block not found"
        self.logger.info("Locations block 'OK'")
        assert self.driver.find_element(*self.teams_block).is_displayed(), "Teams block not found"
        self.logger.info("Teams block 'OK'")
        assert self.driver.find_element(*self.life_at_insider_block).is_displayed(), "Life at Insider block not found"
        self.logger.info("Life at Insider block 'OK'")
#see all qa Jobs section

    def click_see_all_qa_jobs(self):
            self.wait_and_click_element(self.see_all_qa_jobs_button, "See all QA jobs")

    def filter_by_location(self):
            self.wait_and_click_element(self.filter_by_location_element, "Filter by Location")
            time.sleep(2)
            self.wait_and_click_element(self.filter_by_location_istanbul, "Filter Location with Istanbul")

    def filter_by_department(self):
            
            self.wait_and_click_element(self.filter_by_department_element, "Filter by Department")
            time.sleep(2)
            self.wait_and_click_element(self.filter_by_department_QA, "Filter Department with Quality Assurance")
            
    #check for QA department loads successfully after going into link.
    def assert_qa_department_selected(self):
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.qa_department_xpath))
            )
            assert element is not None, "Quality Assurance department is not selected"
            self.logger.info("Quality Assurance department is selected")
        except TimeoutException:
            self.logger.error("Quality Assurance department element not found")
            raise AssertionError("Quality Assurance department is not selected")

        except AssertionError as ae:
            self.logger.error(str(ae))
            raise
        
    def assert_jobs_list_exists_and_not_empty(self):
        try:
            # check that the jobs-list element exists
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "jobs-list"))
            )
            
            # Get the number of direct child elements under jobs-list using JavaScript
            child_count = self.driver.execute_script("""
                var jobsList = document.getElementById('jobs-list');
                return jobsList ? jobsList.children.length : 0;
            """)
            
            # Count check > 0 with assert
            assert child_count > 0, f"Jobs list is empty. Found {child_count} job items."
            
            self.logger.info(f"Jobs list found with {child_count} job items")
            return child_count
        except TimeoutException:
            self.logger.error("Jobs list element not found within the timeout period")
            raise AssertionError("Jobs list element not found")
        except AssertionError as ae:
            self.logger.error(str(ae))
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error while checking jobs list: {str(e)}")
            raise
#click element 
    def wait_and_click_element(self, locator, element_name, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))
            element.click()
            self.logger.info(f"Clicked on {element_name}")
        except Exception as e:
            self.logger.error(f"Failed to click on {element_name}: {str(e)}")
            raise
