from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
from translatepy import Translator
from dotenv import load_dotenv

import requests, base64, json, time, os

load_dotenv()

SUBSCRIPTION_KEY = os.getenv("SUBSCRIPTION_KEY")
ENDPOINT = "https://manga-translator.cognitiveservices.azure.com/"
OCR_URL = f"https://vision.googleapis.com/v1/images:annotate?key={os.getenv('OCR_KEY')}"
translator = Translator()

computervision_client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(SUBSCRIPTION_KEY))

def ocr(filename):
    with open(filename, "rb") as local_img:
        resource = computervision_client.read_in_stream(local_img, raw=True)

        time.sleep(5)

        result_url = resource.headers.get('Operation-Location')
        result = requests.get(result_url,headers = {"Ocp-Apim-Subscription-Key":SUBSCRIPTION_KEY})
        return result.json()

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

def rect(bbox):
    def helper(axis, func):
        result = bbox["vertices"][0][axis]

        for i in range(1, 4):
            current = bbox["vertices"][i][axis]
            result = func(result, current)

        return result
    
    min_x = helper('x', min)
    min_y = helper('y', min)
    max_x = helper('x', max)
    max_y = helper('y', max)

    return min_x - 20, min_y, max_x - min_x + 40, max_y - min_y

def extract_text(block):
    result = ""

    for paragraph in block["paragraphs"]:
        for word in paragraph["words"]:
            for symbol in word["symbols"]:
                result += symbol["text"]

    return result

def get_blocks(res):
    return res["responses"][0]["fullTextAnnotation"]["pages"][0]["blocks"]

def translate(japanese):
    return str(translator.translate(japanese, "English"))

def make_all_bubbles(blocks):
    bubbles = []

    for block in blocks:
        _rect = rect(block["boundingBox"])
        japanese = extract_text(block)
        english = translate(japanese)
        bubbles.append((english, _rect))

    return bubbles

# with open("./format", "w") as f:
#     f.write(json.dumps(hacked_ocr("./bruh.jpeg"), indent=4, sort_keys=True))

# with open("./format.json", "r") as f:
#     content = json.loads(f.read())

#     blocks = get_blocks(content)
#     bubbles = make_all_bubbles(blocks)

#     print(json.dumps(bubbles, indent=4, sort_keys=True))

"""
    x: bubble.rect.x + bubble.rect.width / 2,
    y: bubble.rect.y + bubble.rect.height / 2,
    width: bubble.rect.width,
    height: bubble.rect.height,

"""