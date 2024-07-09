import requests
from bs4 import BeautifulSoup
import soupsieve as sv

headers = {
    # "User-Agent": ua.opera
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
    "Accept": "*/*"
}

# # точка отправления https://suggests.rasp.yandex.net/all_suggests?field=from&format=old&lang=ru&national_version=ru&part=***
# # точка назначения https://suggests.rasp.yandex.net/all_suggests?field=to&format=old&lang=ru&national_version=ru&part=***
#
# From = 'Краснодар'
# To = 'Северская'
#
# url = f"https://suggests.rasp.yandex.net/all_suggests?field=from&format=old&lang=ru&national_version=ru&part={From}".format(From)
#
#
# # Тянем fromId
#
# r = requests.get(url, headers=headers)
# src = r.text
#
# with open('fromtxt.html','w',encoding='utf-8', newline='') as file:
#    file.write(src)
#
# with open('fromtxt.html',encoding='utf-8', newline='') as file:
#     i = 0
#     from_id = ''
#     for line in file:
#         for char in line:
#             if(i == 1):
#                 if(char != '"'):
#                     from_id = from_id + char
#             if (char == '"'):
#                 i += 1
# print(from_id)
#
#
#
#
# # Тянем toId
#
# url = f"https://suggests.rasp.yandex.net/all_suggests?field=to&format=old&lang=ru&national_version=ru&part={To}".format(To)
# r = requests.get(url, headers=headers)
# src = r.text
#
# with open('totxt.html','w',encoding='utf-8', newline='') as file:
#     file.write(src)
#
# with open('totxt.html',encoding='utf-8', newline='') as file:
#     i = 0
#     to_id = ''
#     for line in file:
#         for char in line:
#             if(i == 1):
#                 if(char != '"'):
#                     to_id = to_id + char
#             if (char == '"'):
#                 i += 1
# print(to_id)
#
# # Тянем страницу расписания без даты (when = 'число + месяц') хотя можно и с датой
# # там календарик какойнить простенький или поле для ввода
# # url = f"https://www.avtovokzaly.ru/avtobus/{FromTo}?date={date}".format(FromTo,date) другой сайт(на всякий)
# # url = f"https://rasp.yandex.ru/bus/{From}--{To}".format(From, To) без ID
# url = f"https://rasp.yandex.ru/search/?fromId={from_id}&fromName={From}&toId={to_id}&toName={To}".format(from_id, From, to_id, To)
# r = requests.get(url, headers=headers)
# src = r.text
#
# print(url)
# with open('index_final_test.html','w',encoding='utf-8', newline='') as file:
#      file.write(src)
#
#
# i = 0
# items_dict = {}
# with open('index_final_test.html',encoding='utf-8', newline='') as file:
#     src = file.read()
#
# soup = BeautifulSoup(src, 'lxml')
#
# items_dep = []
# links = soup.find_all("td", "TableTimeAndStations__departure")
# for link in links:
#     time = link.find("span")
#     time_dep = time.text
#     station = link.find("a")
#     station_dep = station.text
#     item_dep = time_dep + '\n' + station_dep
#     items_dep.append(item_dep)
#
# items_arr = []
# links = soup.find_all("td", "TableTimeAndStations__arrival")
# for link in links:
#     time = link.find("span")
#     time_arr = time.text
#     station = link.find("a")
#     station_arr = station.text
#     item_arr = time_arr + '\n' + station_arr
#     items_arr.append(item_arr)
#     # print(item_arr)
#
# for x in items_dep:
#     print(x)
#
# for x in items_arr:
#     print(x)




er = 0
pointdep = 'Москва'
pointarr = 'Краснодар'



url = f"https://partner.onetwotrip.com/_partner/rzd/suggestStations?flat=true&lang=ru&searchText={pointdep}&type=station".format(pointdep)
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, 'lxml')
from_key = ''
link = soup.find("p")
from_text = link.text
i = from_text.find('trans')
if (i != -1):
    er += 1
    char = ''
    while (char != '"'):
        char = from_text[i + 8]
        from_key = from_key + char
        i += 1

from_key = from_key[:-1]

print(from_key)

url = f"https://partner.onetwotrip.com/_partner/rzd/suggestStations?flat=true&lang=ru&searchText={pointarr}&type=station".format(pointarr)
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, 'lxml')
to_key = ''
link = soup.find("p")
to_text = link.text
i = to_text.find('trans')
if (i != -1):
    er += 1
    char = ''
    while (char != '"'):
        char = to_text[i + 8]
        to_key = to_key + char
        i += 1

to_key = to_key[:-1]

print(to_key)


url = f"https://www.onetwotrip.com/ru/poezda/{from_key}_{to_key}/".format(from_key, to_key)
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, 'lxml')
items_dep = []
links = soup.find_all("div", "train-card__time")

for link in links:
    time = link.find("div", "train-card__time__info__departure")
    time_dep = time.text
    station = link.find("div", "")
    station_dep = station.text
    station_dep = str(station_dep)
    item_dep = time_dep + '\n' + station_dep
    items_dep.append(item_dep)

items_arr = []
links = soup.find_all("div", "train-card__time")

for link in links:
    time = link.find("div", "train-card__time__info__arrival")
    time_arr = time.text
    station = link.find("div", "")
    station = station.find_next("div", "")
    station_arr = station.text
    station_arr = str(station_arr)
    item_arr = time_arr + '\n' + station_arr
    items_arr.append(item_arr)

for x in items_dep:
    print(x)

for x in items_arr:
    print(x)