import requests
import json

def ocr_space_file(filename, overlay=True, api_key='helloworld', language='eng'):
    """ OCR.space API request with local file.
        Python3.5 - not tested on 2.7
    :param filename: Your file path & name.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )
    return r.content.decode()


# Use examples:
r = ocr_space_file(filename='bruh.jpeg', language='jpn')
parsed = json.loads(r)
print(json.dumps(parsed, indent=4, sort_keys=True))
# print(parsed['ParsedResults'][0]['ParsedText'])

# with open("./bruh-2.jpeg", "wb") as handle:
#     for chunk in r:
#         handle.write(chunk)

# test_url = ocr_space_url(url='http://i.imgur.com/31d5L5y.jpg')