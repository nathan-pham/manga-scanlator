from bs4 import BeautifulSoup
import requests, os

# "https://tonarinoyj.jp/episode/3269632237330300439"

def fetch(url, _from=None):
    return requests.get(url, headers={
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
        "referer": _from,
        "origin": _from,
    })

def get_json(manga_site):
    viewer_selector = "#page-viewer > section.viewer.js-viewer"
    
    res = fetch(manga_site, manga_site)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, "html.parser")
        viewer_element = soup.select(viewer_selector)[0]
        manga_api = viewer_element.get("data-json-url").strip()

        res = fetch(manga_api)
        if res.status_code == 200:
            return res.json()

    return {}