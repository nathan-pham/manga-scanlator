from PIL import Image, ImageFilter
import requests
import os.path

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

filename = download_image("https://cdn-img.tonarinoyj.jp/public/page/2/3269754496293452125-862755161d18130e712ab78908d383ec")

img = Image.open(filename)
img.show()

"""
#Read image
im = Image.open( 'image.jpg' )
#Display image
im.show()

"""