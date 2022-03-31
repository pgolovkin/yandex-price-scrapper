import requests
from bs4 import BeautifulSoup
from time import sleep
from datetime import date

GOODS = [
    {"Холодильник LG GA-B459MQSL, белый": "https://market.yandex.ru/product--kholodilnik-lg-doorcooling-ga-b459m-sl/649939034?nid=71639&show-uid=16487062223606251975406023&context=search&sku=101631926730"},
    {"Смартфон Samsung Galaxy S22 Ultra (SM-S908B) 12/512GB RU Phantom Black (Черный": "https://market.yandex.ru/product--smartfon-samsung-galaxy-s22-ultra-sm-s908b/1665531245?nid=26828310&show-uid=16487062223606251975406021&context=search&sku=101610502749"},
    {"Телевизор Samsung UE32T5300AU": "https://market.yandex.ru/product--32-televizor-samsung-ue32t5300au-led-hdr-2020/661339018?nid=26960210&show-uid=16487062223606251975406019&context=search&sku=100911195769"},
    {"Телевизор Samsung UE24N4500AU LED, HDR (2018)": "https://market.yandex.ru/product--24-televizor-samsung-ue24n4500au-led-2018/648953154?nid=26960210&show-uid=16487062223606251975406013&context=search&sku=100845027438"},
    {"Холодильник LG DoorCooling+ GA-B509SVUM, белый": "https://market.yandex.ru/product--kholodilnik-lg-doorcooling-ga-b509svum/717088000?nid=71639&show-uid=16487062223606251975406007&context=search&sku=717088000"},
    {"Холодильник LG GA-B459MEQM, бежевый": "https://market.yandex.ru/product--kholodilnik-lg-ga-b459meqm/871698040?nid=71639&show-uid=16487062223606251975406005&context=search&sku=871698040"},
    {"Ноутбук APPLE MacBook Pro 14 (2021) Space Grey MKGP3RU/A (Apple M1 Pro with 8-core CPU": "https://market.yandex.ru/product--14-2-noutbuk-apple-macbook-pro-14-late-2021-3024-1964-apple-m1-pro-ram-16-gb-ssd-512-gb-apple-graphics-14-core/1447472428?nid=26895412&show-uid=16487062223606251975406001&context=search&sku=101459417737"}
]

USD_CODE = "840"

usd_page = requests.get("https://www.cbr.ru/currency_base/daily/")
soup = BeautifulSoup(usd_page.content, "html.parser")
usd_price_in_rub = soup.find("td", text=USD_CODE).find_next_sibling("td").find_next_sibling("td").find_next_sibling("td").find_next_sibling("td").getText()

date = date.today().strftime("%d.%m.%Y")
print(date)
print(usd_price_in_rub)

for good in GOODS:
    for key in good:
        URL = good[key]
        market_page = requests.get(URL)
        soup = BeautifulSoup(market_page.content, "html.parser")
        span_element = soup.find("div", class_="KnVez").find(class_="_3NaXx _3kWlK")
        result = span_element.next_element.next_element.getText().replace(" ", "")
        print(key + " " + result)
        sleep(600)
