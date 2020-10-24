import asyncio
import random
import csv
from selenium import webdriver


# Chome 드라이버 추출하기
# browser = webdriver.Chrome(executable_path='D:/000UbicFinal/chromedriver')
# browser2 = webdriver.Chrome(executable_path='D:/000UbicFinal/chromedriver')
# print(browser, browser2)  # 다르다 ok

# url_login = "https://everytime.kr/login"
# url_login = 'http://localhost:8080/'
# browser.get(url_login)
# print('페이지 접근')


## css_selector
# e = browser.find_element_by_css_selector("#container > form > p:nth-child(1) > input").click()
# button.btn.btn-primary.btn-lg.btn-shoplist ## 장바구니 selector
# button.btn.btn-primary.btn-lg.btn-order-immediately-from-detail ## 즉시주문 selector

def get_product_id_list():
    csvfile = open('product_id_list.txt', 'r')

    fieldnames = ("product_id",)
    reader = csv.DictReader(csvfile, fieldnames)

    product_id_list = []
    for row in reader:
        product_id_list.append(row['product_id'])
    return product_id_list


product_id_list = get_product_id_list()


# print("random item from list is: ", random.choice(product_id_list))


# url_product_detail = 'http://localhost:8080/products/' + random.choice(product_id_list)
#
# browser.get(url_product_detail)

async def user_test():
    # for test in range(10): ## test 10

    browser = webdriver.Chrome(executable_path='D:/000UbicFinal/chromedriver')
    url_product_detail = 'http://localhost:8080/products/' + random.choice(product_id_list)
    browser.get(url_product_detail)
    await asyncio.sleep(3.0)  # 3초 대기. asyncio.sleep도 네이티브 코루틴


async def test_user_10():
    for test in range(10):  ## test 10
        user_test()
        print('test_user_10', test)


loop = asyncio.get_event_loop()  # 이벤트 루프를 얻음
loop.run_until_complete(test_user_10())  # print_add가 끝날 때까지 이벤트 루프를 실행
loop.close()
