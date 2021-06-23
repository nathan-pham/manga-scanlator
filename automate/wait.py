from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def wait(driver, element):
    timeout = 3

    try:
        element_present = EC.presence_of_element_located((By.CSS_SELECTOR, element))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print("timed out, page took to long to load")
    finally:
        print("page loaded")