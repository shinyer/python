from aip import AipOcr
import pprint
import numpy as np
import requests
import json
from PIL import Image,ImageDraw,ImageFont

""" 你的 APPID AK SK """
APP_ID = '27224528'
API_KEY = 'YOUR APIKEY'
SECRET_KEY = 'YOUR SECRET KEY'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
""" 读取文件 """
def get_file_content(filePath):
    with open(filePath, "rb") as fp:
        return fp.read()

in_img = input("请输入要翻译的图片名称(完整图片格式):>") #例:test.jpg
out_img = input("请输入保存名称(完整图片格式):>") #例:test.jpg
image1 = get_file_content(in_img) # 需要输入图片名字

res_image = client.accurate(image1)
# res_image = {'words_result': [{'words': '泰车团', 'location': {'top': 25, 'left': 86, 'width': 138, 'height': 20}}, {'words': '保价30天', 'location': {'top': 7, 'left': 540, 'width': 206, 'height': 53}}, {'words': 'TITAN ARMY', 'location': {'top': 48, 'left': 86, 'width': 138, 'height': 12}}, {'words': '2K144HzY火力宝开', 'location': {'top': 112, 'left': 31, 'width': 691, 'height': 87}}, {'words': '150R电竞曲面', 'location': {'top': 206, 'left': 317, 'width': 394, 'height': 48}}, {'words': 'TITAN ARMY', 'location': {'top': 656, 'left': 339, 'width': 80, 'height': 18}}, {'words': '现货速发', 'location': {'top': 859, 'left': 17, 'width': 168, 'height': 43}}, {'words': '6期免息赠24H碎屏险', 'location': {'top': 889, 'left': 295, 'width': 416, 'height': 39}}, {'words': '￥', 'location': {'top': 955, 'left': 8, 'width': 17, 'height': 24}}, {'words': '999', 'location': {'top': 916, 'left': 48, 'width': 149, 'height': 71}}, {'words': '限时赠炫光键鼠套装', 'location': {'top': 944, 'left': 273, 'width': 468, 'height': 47}}], 'words_result_num': 11, 'log_id': 1564544295485200030}

image = Image.open(in_img)  # 需要输入图片名字
img_draw = ImageDraw.Draw(image)
print("图像大小:"+str(image.size))
img_font = ImageFont.truetype("~/资源库/Fonts/STHeiti Light.ttc",size=36)
# y轴
def fun_top():
    top_list = []
    s = len(res_image['words_result'])
    for i in range(0,s):
        location = res_image['words_result'][i]
        get_local = location.get('location')
        top = int(get_local.get('top'))
        top_list.append(top)
    return top_list

# x轴
def fun_left():
    left_list = []
    s = len(res_image['words_result'])
    for i in range(0, s):
        location = res_image['words_result'][i]
        get_local = location.get('location')
        left = int(get_local.get('left'))
        left_list.append(left)
    return left_list

def fun_width():
    width_list = []
    s = len(res_image['words_result'])
    for i in range(0, s):
        location = res_image['words_result'][i]
        get_local = location.get('location')
        width = int(get_local.get('width'))
        width_list.append(width)
    return width_list

def fun_height():
    height_list = []
    s = len(res_image['words_result'])
    for i in range(0, s):
        location = res_image['words_result'][i]
        get_local = location.get('location')
        height = int(get_local.get('height'))
        height_list.append(height)
    return height_list

def translate(word):
    # 有道词典 api
    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null'
    # 传输的参数，其中 i 为需要翻译的内容
    key = {
        'type': "AUTO",
        'i': word,
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "ue": "UTF-8",
        "action": "FY_BY_CLICKBUTTON",
        "typoResult": "true"
    }
    # key 这个字典为发送给有道词典服务器的内容
    response = requests.post(url, data=key)
    # 判断服务器是否相应成功
    if response.status_code == 200:
        # 然后相应的结果
        return response.text
    else:
        print("有道词典调用失败")
        # 相应失败就返回空
        return None

def get_main(word):
    list_trans = translate(word)
    result = json.loads(list_trans)
    result = result['translateResult'][0][0]['tgt']
    return result

def get_text():
    text_list = []
    for i in res_image['words_result']:
        # print(i['words'])
        text_list.append(get_main(i['words']))
    return text_list

top = fun_top()
left = fun_left()
width = fun_width()
height = fun_height()

text = get_text()
#print(text)
count = 0
for i in range(0,len(top)):
    x1 = left[i]
    y1 = top[i]
    txt = text[i]
    back_color = image.getpixel((x1-3,y1-3))  # 取某一点的RGB值(top-5,left-5)
    font_color = image.getpixel((x1+3,y1+3))  # 取字体颜色
    count = count + 1
    print(str(count) + "背景颜色:" + str(back_color) + txt)
    # print(str(count) + "字体颜色:" + str(font_color))
    img_draw.rectangle((x1,y1,x1+width[i],y1+height[i]),fill=back_color) # 画矩形
    img_draw.text((x1,y1),txt,fill=(255,255,255),font=img_font)

image.save(out_img)
print("已保存")

# 背景颜色:(73, 34, 151)
# 字体颜色:(70, 37, 154)
