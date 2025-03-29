from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

BASE_DIR = Path(__file__).parent.parent
CHROME_DRIVER_NAME = 'chromedriver.exe'
CHROME_DRIVER_PATH = BASE_DIR / 'bin' / CHROME_DRIVER_NAME

def get_driver():
    service = Service(executable_path=CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service)
    return driver
