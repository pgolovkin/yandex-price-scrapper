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
    {"Квадрокоптер DJI Mini SE Fly More Combo, белый": "https://market.yandex.ru/product--kvadrokopter-dji-mini-se-fly-more-combo/1483484419?cpa=1&sku=101507521741&offerid=lrp8ba30D2RVcM97VAiAlQ"}
]

USD_CODE = "840"
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
GOOGLE_SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
GOOGLE_DOC_ID = os.environ.get('GOOGLE_DOC_ID')
GOOGLE_TOKEN = json.loads(os.environ.get('GOOGLE_TOKEN'))
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
                                   valueInputOption='RAW',
                                   body={"values": [new_row]}).execute()


def get_prices():
    for good in GOODS:
        result_array = []
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
