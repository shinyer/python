import pytesseract
from PIL import Image
import requests

url = 'https://pmd5.com/'
req = requests.get(url)
res = req.content
print(res)


image = Image.open('下载.jpeg')
code = pytesseract.image_to_string(image)
print(code)