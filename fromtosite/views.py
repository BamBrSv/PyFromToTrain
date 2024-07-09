from django.shortcuts import render
from .forms import From_to_form
import requests
from bs4 import BeautifulSoup
# from urllib.request import urlopen
# import html5lib

import soupsieve as sv
# Create your views here.


headers = {
        # "User-Agent": ua.opera
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54",

        "Accept": "*/*"
    }

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt


def main(request):


    submitbutton= request.POST.get("submit")

    pointdep=''
    pointarr=''
    transport=''

    form= From_to_form(request.POST or None)
    if form.is_valid():
        transport= form.cleaned_data.get("transport")
        pointdep= form.cleaned_data.get("pointdep")
        pointdep1 = form.cleaned_data.get("pointdep1")
        pointdep2 = form.cleaned_data.get("pointdep2")
        pointdep3 = form.cleaned_data.get("pointdep3")
        pointarr= form.cleaned_data.get("pointarr")

        context= {'form': form, 'transport': transport, 'pointdep': pointdep, 'pointarr': pointarr}



        er = 0
        if transport=='Автобус' :
            url = f"https://www.avtovokzaly.ru/city/suggest?query={pointdep}".format(pointdep)
            r = requests.get(url, headers=headers)
            soup = BeautifulSoup(r.text, 'lxml')
            print(soup)
            from_key = ''
            link = soup.find("p")
            from_text = link.text
            from_text = str(from_text)
            i = from_text.find('key')
            if (i != -1):
                er += 1
                char = ''
                while (char != '"'):
                    char = from_text[i+6]
                    from_key = from_key + char
                    i += 1

                from_key = from_key[:-1]

                print(from_key)

                # Тянем to_key

                url =f"https://www.avtovokzaly.ru/city/suggest?query={pointarr}".format(pointarr)
                r = requests.get(url, headers=headers)
                soup = BeautifulSoup(r.text, 'lxml')
                to_key = ''
                link = soup.find("p")
                to_text = link.text
                i = to_text.find('key')
                if (i != -1):
                    er += 1
                    char = ''
                    while (char != '"'):
                        char = to_text[i + 6]
                        to_key = to_key + char
                        i += 1

                to_key = to_key[:-1]

                print(to_key)

            if (er == 2):

                url = f"https://www.avtovokzaly.ru/avtobus/{from_key}-{to_key}".format(from_key, to_key)
                r = requests.get(url, headers=headers)
                soup = BeautifulSoup(r.text, 'lxml')
                items_dep = []
                links = soup.find_all("tr", "dd-additional-info")

                for link in links:
                    time = link.find("span", "strong")
                    time_dep = time.text
                    station = link.find("div", "secondary-text")
                    station_dep = station.text
                    station_dep = str(station_dep)
                    item_dep = time_dep + '\n' + station_dep
                    items_dep.append(item_dep)

                items_arr = []
                links = soup.find_all("tr", "dd-additional-info")

                for link in links:
                    time = link.find("span", "strong")
                    time = time.find_next("span", "strong")
                    time_arr = time.text
                    station = link.find("div", "secondary-text")
                    station = station.find_next("div", "secondary-text")
                    station_arr = station.text
                    station_arr = str(station_arr)
                    item_arr = time_arr + '\n' + station_arr
                    items_arr.append(item_arr)

            else:
                items_arr = ['не найдено проверьте введённые данные']
                items_dep = ['не найдено проверьте введённые данные']

            # context = {"items_dep": items_dep, "items_arr": items_arr}
            # return render(request, 'cntx.html', context)


        else:
            url = f"https://partner.onetwotrip.com/_partner/rzd/suggestStations?flat=true&lang=ru&searchText={pointdep}&type=station".format(
                pointdep)
            r = requests.get(url, headers=headers)
            soup = BeautifulSoup(r.text, 'lxml')
            from_key = ''
            link = soup.find("p")
            print(link.text)
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

            url = f"https://partner.onetwotrip.com/_partner/rzd/suggestStations?flat=true&lang=ru&searchText={pointarr}&type=station".format(
                pointarr)
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

            if (er == 2):
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
            else:
                items_arr = ['не найдено проверьте введённые данные']
                items_dep = ['не найдено проверьте введённые данные']

        context = {"items_dep": items_dep, "items_arr": items_arr}
        return render(request, 'cntx.html', context)
    else:
        form= From_to_form()
    return render(request, 'main.html', {
        "form": From_to_form
    })


    return render(request, 'main.html')

