from PIL import Image, ImageDraw, ImageEnhance, ImageOps, ImageFont, ImageFilter
from translatepy import Translator
import requests, json, math, os
import pytesseract
import cv2

from automate import get_json
from ocr import ocr

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
translator = Translator()

font = ImageFont.truetype("arial", 12)

def wrap_text(text, font=font, line_length=100):
    lines = ['']
    for word in text.split():
        line = f'{lines[-1]} {word}'.strip()
        if font.getlength(text) <= line_length:
            lines[-1] = line
        else:
            lines.append(word)
    return '\n'.join(lines)

def purge_imgs(mydir="./images"):
    for f in os.listdir(mydir):
        os.remove(os.path.join(mydir, f))

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
        new_img.save(filename)

    return new_img

def convert(filename, img):
    data = json.loads(ocr(filename))

    try:
        lines = data["analyzeResult"]["readResults"][0]["lines"]
    except:
        print("failed ocr for", filename)
        lines = []

    draw = ImageDraw.Draw(img)

    texts = []
    for line in lines:
        bbox, text = line["boundingBox"], line["text"]
        new_bbox = []

        for i in range(len(bbox)):
            if i % 2 == 0:
                new_bbox.append((bbox[i], bbox[i + 1]))    

        draw.rectangle((new_bbox[0] + new_bbox[-2]), fill=(255, 255, 255))

        translated = str(translator.translate(text, "English"))
        texts.append((new_bbox[1], wrap_text(translated)))

    for xy, text in texts:
        draw.text(xy, text, (255, 0, 0), font=font, spacing=-1)

    return img

def export_pdf(in_url, start_end=None):
    out_pdf = f"{in_url.split('/').pop()}.pdf"

    purge_imgs()
    print("purged images")
    
    manga_json = get_json(in_url)
    print("retrieved manga api")

    pages = manga_json["readableProduct"]["pageStructure"]["pages"]
    if start_end is not None:
        start, end = start_end
        pages = pages[start:end]

    img_list = []

    print(len(pages), "pages")

    for page in pages:
        if page.get("type", "other") == "main":            
            src = page.get("src")

            filename = download_img(src)
            new_img = unscramble(filename, download=True)
            print("rewrote with unscrambled file")

            img_list.append(convert(filename, new_img))

    img1 = img_list.pop(0)
    
    img1.save(out_pdf, save_all=True, append_images=img_list)
    print("exported pdf", out_pdf)
    return out_pdf

export_pdf("https://tonarinoyj.jp/episode/3269754496359036797")