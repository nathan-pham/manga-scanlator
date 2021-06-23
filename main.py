from PIL import Image
import requests
import os.path
import math

from img_map import img_map

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

filename = download_image("https://cdn-img.tonarinoyj.jp/public/page/2/3269754496293452124-c1755e494b4f988a003964792ae268e2")

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
        y * height_increment
    ))

new_img.show()