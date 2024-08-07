from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException


class OpenPositionsPage:
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger

    def check_job_listings(self):
        try:
            # Find the jobs-list element
            jobs_list = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "jobs-list"))
            )
            
            # Find all job listings
            job_items = jobs_list.find_elements(By.XPATH, "./div")  # Direct child divs of jobs-list
            
            if not job_items:
                raise AssertionError("No job listings found")
            
            for index, job in enumerate(job_items, start=1):
                try:
                    # Extract required information for each job listing
                    position = job.find_element(By.XPATH, "//*[@class='position-title font-weight-bold']").text 
                    department = job.find_element(By.XPATH, "//*[@class='position-department text-large font-weight-600 text-primary']").text
                    location = job.find_element(By.XPATH, "//*[@class='position-location text-large']").text

                    # Perform necessary checks
                    assert "Quality Assurance" in position, f"Job {index}: Position does not contain 'Quality Assurance'"
                    assert department == "Quality Assurance", f"Job {index}: Department is not 'Quality Assurance'"
                    assert "Istanbul, Turkey" in location, f"Job {index}: Location does not contain 'Istanbul, Turkey'"
                    
                    self.logger.info(f"Job {index} verified successfully")
                except AssertionError as ae:
                    self.logger.error(str(ae))
                    raise
                except NoSuchElementException:
                    self.logger.error(f"Job {index}: Required information not found")
                    raise AssertionError(f"Job {index}: Required information not found")
            
            self.logger.info(f"All {len(job_items)} job listings verified successfully")
        except TimeoutException:
            self.logger.error("Jobs list element not found within the timeout period")
            raise AssertionError("Jobs list element not found")
        except Exception as e:
            self.logger.error(f"Unexpected error while checking job listings: {str(e)}")
            raise   

    def check_all_view_role_buttons(self):
        try:
            # Find all job list items
            job_items = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//*[@class='position-list-item-wrapper bg-light']"))
            )
            
            self.logger.info(f"Found {len(job_items)} job items")

            for index, job_item in enumerate(job_items, start=1):
                # Scroll the job item into view
                self.driver.execute_script("arguments[0].scrollIntoView(true);", job_item)
                
                # Hover over the job item
                ActionChains(self.driver).move_to_element(job_item).perform()
                self.logger.info(f"Hovered over job item {index}")

                # Find and click the "View Role" button within this job item
                view_role_button = WebDriverWait(job_item, 10).until(
                    EC.element_to_be_clickable((By.XPATH, ".//a[contains(@class, 'btn-navy') and contains(text(), 'View Role')]"))
                )

                original_window = self.driver.current_window_handle
                view_role_button.click()
                self.logger.info(f"Clicked 'View Role' button for job {index}")

                # Wait for the new window/tab to open and switch to it
                WebDriverWait(self.driver, 10).until(EC.number_of_windows_to_be(2))
                for window_handle in self.driver.window_handles:
                    if window_handle != original_window:
                        self.driver.switch_to.window(window_handle)
                        break

                # Wait for and verify the Lever Application form URL
                WebDriverWait(self.driver, 10).until(EC.url_contains("jobs.lever.co"))
                assert "jobs.lever.co" in self.driver.current_url, f"Job {index}: Not redirected to Lever Application form"
                self.logger.info(f"Job {index}: Successfully redirected to Lever Application form")

                # Close the new tab and switch back to the original window
                self.driver.close()
                self.driver.switch_to.window(original_window)

            self.logger.info("All 'View Role' buttons checked successfully")

        except TimeoutException:
            self.logger.error("Job items or 'View Role' buttons not found")
            raise
        except ElementNotInteractableException:
            self.logger.error(f"'View Role' button for job {index} is not interactable")
            raise
        except AssertionError as ae:
            self.logger.error(str(ae))
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error while checking 'View Role' buttons: {str(e)}")
            raise