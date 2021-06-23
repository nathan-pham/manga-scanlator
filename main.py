from PIL import Image, ImageDraw, ImageEnhance, ImageOps, ImageFilter
from googletrans import Translator
import requests, json, math, os
import pytesseract
import cv2

# from automate.main import get_json, quit_driver
from translate.locate_bubbles import get_blurbs
from img_map import img_map

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def download_img(url):
    filename = f"./images/{url.split('/').pop()}.jpeg"

    if os.path.isfile(filename):
        print("already downloaded", filename)
        return filename

    res = requests.get(url, stream=True)
    if res.status_code == 200:
        with open(filename, "wb") as handle:
            for chunk in res:
                handle.write(chunk)
        print("successfully downloaded", filename)
    else:
        print("failed to download", filename)
   
    return filename

def unscramble(filename, show=False, download=False):
    img = Image.open(filename)
    width, height = img.size

    height -= 20

    width_increment = math.floor(width / 4)
    height_increment = math.floor(height / 4)

    all_crops = []

    for x in range(4):
        for y in range(4):
            new_width = x * width_increment
            new_height = y * height_increment

            cropped_img = img.crop((new_width, new_height, new_width + width_increment, new_height + height_increment))
            all_crops.append((x, y, cropped_img))

    new_img = Image.new("RGB", (width, height), (255, 255, 255))


    for y, x, cropped_img in all_crops:
        new_img.paste(cropped_img, (
            x * width_increment, 
            y * height_increment # + (x * 5) # - (y * 15) # - math.floor(y * scale_factor[x] * 5)
        ))

    if show:
        new_img.show()

    if download:
        new_img.save(f"{download}/{filename.split('/').pop()}")

    return new_img

def export_pdf(in_url, out_pdf="./manga.pdf"):
    manga_json = get_json(in_url)
    quit_driver()

    pages = manga_json["readableProduct"]["pageStructure"]["pages"]
    img_list = []

    for page in pages:
        if page.get("type", "other") == "main":
            src = page.get("src")

            filename = download_img(src)
            new_img = unscramble(filename)
            
            img_list.append(new_img)

    img1 = img_list.pop(0)
    img1.save(out_pdf, save_all=True, append_images=img_list)
    print("exported pdf", out_pdf)

    return (img1, out_pdf)

# export_pdf("https://tonarinoyj.jp/episode/3269632237330300439")
# img = unscramble("./images/3269754496293452143-0104389836574dd726d44eaf904c4b1f.jpeg")
img = Image.open("./bruh.jpeg")
draw = ImageDraw.Draw(img)

with open("./format.json") as f:
    data = json.load(f)

lines = data["ParsedResults"][0]["TextOverlay"]["Lines"]
translator = Translator()

for line in lines:
    words = line["Words"]

    for word in words:
        draw.rectangle([word["Left"], word["Top"], word["Left"] + word["Width"], word["Top"] + word["Height"]], outline="red", width=5)

    translated = translator.translate(line["LineText"])
    text = translated.text
    
    draw.text([ words[0]["Left"], words[0]["Top"] ], fill="white", text=text.encode("ascii", "ignore"), stroke_width="red", stroke_fill="red")

# >>> 
# >>> translator = Translator()
# >>> translator.translate('안녕하세요.')


img.show()
"""
                        "LineText": "\u66f4\u65b0\u4e2d\u2033\u30fb",
                        "MaxHeight": 17.0,
                        "MinTop": 1082.0,
                        "Words": [
                            {
                                "Height": 16.0,
                                "Left": 29.0,
                                "Top": 1083.0,
                                "Width": 16.0,
                                "WordText": "\u66f4"
                            },
                            {
                                "Height": 16.0,
                                "Left": 46.0,
                                "Top": 1083.0,
                                "Width": 16.0,
                                "WordText": "\u65b0"
                            },
                            {
                                "Height": 17.0,
                                "Left": 63.0,
                                "Top": 1082.0,
                                "Width": 16.0,
                                "WordText": "\u4e2d"
                            },
                            {
                                "Height": 13.0,
                                "Left": 81.0,
                                "Top": 1084.0,
                                "Width": 14.0,
                                "WordText": "\u2033"
                            },
                            {
                                "Height": 3.0,
                                "Left": 95.0,
                                "Top": 1091.0,
                                "Width": 4.0,
                                "WordText": "\u30fb"
                            }
                        ]
"""