from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager

def get_driver():
    service = Service(r"./driver/chromedriver.exe")
    return webdriver.Chrome(service=service)