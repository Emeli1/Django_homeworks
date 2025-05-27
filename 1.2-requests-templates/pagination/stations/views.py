import csv

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse

from pagination.settings import BASE_DIR, BUS_STATION_CSV


def index(request):
    return redirect(reverse('bus_stations'))

def read_csv():
    info = []

    with open(BUS_STATION_CSV, encoding='utf-8') as f:
        r = csv.reader(f)
        for el in r:
            if el[1] != 'Name' or el[4] != 'Street' or el[6] != 'District':
                info.append({
                    'Name': el[1],
                    'Street': el[4],
                    'District': el[6]
                })
    return info

# var 2
# csv.DictReader(f) в Python создаёт объект,
# который читает данные из CSV-файла и преобразует их в формат словаря.
# with open(settings.BUS_STATION_CSV, newline='', encoding="utf-8") as f:
#     csv_data = csv.DictReader(f)
#     bus_stations_list = []
#     for row in csv_data:
#         bus_stations_list.append(row)

def bus_stations(request):
    # получите текущую страницу и передайте ее в контекст
    # также передайте в контекст список станций на странице

    info = read_csv()

    pagi = Paginator(info, 10)
    current_page = int(request.GET.get('page', 1))
    page = pagi.get_page(current_page)

    context = {
        'bus_stations': page.object_list,
        'page': page,
    }
    return render(request, 'stations/index.html', context)


