import requests
import lxml.html

etree = lxml.html.etree

# print(response)

url = 'http://book.zongheng.com/showchapter/1028154.html'
req = requests.get(url)
res = req.encoding = 'utf-8'
res = etree.HTML(req.content.decode())
# print(res)

s_list = res.xpath('//div[@class="container"]/div/div[@class="volume-list"]/div/div/a/@href')  # 图片链接
print(s_list)
p_list = res.xpath('//div[@class="container"]/div/div[@class="volume-list"]/div/ul/li/a/text()')  # 图片名称
print(p_list)

