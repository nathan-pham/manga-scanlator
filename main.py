from PIL import Image, ImageDraw, ImageEnhance, ImageOps, ImageFilter
import requests, json, math, os
import pytesseract

from automate.main import get_json, quit_driver
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
        # nx = math.floor(y / height_increment)
        # ny = math.floor(x / width_increment)
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
img = unscramble("./images/3269754496293452143-0104389836574dd726d44eaf904c4b1f.jpeg")
img = img.convert('L').filter(ImageFilter.MedianFilter()).point(lambda x : 0 if x < 140 else 255)
img.show()

boxes = pytesseract.image_to_boxes(img, "jpn").strip().split('\n')

"""
import sys
IMAGE_PATH = sys.argv[1]

# open image
im = Image.open(IMAGE_PATH)

# preprocessing
im = im.convert('L')                             # grayscale
im = im.filter(ImageFilter.MedianFilter())       # a little blur
im = im.point(lambda x: 0 if x < 140 else 255)   # threshold (binarize)

text = pytesseract.image_to_string(im)           # pass preprocessed image to tesseract
print(text)                
"""