from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time

from dotenv import load_dotenv
load_dotenv()

subscription_key = os.getenv("SUBSCRIPTION_KEY")
endpoint = "https://manga-translator.cognitiveservices.azure.com/"

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

def ocr(filename):
    with open(filename, "rb") as local_image_printed_text:
        results = computervision_client.read_in_stream(local_image_printed_text, raw=True)
    return results