from selenium.webdriver.chrome.options import Options

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"

normal = [
    f"user-agent={user_agent}",
    "--headless", # enable to hide browser
    "--no-sandbox",
    "--disable-gpu",
    "--no-first-run",
    "--start-maximized",
    "--homepage=about:blank",
    "--ignore-certificate-errors",
    "--disable-infobars",
    "--disable-extensions",
    "--disable-dev-shm-usage",
    "--disable-popup-blocking",
    # "--user-data-dir=chrome-data",
]

experimental = {
  "prefs": { 
		"profile.default_content_setting_values.media_stream_camera": 1,
		"profile.default_content_setting_values.media_stream_mic": 1, 
		"profile.default_content_setting_values.notifications": 1,
		"profile.default_content_setting_values.geolocation": 1
	},
	"excludeSwitches": [ "enable-automation" ],
    "useAutomationExtension": False
}

default_options = Options()

for option in normal:
  default_options.add_argument(option)

for key in experimental:
  default_options.add_experimental_option(key, experimental[key])
