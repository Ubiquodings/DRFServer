from time import time
from urllib.request import Request, urlopen
import asyncio

import random
import csv
from selenium import webdriver


# urls = ['https://www.google.co.kr/search?q=' + i
#         for i in ['apple', 'pear', 'grape', 'pineapple', 'orange', 'strawberry']]

def get_product_id_list():
    csvfile = open('product_id_list.txt', 'r')

    fieldnames = ("product_id",)
    reader = csv.DictReader(csvfile, fieldnames)

    product_id_list = []
    for row in reader:
        product_id_list.append(row['product_id'])
    return product_id_list


product_id_list = get_product_id_list()

action_select_list = [0, 1]  # 0:장바구니 , 1:즉시주문


async def fetch():
    # request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})  # UA가 없으면 403 에러 발생
    browser = webdriver.Chrome(executable_path='D:/000UbicFinal/chromedriver')

    while True:
        product_detail_id = random.choice(product_id_list)
        print(product_detail_id, browser, time())
        url_product_detail = 'http://localhost:8080/products/' + product_detail_id
        browser.get(url_product_detail)  # 상품 상세 화면 이동

        # 장바구니 또는 바로구매
        action_flag = random.choice(action_select_list)
        if action_flag == 0:  # 장바구니
            print('장바구니 ', browser)
            browser.find_element_by_css_selector("button.btn.btn-primary.btn-lg.btn-shoplist").click()
        else:  # 즉시구매
            print('즉시구매 ', browser)
            browser.find_element_by_css_selector(
                "button.btn.btn-primary.btn-lg.btn-order-immediately-from-detail").click()

        await asyncio.sleep(3.0)  # 실전은 3초 대기. asyncio.sleep도 네이티브 코루틴

    # response = await loop.run_in_executor(None, urlopen, request)  # run_in_executor 사용
    # page = await loop.run_in_executor(None, response.read)  # run in executor 사용
    # return len(page)


async def main():
    futures = [asyncio.ensure_future(fetch()) for test in range(20)]  # 10개 원소 리스트
    # 태스크(퓨처) 객체를 리스트로 만듦
    result = await asyncio.gather(*futures)  # 결과를 한꺼번에 가져옴 : 리스트 반환
    print(result)


begin = time()
loop = asyncio.get_event_loop()  # 이벤트 루프를 얻음
loop.run_until_complete(main())  # main이 끝날 때까지 기다림
loop.close()  # 이벤트 루프를 닫음
end = time()
print('실행 시간: {0:.3f}초'.format(end - begin))
