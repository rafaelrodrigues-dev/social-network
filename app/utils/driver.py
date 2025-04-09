from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

BASE_DIR = Path(__file__).parent.parent
CHROME_DRIVER_NAME = 'chromedriver.exe'
CHROME_DRIVER_PATH = BASE_DIR / 'bin' / CHROME_DRIVER_NAME

def get_driver():
    options = Options()
    options.add_argument('--lang=en-US')
    service = Service(executable_path=CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service,options=options)
    return driver
