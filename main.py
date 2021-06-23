from PIL import Image, ImageDraw, ImageEnhance, ImageOps
import requests
import os.path
import math

from img_map import img_map

from pytesseract import Output
import pytesseract

pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"

def download_image(url):
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

filename = download_image("https://cdn-img.tonarinoyj.jp/public/page/2/3269754496293452127-931794360661b9e06fda46569bfa49ae")
new_img = unscramble(filename) # "./images/exports"
gray_img = ImageOps.grayscale(new_img)

boxes = pytesseract.image_to_boxes(gray_img, "jpn").strip().split('\n')
draw = ImageDraw.Draw(new_img)

for box in boxes:
    char, left, bottom, right, top, page = box.split(' ')
    print(box)
    draw.rectangle([int(left), int(top), int(right), int(bottom)], outline="red", width=5)
# {'char': ['~'], 'left': [0], 'bottom': [0], 'right': [800], 'top': [1122], 'page': [0]}
    # (x, y, w, h) = (boxes['left'][i], boxes['top'][i], boxes['width'][i], boxes['height'][i])
    # draw.rectangle([x, y, x + w, y + h], outline=(0, 0, 0), width=5)

new_img.show()    

"""


  segmented_image = seg.segment_image(gray)
  segmented_image = segmented_image[:,:,2]
  components = cc.get_connected_components(segmented_image)
  cc.draw_bounding_boxes(img,components,color=(255,0,0),line_size=2)


# run tesseract, returning the bounding boxes
boxes = pytesseract.image_to_boxes(img) # also include any config options you use

# draw the bounding boxes on the image
for b in boxes.splitlines():
    b = b.split(' ')
    img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)

# show annotated image and wait for keypress
cv2.imshow(filename, img)
cv2.waitKey(0)

"""

"""
select(#page-viewer > section.viewer.js-viewer)

url = getAttribute(data-json-url)
fetch(url)

"""