from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

import requests, base64, json, time, os

from dotenv import load_dotenv
load_dotenv()

SUBSCRIPTION_KEY = os.getenv("SUBSCRIPTION_KEY")
ENDPOINT = "https://manga-translator.cognitiveservices.azure.com/"
OCR_URL = f"https://vision.googleapis.com/v1/images:annotate?key={os.getenv("OCR_KEY")}"

computervision_client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(SUBSCRIPTION_KEY))

def ocr(filename):
    with open(filename, "rb") as local_img:
        resource = computervision_client.read_in_stream(local_img, raw=True)

        time.sleep(5)

        result_url = resource.headers.get('Operation-Location')
        result = requests.get(result_url,headers = {"Ocp-Apim-Subscription-Key":SUBSCRIPTION_KEY})
        return result.text

def build_request(content):
    return {
        "requests": [
            {
                "image": {
                    "content": content
                },
                "features": [
                    {
                        "type": "DOCUMENT_TEXT_DETECTION"
                    }
                ]
            }
        ]
    }

def hacked_ocr(filename):
    with open(filename, "rb") as f:
        content = str(base64.b64encode(f.read()).decode("ascii"))

    body = json.dumps(build_request(content))
    res = requests.post(OCR_URL, data=body, headers={
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
        "content-type": "application/json",
        "referer": "https://scanlate.io/",
        "origin": "https://scanlate.io/",
    })

    return res.json()

with open("./format.json", "w") as f:
    f.write(json.dumps(hacked_ocr("./bruh.jpeg"), indent=4, sort_keys=True))
