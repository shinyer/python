## ********************************** 第一步：抓取该平台二手车的所有品牌 **********************************
# 导入第三方包
import requests
from bs4 import BeautifulSoup
import time

# 设置伪头
headers = {
    'Accept':'*/*',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Connection':'keep-alive',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36 SE 2.X MetaSr 1.0'
}


# 二手车主页的链接
url = 'https://changsha.taoche.com/all/'
# 发出抓取链接的请求并进一步解析
res = requests.get(url, headers = headers).text
soup = BeautifulSoup(res,'html.parser')

# 抓取二手车品牌名称及对应的链接
car_brands = soup.find('div',{'class':'li_main clearfix'}).find_all('li')
car_brands = [j for i in car_brands for j in i]
car_brands = car_brands[41:]
brands = [i for i in car_brands]
brands = [i.text for i in car_brands]
urls = ['https://changsha.taoche.com' + i['href'] for i in car_brands]


print(urls)
## ********************************** 第二步：抓取该平台二手车的目标链接 **********************************
# 生成所需抓取的目标链接
target_urls = []
target_brands = []

for b,u in zip(brands,urls):
    # 抓取各品牌二手车主页下的所有页码
    
    res = requests.get(u, headers = headers).text
    soup = BeautifulSoup(res,'html.parser')

    # 查询出页数
    if len(soup.findAll('div',{'class':'paging-box the-pages'})) == 0:
        pages = 1
    else:
        pages = int([page.text for page in soup.findAll('div',{'class':'paging-box the-pages'})[0].findAll('a')][-2])
    time.sleep(0)
 


#问题段落。
    uu = u
    page_num = pages
    print(page_num)
    for i in range(1,page_num):
        target_brands.append(b)
        print(target_brands)
        try:
            target_urls.append(u+'?page='+str(i)+'#pagetag')
            print(u)
            infos=soup.find('ul',{'class':'gongge_ul'}).find_all('li')
        except AttributeError:
            print('当前页空白')
        print(target_urls)





        ## ********************************** 第三步：对该平台的二手车信息进行采集 **********************************        
        # 构建空列表，用于数据的存储
        brand = []
        title = []
        boarding_time = []
        km = []
        discharge = []
        sec_price = []
        new_price = []

        # 对每个链接发生请求
        for b,u in zip(target_brands,target_urls):
            res = requests.get(u, headers = headers).text
            soup = BeautifulSoup(res,'html.parser')
            # 每页车子的数量
            N = len([i.findAll('a')[0]['title'] for i in soup.findAll('div',{'class':'gongge_main'})])
            print(N)

            try:
                # 车品牌
                brands = (b+'-')*N
                brand.extend(brands.split('-')[:-1])
                # 车名称
                title.extend([i.findAll('a')[0]['title'] for i in soup.findAll('div',{'class':'gongge_main'})])
                # 二手车的上牌时间、行驶里程数等信息
                info = [i.findAll('li') for i in soup.findAll('ul',{'class':'gongge_ul'})]
                boarding_time.extend([i[0].text[4:] for i in info])
                km.extend([i[1].text[4:] for i in info])
                discharge.extend([i[3].text[4:] for i in info])
                sec_price.extend([float(i.findAll('h2')[0].text[:-1]) for i in soup.findAll('div',{'class':'gongge_main'})])
                new_price.extend([i.findAll('p')[0].text.split('\xa0')[0][5:].strip() for i in soup.findAll('div',{'class':'gongge_main'})])
            except IndexError:
                pass
            # 每3秒停顿一次
            time.sleep(0)

            
        ## ********************************** 第四步：将采集来的数据进行存储 **********************************      
        # 数据导出
        import pandas as pd
        cars_info = pd.DataFrame([brand,title,boarding_time,km,discharge,sec_price,new_price]).T
        cars_info = cars_info.rename(columns={0:'Brand',1:'Name',2:'Boarding_time',3:'Km',4:'Discharge',5:'Sec_price',6:'New_price'})
        cars_info.to_csv('second_cars_info.csv', index=False)
