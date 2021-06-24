from PIL import Image, ImageDraw, ImageEnhance, ImageOps, ImageFont, ImageFilter
import requests, json, math, os
import pytesseract
import cv2

from ocr import ocr, hacked_ocr, get_blocks, make_all_bubbles
from automate import get_json

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
font = ImageFont.truetype("arial", 16)

def text_wrap(text, draw, max_width, max_height, font=font):
    lines = [[]]
    words = text.split()
    for word in words:
        # try putting this word in last line then measure
        lines[-1].append(word)
        (w,h) = draw.multiline_textsize('\n'.join([' '.join(line) for line in lines]), font=font)
        if w > max_width: # too wide
            # take it back out, put it on the next line, then measure again
            lines.append([lines[-1].pop()])
            (w,h) = draw.multiline_textsize('\n'.join([' '.join(line) for line in lines]), font=font)
            if h > max_height: # too high now, cannot fit this word in, so take out - add ellipses
                lines.pop()
                # try adding ellipses to last word fitting (i.e. without a space)
                lines[-1][-1] += '...'
                # keep checking that this doesn't make the textbox too wide, 
                # if so, cycle through previous words until the ellipses can fit
                while draw.multiline_textsize('\n'.join([' '.join(line) for line in lines]),font=font)[0] > max_width:
                    lines[-1].pop()
                    lines[-1][-1] += '...'
                break
    return '\n'.join([' '.join(line) for line in lines])


def purge_imgs(mydir="./images"):
    for f in os.listdir(mydir):
        os.remove(os.path.join(mydir, f))

def download_img(url):
    filename = f"./images/{url.split('/').pop()}.jpeg"

    if os.path.isfile(filename):
        return filename

    res = requests.get(url, stream=True)
    if res.status_code == 200:
        with open(filename, "wb") as handle:
            for chunk in res:
                handle.write(chunk)
   
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
    data = ocr(filename)
    content = hacked_ocr(filename)

    try:
        lines = data["analyzeResult"]["readResults"][0]["lines"]
    except:
        lines = []

    draw = ImageDraw.Draw(img)
    blocks = get_blocks(content)
    bubbles = make_all_bubbles(blocks)

    bboxes = [bubble[1][2] * bubble[1][3] for bubble in bubbles]
    max_area = max(bboxes)
    min_area = min(bboxes)

    print(max_area, min_area)
    
    for line in lines:
        bbox, text = line["boundingBox"], line["text"]
        new_bbox = []

        for i in range(len(bbox)):
            if i % 2 == 0:
                new_bbox.append((bbox[i], bbox[i + 1]))

        rect_coords = (new_bbox[0] + new_bbox[-2])
        x1, y1, x2, y2 = rect_coords
        area = (x2 - x1) * (y2 - y1)
        if area < max_area and area > min_area:
            draw.rectangle(rect_coords, fill=(255, 255, 255))

    for english, bbox in bubbles:
        x, y, width, height = bbox
        wrapped = text_wrap(english, draw, width, height)
        draw.text((x, y), wrapped, font=font, fill=(0, 0, 0))
    return img

def export_pdf(in_url, start_end=None):
    out_pdf = f"{in_url.split('/').pop()}.pdf"

    purge_imgs()
    manga_json = get_json(in_url)

    pages = manga_json["readableProduct"]["pageStructure"]["pages"]
    pages = list(filter(lambda page: page.get("type", "other") == "main", pages))
    img_list = []

    if start_end is not None:
        start, end = start_end
        pages = pages[start:end]

    for i in range(len((pages))):
        page = pages[i]
        print(f"page: {i + 1}/{len(pages)}")
        if page.get("type", "other") == "main":            
            src = page.get("src")

            filename = download_img(src)
            new_img = unscramble(filename, download=True)
            img_list.append(convert(filename, new_img))

    img1 = img_list.pop(0)
    img1.save(out_pdf, save_all=True, append_images=img_list)
    return out_pdf

export_pdf("https://tonarinoyj.jp/episode/3269632237330300439", (1, 2))