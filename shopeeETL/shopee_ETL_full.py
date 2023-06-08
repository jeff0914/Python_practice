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
from tqdm import tqdm
import zlib
#-------------------------------------------------------------------
User_Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
my_headers = {
    'user-agent': User_Agent,
    'af-ac-enc-dat': 'AAcyLjQuMS0yAAABhEYD7joAAAjHAcEAAAAAAAAAAOYyhFB7rjob26/8rq6jA0F3J6Kfg5aGEX+GYncix7fIyPghAefe3JS894jq/3nC9cJjpEn32HTqasIUhFkInWzoCOj1uSC5kl6LU06aSrm61kX/Ny1L5jzxFjDrS1IzPHwt9muZUbatRPTf42k24UXHBZsir4fwWxQLVKw5gDu5CyybpSVWFCd7OLsY30Hj1OjSKZvDNTpkAhYqvdOyLCTGr41kHyFGV3ZaoQ01NX1u6R9AnBG6X9s1ynZK6vnTBgzBIOKTNFS4j1VT8sOl1BEtObri8ZUW3OTOHeCO4vGDCq4gRJFmvwSm1BNdccjxAekgEx3xwroP6ZL6LO5bh9QSxuKGYkUmR84CcHLB6dmMPnXDUGkagca9MFiK8RmRsrN2vcLDNTpkAhYqvdOyLCTGr41kKUmjTinalW5/ctjHa7Lte+06J5ekdC078Iv4wrMjrvbzUjYNqi2Hdu8tLPGrNL/jmEfixe8rpESf8+9J+WOK8kusILDBjMDq/xa+8hI9GWbdxIdVmB5payUD+EtCC4BUkWOzjLDykZY2dhCO2aemlpFjs4yw8pGWNnYQjtmnppZDbeO6witi5K5LrYrVnhWzWCX7lKDZYje5tgIJeETgYw==',
    'Accept': 'application/json',
    'X-API-SOURCE': 'pc',
    'X-Requested-With': 'X',
    'X-CSRFToken': 'IDq3287GJnXS5JJj5c2p5NfuvByGNpst',
    'sz-token': 'Ra/NJSFhMbpYXlWXB/kMKw==|tbtAeRuQraLaHXP0PPLER62V4RREUxTHlM0sHpOnYMwbMMQeM9+qLgkomlUGpUVkjby5btMmGHCl9DFdTYOavUNJ3LuXv0sobg==|oZGZsgOMDe5oaMrE|06|3',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Cookie': 'SPC_EC=eWVuVzdSMU10OGFHb1QzV2r5/vvLeTNvDDk2AVnFbPKB2gmfMPe5xvZ7NC81wUIC8vKKgoTpt9skOsCk1GO0keSXJKYLjIyLqe8X/29ILr4P81AUXvQS47ckylZx/FY+HgktG2GoRotjwTZqy0N/Z/JBNtDB4bP/+BysNRDZebk=; REC_T_ID=206a7062-d446-11ed-a75f-f4ee081d8fa9; SPC_SI=tTljZAAAAABvaHFpWlRwcsy1sQAAAAAAT3ZNWGx3YUQ=; SPC_U=32201823; SPC_R_T_ID=zth6DF58mGimc15AQ/5CfCexpv5ZrgMY1HlamI+vCDJvoXF8QABjWaVClfZQ8DPfpFN+JgnIJWGJB2dD3mvNxH7bCfGkFSNe12kGYJHakcrsfFIUih37vW9sXT5XjrOu9qTC8+k0Qb4EKwHPqa25FYe4t2KNiw/S3TVN5ixy2Jo=; SPC_R_T_IV=WVUycHVickM2eE5idGRMRg==; SPC_T_ID=zth6DF58mGimc15AQ/5CfCexpv5ZrgMY1HlamI+vCDJvoXF8QABjWaVClfZQ8DPfpFN+JgnIJWGJB2dD3mvNxH7bCfGkFSNe12kGYJHakcrsfFIUih37vW9sXT5XjrOu9qTC8+k0Qb4EKwHPqa25FYe4t2KNiw/S3TVN5ixy2Jo=; SPC_T_IV=WVUycHVickM2eE5idGRMRg==',
    'X-Request-Id':'1f8a1b84fc29739bfde9231d03365700:000000067b7a9dae:0000000000000000'
}
#----------------------------------------------------------------------
#key in your username/password
username=''
password=''
keyword = "七變化虎耳草"
ecode = 'utf-8-sig'
page = 1
#----------------------------------------------------------------------
# 進入每個商品，抓取買家留言
def goods_comments(item_id, shop_id, page=1):
    offset = (page - 1) * 50
    url = 'https://shopee.tw/api/v4/item/get_ratings?filter=0&flag=1&itemid=' + str(
        item_id) + '&limit=50&offset=' + str(offset) + '&shopid=' + str(shop_id) + '&type=0'
    r = requests.get(url, headers=my_headers)
    st = r.text.replace("\\n", "^n")
    st = st.replace("\\t", "^t")
    st = st.replace("\\r", "^r")
    gj = json.loads(st)
    return gj['data']['ratings']
#----------------------------------------------------------------------
# 進入每個商品，抓取賣家更細節的資料（商品文案、SKU）

def goods_detail(url, item_id, shop_id):
    driver.get(url) 
    time.sleep(random.randint(10,20))
    getPacket = ''
    for request in driver.requests:
        if request.response:
            # 挑出商品詳細資料的json封包
            if 'https://shopee.tw/api/v4/pdp/hot_sales/get?itemid=' + str(item_id) + '&shopid=' + str(shop_id) in request.url:
                # 此封包是有壓縮的，因此需要解壓縮
                try:
                    getPacket = zlib.decompress(
                        request.response.body,
                        16+zlib.MAX_WBITS
                        )
                    break
                except:
                    print('封包有誤')
    if getPacket != '':
        gj=json.loads(getPacket)
        return gj['data']
    else:
        return getPacket
#----------------------------------------------------------------------
service = ChromeService(executable_path=ChromeDriverManager().install())
options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
options.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(service=service, chrome_options=options)
time.sleep(random.randint(10, 20))
#----------------------------------------------------------------------
driver.get('https://shopee.tw/search?keyword=' + keyword )
time.sleep(random.randint(10,20))
#----------------------------------------------------------------------
driver.find_element(By.CSS_SELECTOR, 'input[name="loginKey"]').send_keys(username)
time.sleep(2)
driver.find_element(By.CSS_SELECTOR, 'input[name="password"]').send_keys(password)
time.sleep(3)
driver.find_element(by=By.XPATH, value='//*[@id="main"]/div/div[2]/div/div/div/div[2]/form/div/div[2]/button').click()
time.sleep(3)
#----------------------------------------------------------------------
print('---------- 開始進行爬蟲 ----------')
tStart = time.time()
#----------------------------------------------------------------------
container_product = pd.DataFrame()
container_comment = pd.DataFrame()
for i in range(int(page)):
    itemid = []
    shopid =[]
    name = []
    link = []
    stock = []
    price = []
    ctime = []
    description = []
    discount = []
    can_use_bundle_deal = []
    can_use_wholesale = []
    tier_variations = []
    historical_sold = []
    is_cc_installment_payment_eligible = []
    is_official_shop = []
    is_pre_order = []
    liked_count = []
    shop_location = []
    SKU = []
    cmt_count = []
    five_star = []
    four_star = []
    three_star = []
    two_star = []
    one_star = []
    rating_star = []
    
    driver.get('https://shopee.tw/search?keyword=' + keyword + '&page=' + str(i))
    time.sleep(random.randint(5,10))
    
    # 滾動頁面
    for scroll in range(6):
        driver.execute_script('window.scrollBy(0,1000)')
        time.sleep(random.randint(10,15))
    
    #取得商品內容
    for item, thename in zip (driver.find_elements(By.CSS_SELECTOR,'div.col-xs-2-4 *[data-sqe="link"]'),
                              driver.find_elements(By.CSS_SELECTOR,'div.col-xs-2-4 *[data-sqe="name"]')):
        #商品ID、商家ID、商品連結
        getID = item.get_attribute('href')
        theitemid = int((getID[getID.rfind('.')+1:getID.rfind('?')]))
        theshopid = int(getID[ getID[:getID.rfind('.')].rfind('.')+1 :getID.rfind('.')]) 
        link.append(getID)
        itemid.append(theitemid)
        shopid.append(theshopid)
        
        #商品名稱
        getname = thename.text.split('\n')[0]
        name.append(getname)
        
        #價格
        thecontent = item.text
        thecontent = thecontent[(thecontent.find(getname)) + len(getname):]
        thecontent = thecontent.replace('萬','000')
        thecut = thecontent.split('\n')

        if len(thecut) >= 3:
            if bool(re.search('市|區|縣|鄉|海外|中國大陸', thecontent)): #有時會沒有商品地點資料
                if bool(re.search('已售出', thecontent)): #有時會沒銷售資料
                    if '出售' in thecut[-3][1:]:
                        theprice = thecut[-4][1:]
                    else:
                        theprice = thecut[-3][1:]
                else:
                    theprice = thecut[-2][1:]
            else:
                theprice = thecut[-1][1:]
        elif re.search('已售出', thecontent): #有時會沒銷售資料
                theprice = thecut[-2][1:]
        else:                               # 處理 thecut 列表不足 3 個元素的情況（例如將 theprice 設置為空字符串）
            theprice = ''
        
        theprice = theprice.replace('$','')
        theprice = theprice.replace(',','')
        theprice = theprice.replace('國','')
        theprice = theprice.replace('已','')
        theprice = theprice.replace('售','')
        theprice = theprice.replace('出','')
        theprice = theprice.replace(' ','')
        if ' - ' in theprice:
            theprice = (int(theprice.split(' - ')[0]) +int(theprice.split(' - ')[1]))/2
        if '-' in theprice:
            theprice = (int(theprice.split('-')[0]) +int(theprice.split('-')[1]))/2
        if theprice != '':
            price.append(int(theprice))
        else:
            price.append(0)
#         break
    for lnk, itid, shid in zip(link, itemid, shopid):
        #請求商品詳細資料
        itemDetail = goods_detail(url = lnk, item_id = itid, shop_id = shid)
        print('抓取： '+ str(itid) )
        if itemDetail == '':
            # 抓不到資料就全部塞空值
            print('抓不到商品詳細資料...\n')
#             brand.append(None) #品牌
            stock.append(None) #存貨數量
            ctime.append(None) #上架時間
            description.append(None) #商品文案
            discount.append(None) #折數
            can_use_bundle_deal.append(None) #可否搭配購買
            can_use_wholesale.append(None) #可否大量批貨購買
            tier_variations.append(None) #選項
            historical_sold.append(None) #歷史銷售量
            is_cc_installment_payment_eligible.append(None) #可否分期付款
            is_official_shop.append(None) #是否官方賣家帳號
            is_pre_order.append(None) #是否可預購
            liked_count.append(None) #喜愛數量
            SKU.append(None) #SKU
            shop_location.append(None) #商家地點
            cmt_count.append(None) #評價數量
            five_star.append(None) #五星
            four_star.append(None) #四星
            three_star.append(None) #三星
            two_star.append(None) #二星
            one_star.append(None) #一星
            rating_star.append(None) #評分
            continue

#         brand.append(itemDetail['brand']) #品牌
        stock.append(itemDetail['stock']) #存貨數量
        ctime.append(itemDetail['ctime']) #上架時間
        description.append(itemDetail['description']) #商品文案
        discount.append(itemDetail['discount']) #折數
        can_use_bundle_deal.append(itemDetail['can_use_bundle_deal']) #可否搭配購買
        can_use_wholesale.append(itemDetail['can_use_wholesale']) #可否大量批貨購買
        tier_variations.append(itemDetail['tier_variations']) #選項
        historical_sold.append(itemDetail['historical_sold']) #歷史銷售量
        is_cc_installment_payment_eligible.append(itemDetail['is_cc_installment_payment_eligible']) #可否分期付款
        is_official_shop.append(itemDetail['is_official_shop']) #是否官方賣家帳號
        is_pre_order.append(itemDetail['is_pre_order']) #是否可預購
        liked_count.append(itemDetail['liked_count']) #喜愛數量
        
        #SKU
        all_sku=[]
        for sk in itemDetail['models']:
            all_sku.append(sk['name'])
        SKU.append(all_sku) #SKU
        shop_location.append(itemDetail['shop_location']) #商家地點
        cmt_count.append(itemDetail['cmt_count']) #評價數量
        five_star.append( itemDetail['item_rating']['rating_count'][5] ) #五星
        four_star.append( itemDetail['item_rating']['rating_count'][4] ) #四星
        three_star.append( itemDetail['item_rating']['rating_count'][3] ) #三星
        two_star.append( itemDetail['item_rating']['rating_count'][2] ) #二星
        one_star.append( itemDetail['item_rating']['rating_count'][1] ) #一星
        rating_star.append(itemDetail['item_rating']['rating_star']) #評分
     
    current_page = 1
    has_more_comments = True

    for lnk, itid, shid in zip(link, itemid, shopid):
        iteComment, total_reviews = goods_comments(item_id=itid, shop_id=shid, page=current_page)  #
        reviews_per_page = 50
        total_pages = total_reviews // reviews_per_page
        if total_reviews % reviews_per_page > 0:
            total_pages += 1
    # 消費者評論詳細資料
        while has_more_comments:
            
            iteComment = goods_comments(item_id = itid, shop_id = shid, page=current_page)
            if not iteComment[0]:
                break
            userid = [] #使用者ID
            anonymous = [] #是否匿名
            commentTime = [] #留言時間
            is_hidden = [] #是否隱藏
            orderid = [] #訂單編號
            comment_rating_star = [] #給星
            comment = [] #留言內容
            product_SKU = [] #商品規格

            print(itid, current_page, len(iteComment[0]))  #印出產品ID 頁數  評論數
            
            for comm in iteComment[0]:
                userid.append(comm['userid'])
                anonymous.append(comm['anonymous'])
                commentTime.append(comm['ctime'])
                is_hidden.append(comm['is_hidden'])
                orderid.append(comm['orderid'])
                comment_rating_star.append(comm['rating_star'])
                try:
                    comment.append(comm['comment'])
                except:
                    comment.append(None)
                product_SKU_per_comment = []
                for pro in comm['product_items']:
                    try:
                        product_SKU_per_comment.append(pro['model_name'])
                    except:
                        product_SKU_per_comment.append(None)

                product_SKU.append(product_SKU_per_comment)
            
            commDic = {
                '商品ID':[ itid for x in range(len(iteComment[0])) ],
                '賣家ID':[ shid for x in range(len(iteComment[0])) ],
                '商品名稱':[ getname for x in range(len(iteComment[0])) ],
                '價格':[int(theprice) if theprice != '' else 0 for x in range(len(iteComment[0]))],
                '使用者ID':userid,
                '是否匿名':anonymous, 
                '留言時間':commentTime,
                '是否隱藏':is_hidden,
                '訂單編號':orderid,
                '給星':comment_rating_star,
                '留言內容':comment,
                '商品規格':product_SKU
                }
            lengths = [len(v) for v in commDic.values()]
            if len(set(lengths)) > 1: 
                print(f"Lengths are not equal: {lengths}")
                print(commDic)  # Add this line to print commDic
            container_comment = pd.concat([container_comment, pd.DataFrame(commDic)], axis=0)


            time.sleep(random.randint(15,30)) # 休息久一點
            if current_page>=6:   #最多抓取6頁300筆
                has_more_comments = False
                current_page = 1
            elif current_page < total_pages:
                current_page += 1
            else:
                has_more_comments = False
                current_page = 1
        has_more_comments = True
        
    dic = {
        '商品ID':itemid,
        '賣家ID':shopid,
        '商品名稱':name,
        '商品連結':link,
#         '品牌':brand,
        '存貨數量':stock,
        '價格':price,
        '商品文案':description,
        '折數':discount,
        '可否搭配購買':can_use_bundle_deal,
        '可否大量批貨購買':can_use_wholesale,
        '選項':tier_variations,
        '歷史銷售量':historical_sold,
        '可否分期付款':is_cc_installment_payment_eligible,
        '是否官方賣家帳號':is_official_shop,
        '是否可預購':is_pre_order,
        '喜愛數量':liked_count,
        '商家地點':shop_location,
        'SKU':SKU,
        '評價數量':cmt_count,
        '五星':five_star,
        '四星':four_star,
        '三星':three_star,
        '二星':two_star,
        '一星':one_star,
        '評分':rating_star,
    }

    #處理字典 dic，將字典中的每個值（列表）都填充到相同的長度 因為在創建 DataFrame 時，所有列都需要具有相同的長度。
    max_length = max([len(v) for v in dic.values()])
    for key, value in dic.items():
        if len(value) < max_length:
            dic[key] = value + [None] * (max_length - len(value))
    #資料整合
    container_product = pd.concat([container_product,pd.DataFrame(dic)], axis=0)
    #暫時存檔紀錄
    container_product.to_csv('shopeeAPIData'+str(i+1)+'_Product.csv', encoding = ecode, index=False)
    container_comment.to_csv('shopeeAPIData'+str(i+1)+'_Comment.csv', encoding = ecode, index=False)

    print('目前累積商品： ' + str(len(container_product)) + ' 留言累積' + str(len(container_comment)))
    time.sleep(random.randint(10,30)) 

#----------------------------------------------------------------------
container_product.to_csv(keyword +'_商品資料.csv', encoding = ecode, index=False)
container_comment.to_csv(keyword +'_留言資料.csv', encoding = ecode, index=False)
#----------------------------------------------------------------------
tEnd = time.time()#計時結束
totalTime = int(tEnd - tStart)
minute = totalTime // 60
second = totalTime % 60
print('資料儲存完成，花費時間（約）： ' + str(minute) + ' 分 ' + str(second) + '秒')
#----------------------------------------------------------------------
driver.close() 