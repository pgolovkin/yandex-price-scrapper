import base64
import os
import string

import requests
import json
from bs4 import BeautifulSoup
from time import sleep
from datetime import date
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

GOODS = [
    {"Холодильник LG GA-B459MQSL, белый": "https://market.yandex.ru/product--kholodilnik-lg-doorcooling-ga-b459m-sl/649939034?nid=71639&show-uid=16487062223606251975406023&context=search&sku=101631926730"},
    {"Смартфон Samsung Galaxy S22 Ultra (SM-S908B) 12/512GB RU Phantom Black (Черный": "https://market.yandex.ru/product--smartfon-samsung-galaxy-s22-ultra-sm-s908b/1665531245?nid=26828310&show-uid=16487062223606251975406021&context=search&sku=101610502749"},
    {"Телевизор Samsung UE32T5300AU": "https://market.yandex.ru/product--32-televizor-samsung-ue32t5300au-led-hdr-2020/661339018?nid=26960210&show-uid=16487062223606251975406019&context=search&sku=100911195769"},
    {"Телевизор Samsung UE24N4500AU LED, HDR (2018)": "https://market.yandex.ru/product--24-televizor-samsung-ue24n4500au-led-2018/648953154?nid=26960210&show-uid=16487062223606251975406013&context=search&sku=100845027438"},
    {"Холодильник LG DoorCooling+ GA-B509SVUM, белый": "https://market.yandex.ru/product--kholodilnik-lg-doorcooling-ga-b509svum/717088000?nid=71639&show-uid=16487062223606251975406007&context=search&sku=717088000"},
    {"Холодильник LG GA-B459MEQM, бежевый": "https://market.yandex.ru/product--kholodilnik-lg-ga-b459meqm/871698040?nid=71639&show-uid=16487062223606251975406005&context=search&sku=871698040"},
    {"Ноутбук APPLE MacBook Pro 14 (2021) Space Grey MKGP3RU/A (Apple M1 Pro with 8-core CPU": "https://market.yandex.ru/product--14-2-noutbuk-apple-macbook-pro-14-late-2021-3024-1964-apple-m1-pro-ram-16-gb-ssd-512-gb-apple-graphics-14-core/1447472428?nid=26895412&show-uid=16487062223606251975406001&context=search&sku=101459417737"},
    {"Квадрокоптер DJI Mini SE Fly More Combo, белый": "https://market.yandex.ru/product--kvadrokopter-dji-mini-se-fly-more-combo/1483484419?cpa=1&sku=101507521741&offerid=lrp8ba30D2RVcM97VAiAlQ"},
    {"Электрический стабилизатор для смартфона DJI Osmo Mobile 4": "https://market.yandex.ru/product--elektricheskii-stabilizator-dlia-smartfona-dji-osmo-mobile-4/821146023?cpa=1&sku=821146023&nid=26995670"},
    {"Электрический стабилизатор для смартфона DJI OM 5 athens gray": "https://market.yandex.ru/offer/XLxcOkihMlPfGsjrLoHvTw?cpc=LKuPusMKeF_2v2e9labS-IQVyILHrtWSmfdKdN2VRcGUuqL3bBTpKRxUJe5JOr1lj2zElX1bbqkoZk50j-ED4OAAeZ_Qg4BckznfJ_TlR5lEdIHsndN0DO6eTyi3qAOGJ1xV-GFpVvQ4-q5ImiEiON9ceUHKMwd19TNt35nHeJ0Keeae9dtoOvNKmfSWnh-SsgP9aJwl1KU%2C&hid=15880008&hyperid=1450883456&lr=192&modelid=1450883456&nid=26995670&text=DJI%20Osmo%20Mobile%205&show-uid=16498423117804114325000001"},
    {"Торцовочная пила с протяжкой ЗУБР ЗПТ-255-1800 ПЛ, 1800 Вт": "https://market.yandex.ru/product--tortsovochnaia-pila-s-protiazhkoi-zubr-zpt-255-1800-pl-1800-vt/14178346?nid=70997&show-uid=16500128545864410327316002&context=search&text=%D0%B7%D1%83%D0%B1%D1%80%20%D0%BF%D1%80%D0%BE%D1%84%D0%B5%D1%81%D1%81%D0%B8%D0%BE%D0%BD%D0%B0%D0%BB%20%D0%BF%D0%BF%D1%82%20255%D0%BF&sku=14178346&cpc=4vj2ECJjVWvRq1TLTfeQq3-wZWQI_sO04_GxgD4PKm46yNpny63Q_Yy2TW9VPUqSxffKgi9uUEKQ3RAyrBCD7u6Akr-49sW_zjSBOYAaxPFvBe0HXvyCrc_ai7WGC_Bn9JqlYOfflKAgdg2Sqx5MsjQEX79Vv2M7ysX9kNLu90ae1mS2Gm6vanwc8dL7_sAtuM4C5XftaGk%2C&do-waremd5=I2_s1nETi05karBkBsNPmw&sponsored=1"},
    {"Пила торцовочная ЗУБР Профессионал ППТ-216-П", "https://market.yandex.ru/product--pila-tortsovochnaia-zubr-professional-ppt-216-p/1399192317?text=%D0%B7%D1%83%D0%B1%D1%80%20%D0%BF%D1%80%D0%BE%D1%84%D0%B5%D1%81%D1%81%D0%B8%D0%BE%D0%BD%D0%B0%D0%BB%20%D0%BF%D0%BF%D1%82%20216%D0%BF&cpc=uUpiwrvnv6LGaGRXAGRtoNWy0F_aK6k0Lbdr9LDLzi39uO_QKKeGLE52OTei4CBNmOfkRRWmeEq-YynGTkTZCmQ0KLzJ2qnQexYnq3hO2H2TzvxU-ApcE-MXLR-irXtEoz3hNT1iNhUt6vg_CdB3z35Cuc6PjktYhRF6pE87mQA4tppAu6kE9GrdKgxm70WJ&sku=101390038248&do-waremd5=LVk6EQWZqZTlJbeWyfNTqw&cpa=1&nid=70997"}
]

USD_CODE = "840"
GOOGLE_SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
GOOGLE_DOC_ID = os.environ['GOOGLE_DOC_ID']
GOOGLE_TOKEN = json.loads(base64.b64decode(os.environ['GOOGLE_TOKEN']))
CBR_RATE_URL = "https://www.cbr.ru/currency_base/daily/"


def update_sheet(current_date, cbr_rate_value, price_values):
    creds = Credentials.from_authorized_user_info(GOOGLE_TOKEN, GOOGLE_SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    new_row = [current_date] + price_values + [cbr_rate_value]
    new_row_end_letter = string.ascii_uppercase[len(new_row) - 1]
    new_row_index = 1
    while True:
        current_row = sheet.values().get(spreadsheetId=GOOGLE_DOC_ID,
                                         range="A" + str(new_row_index) + ":" + new_row_end_letter + str(new_row_index)).execute()
        values = current_row.get('values', [])
        if not values:
            break
        else:
            new_row_index += 1

    sheet.values().update(spreadsheetId=GOOGLE_DOC_ID,
                                   range="A"+str(new_row_index) + ":" + new_row_end_letter + str(new_row_index),
                                   valueInputOption='USER_ENTERED',
                                   body={"values": [new_row]}).execute()


def get_prices():
    result_array = []
    for good in GOODS:
        for key in good:
            url = good[key]
            market_page = requests.get(url)
            i = 1
            while market_page.headers.get('Content-Length'):
                sleep(60 * i)
                i += 1
                market_page = requests.get(url)

            soup = BeautifulSoup(market_page.content, "html.parser")
            no_price_element = soup.find("div", class_="_1Kcza")
            if not no_price_element:
                span_element = soup.find("div", class_="KnVez").find(class_="_3NaXx _3kWlK")
                price = span_element.next_element.next_element.getText().replace(" ", "")
                result_array += [price]
            else:
                result_array += [0]
    return result_array


def get_cbr_rate():
    usd_page = requests.get(CBR_RATE_URL)
    soup = BeautifulSoup(usd_page.content, "html.parser")
    usd_price_in_rub = soup.find("td", text=USD_CODE).find_next_sibling("td").find_next_sibling("td").find_next_sibling("td").find_next_sibling("td").getText()
    return usd_price_in_rub


cbr_rate = get_cbr_rate()
prices = get_prices()
today_str = date.today().strftime("%d.%m.%Y")
update_sheet(today_str, cbr_rate, prices)
