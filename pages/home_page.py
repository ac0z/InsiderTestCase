from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

class HomePage:
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.url = "https://useinsider.com/"
        self.company_menu = (By.XPATH, "//a[@id='navbarDropdownMenuLink' and contains(text(), 'Company')]/..")
        self.careers_submenu = (By.XPATH, "//a[@href='https://useinsider.com/careers/']")
        self.accept_all = (By.XPATH, "//*[@id='wt-cli-accept-all-btn']")

    def open(self):
        try:
            self.driver.get(self.url)
            assert "Insider" in self.driver.title, "Home page not loaded"
            self.logger.info("Home page opened successfully")
        except Exception as e:
            self.logger.error(f"Failed to open home page: {str(e)}")
            raise

    def navigate_to_careers(self):
        try:
            self.click_company_menu() #company click
            self.click_careers_submenu() #submenu click
            self.click_cookies()  #cookie accept
        except Exception as e:
            self.logger.error(f"Failed to navigate to Careers page: {str(e)}")
            raise

    def click_company_menu(self):
        self._wait_and_click_element(self.company_menu, "Company menu")

    def click_careers_submenu(self):
        self._wait_and_click_element(self.careers_submenu, "Careers submenu")

    def click_cookies(self):
        self._wait_and_click_element(self.accept_all, "Cookies")

    def _wait_and_click_element(self, locator, element_name, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))
            element.click()
            self.logger.info(f"Clicked on '{element_name}' successfully")
        except Exception as e:
            self.logger.error(f"Failed to click on '{element_name}': {str(e)}")
            raise
