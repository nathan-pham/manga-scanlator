from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

import requests
import time
import os

from dotenv import load_dotenv
load_dotenv()

subscription_key = os.getenv("SUBSCRIPTION_KEY")
endpoint = "https://manga-translator.cognitiveservices.azure.com/"

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

def ocr(filename):
    with open(filename, "rb") as local_image_printed_text:
        resource = computervision_client.read_in_stream(local_image_printed_text, raw=True)
        print("generating ocr resource")
        time.sleep(5)
        result_url = resource.headers.get('Operation-Location')
        result = requests.get(result_url,headers = {"Ocp-Apim-Subscription-Key":subscription_key})
        print("finished ocr for", filename)
        return result.text