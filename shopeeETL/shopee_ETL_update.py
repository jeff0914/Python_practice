import requests
import json
import pandas as pd
import time
from seleniumwire import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import re
import random
import zlib
from bs4 import BeautifulSoup
#------------------------------------------------------------------------
User_Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
my_headers = {
    'user-agent': User_Agent,
    'af-ac-enc-dat': 'AAcyLjQuMS0yAAABhEYD7joAAAjHAcEAAAAAAAAAAOYyhFB7rjob26/8rq6jA0F3J6Kfg5aGEX+GYncix7fIyPghAefe3JS894jq/3nC9cJjpEn32HTqasIUhFkInWzoCOj1uSC5kl6LU06aSrm61kX/Ny1L5jzxFjDrS1IzPHwt9muZUbatRPTf42k24UXHBZsir4fwWxQLVKw5gDu5CyybpSVWFCd7OLsY30Hj1OjSKZvDNTpkAhYqvdOyLCTGr41kHyFGV3ZaoQ01NX1u6R9AnBG6X9s1ynZK6vnTBgzBIOKTNFS4j1VT8sOl1BEtObri8ZUW3OTOHeCO4vGDCq4gRJFmvwSm1BNdccjxAekgEx3xwroP6ZL6LO5bh9QSxuKGYkUmR84CcHLB6dmMPnXDUGkagca9MFiK8RmRsrN2vcLDNTpkAhYqvdOyLCTGr41kKUmjTinalW5/ctjHa7Lte+06J5ekdC078Iv4wrMjrvbzUjYNqi2Hdu8tLPGrNL/jmEfixe8rpESf8+9J+WOK8kusILDBjMDq/xa+8hI9GWbdxIdVmB5payUD+EtCC4BUkWOzjLDykZY2dhCO2aemlpFjs4yw8pGWNnYQjtmnppZDbeO6witi5K5LrYrVnhWzWCX7lKDZYje5tgIJeETgYw==',
}
#------------------------------------------------------------------------
#key in username/password
username=''
password=''
keyword = "七變化虎耳草"
ecode = 'utf-8-sig'
page = 1
#------------------------------------------------------------------------
service = ChromeService(executable_path=ChromeDriverManager().install())
options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
options.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(service=service, chrome_options=options)
time.sleep(random.randint(10, 20))
#------------------------------------------------------------------------
driver.get('https://shopee.tw/search?keyword=' + keyword )
time.sleep(random.randint(10,20))
#------------------------------------------------------------------------
driver.find_element(By.CSS_SELECTOR, 'input[name="loginKey"]').send_keys(username)
time.sleep(2)
driver.find_element(By.CSS_SELECTOR, 'input[name="password"]').send_keys(password)
time.sleep(3)
driver.find_element(by=By.XPATH, value='//*[@id="main"]/div/div[2]/div/div/div/div[2]/form/div/div[2]/button').click()
time.sleep(3) 
#------------------------------------------------------------------------
print('---------- 開始進行爬蟲 ----------')
tStart = time.time()
#------------------------------------------------------------------------
plants=['七變化虎耳草','大西瓜皮椒草','大麻葉花燭','小西瓜皮椒草','白斑合果芋','白斑姑婆芋','白斑龜背芋','明脈火鶴','油畫竹芋','紅玉椒草','姬龜背芋','斑葉心葉蔓綠絨','斑葉白鶴芋','斑葉豹紋竹芋','絨葉蔓綠絨','黑合果芋','黑頂卷柏','瑞士起司窗孔龜背芋','銅鏡觀音蓮','斑葉獨角獸蔓綠絨','飄帶火鶴','灑金蔓綠絨']
for plant in plants:
    keyword = plant
    itemid = []
    shopid =[]
    name = []
    link = []
    price = []
    historical_sold = []
    plant_type = []
    for i in range(int(page)):
        driver.get('https://shopee.tw/search?keyword=' + keyword + '&page=' + str(i))
        time.sleep(random.randint(5,10))

        for scroll in range(6):
            driver.execute_script('window.scrollBy(0,1000)')
            time.sleep(random.randint(10,15))

        # 取得商品內容
        for block in driver.find_elements(by=By.XPATH, value='//*[@data-sqe="item"]'):
            soup = BeautifulSoup(block.get_attribute('innerHTML'), "html.parser").find('a')
            getID = item.get_attribute('href')
            theitemid = int((getID[getID.rfind('.')+1:getID.rfind('?')]))
            theshopid = int(getID[ getID[:getID.rfind('.')].rfind('.')+1 :getID.rfind('.')]) 
            # 先整理標籤
            get_parent = soup.find('div',{"data-sqe":"name"}).parent.find_all("div", recursive=False)
            # 商品名稱
            if len(get_parent) >0: 
                getname = get_parent[0].find('div').text
            else:
                print('抓不到資料，直接是空的')
                continue # 沒抓到這個商品就別爬了
            #價格
            if len(get_parent) >1: # 確認有資料再進行
                getSpan = get_parent[1].find_all('span')
                counter = []
                for j in getSpan:
                    theprice = j.text
                    theprice = theprice.replace('萬','')
                    theprice = theprice.replace('$','')
                    theprice = theprice.replace(',','')
                    theprice = theprice.replace(' ','')

                    if theprice != '':
                        counter.append(int(theprice))

                # 到這邊確認都有抓到資料，才將它塞入陣列，否則可能會有缺漏
                link.append("https://shopee.tw"+getID)
                itemid.append(theitemid)
                shopid.append(theshopid)
                name.append(getname)
                price.append(sum(counter)/len(counter))
                plant_type.append(plant)
            else:
                print('抓不到價格資料')

            # 取得已售出
        get_historical_sold = driver.find_elements(By.CSS_SELECTOR, "div.r6HknA")
        for element in get_historical_sold:
            content = element.text
            if content == "":
                historical_sold.append(0)
                print(0)
            else:
                regex_pattern = r"已售出\D*(\d{1,3}(?:,\d{3})*|\d+)"
                match = re.search(regex_pattern, content)
                if match:
                    historical_sold_value = int(match.group(1).replace(",", ""))
                    historical_sold.append(historical_sold_value)
                    print(historical_sold_value)
                else:
                    historical_sold.append(0)
                    print(0)


        time.sleep(random.randint(20,30)) # 休息久一點

    dic = {
        '商品ID':itemid,
        '賣家ID':shopid,
        '商品名稱':name,
        '商品連結':link,
        '價格':price,
        '歷史銷售量': historical_sold ,
        '植物種類': plant_type
    }
    max_length = max([len(v) for v in dic.values()])
    for key, value in dic.items():
        if len(value) < max_length:
            dic[key] = value + [None] * (max_length - len(value))
    pd.DataFrame(dic).to_csv(keyword +'_商品資料.csv', encoding = ecode, index=False)

    tEnd = time.time()#計時結束
    totalTime = int(tEnd - tStart)
    minute = totalTime // 60
    second = totalTime % 60
    print('資料儲存完成，花費時間（約）： ' + str(minute) + ' 分 ' + str(second) + '秒')

#------------------------------------------------------------------------
tEnd = time.time()#計時結束
totalTime = int(tEnd - tStart)
minute = totalTime // 60
second = totalTime % 60
print('資料儲存完成，花費時間（約）： ' + str(minute) + ' 分 ' + str(second) + '秒')
#------------------------------------------------------------------------
driver.close() 