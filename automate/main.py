from selenium import webdriver
import requests
import os

from automate.options import default_options
from automate.wait import wait

driver = webdriver.Chrome(
    executable_path="C:/Users/nathan-pham/python-scripts/chromedriver.exe", 
    options=default_options
)

# "https://tonarinoyj.jp/episode/3269632237330300439"

def quit_driver():
    driver.quit()

def get_json(manga_site):
    driver.get(manga_site)

    viewer_selector = "#page-viewer > section.viewer.js-viewer"
    wait(driver, viewer_selector)
    viewer = driver.find_element_by_css_selector(viewer_selector)
    manga_api = viewer.get_attribute("data-json-url").strip()

    res = requests.get(manga_api, headers={
        "content-type": "application/json",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
        "referer": manga_site,
        "origin": manga_site,
    })

    if res.status_code == 200:
        return res.json()
    else:
        return { "error": res.status_code }
