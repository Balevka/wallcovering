import time

import requests
from bs4 import BeautifulSoup as bs
import re

start_page = "https://www.mosoboi.ru/oboi/bumazhnye/"
base_url = "https://www.mosoboi.ru"
headers={'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 OPR/73.0.3856.415 (Edition Yx GX)'}

wallcovering_links = []
wallcoverings = {}
count = 0

# Проверка записи ссылок в список

def check():
  for item in wallcovering_links:
    print(item)

# Поиск ссылок в каталоге

def get_links(start_page, headers):
  session = requests.Session()

  try:
    request = session.get(start_page, headers = headers)
    request.raise_for_status()
    if request.status_code == 200:
      print('Status 200')
    soup = bs(request.content, 'html.parser')
    links = soup.find_all('div', {'class': 'product-item'})
    for item in links:
      link = str(base_url + item['data-product-click'])
      if link not in wallcovering_links:
          wallcovering_links.append(link)

  except requests.exceptions.HTTPError as err:
    raise SystemExit(err)

# Получение данных

def get_data(links, headers, count):
  name = ''
  price = ''
  companions = {}
  other_colors = {}

  # Список названий характеристик
  properties_list = []

  # Список значений характеристик
  values_list = []

  session = requests.Session()
  for link in links:
    try:
      count+=1
      request = session.get(link, headers=headers)
      request.raise_for_status()

      # Проверка соединения
      if request.status_code == 200:
         print('Status 200')

      # Парсинг
      soup = bs(request.content, 'html.parser')

      # Название
      item_name = soup.find('h1', {'id': 'h1-pages'}).text
      name = re.sub(r'\s+', ' ', item_name)
      print(name)

      # Цена
      block = soup.find('div',{'class': 'today-price'})
      price = block.findChild('span').text
      print(price)

      # Харакатеристики
      specifications = soup.find('div', {'class': 'properties tab-info js-tab-info active'})

      properties = specifications.findChildren('div',{'class': 'tab-content-left'})

      for prop in properties:
        text = prop.text
        if text not in properties_list:
          properties_list.append(text)
        print(text)

      # Значение характеристик
      values = specifications.findChildren('span',{'class': 'normal'})
      for value in values:
        text = re.sub(r'\s+', ' ', value.text)
        text = text.split('?')[0]
        if text not in  values_list:
          values_list.append(text)
        print(text)

      # Компаньоны
      try:
        carousel = soup.find('div', {'class': 'head-left pull-left'})
        blocks = carousel.findChildren('div', {'class': 'block interior-carousel-block'})
        x = 0
        for item in blocks:
          companion_name = item['data-name']
          companion_articul = item['data-articul']
          x+=1
          dict = {f'color{x}':{f'{companion_name}':f'{companion_articul}'}}
          companions.update(dict)
          print( companion_name + ' ' + companion_articul)


      except Exception:
        companion_name = 'NULL'
        companion_articul = 'NULL'
        print(Exception)

      # Другие цвета

      try:
        carousel = soup.find('div', {'class': 'head-center pull-left'})
        blocks = carousel.findChildren('div', {'class': 'block interior-carousel-block'})
        x=0
        for item in blocks:
          color_name = item['data-name']
          color_articul = item['data-articul']
          x+=1
          dict = {f'color{x}':{f'{color_name}':f'{color_articul}'}}
          other_colors.update(dict)
          print(color_name + ' ' + color_articul)
          #print(dict)

      except Exception:
        companion_name = 'NULL'
        companion_articul = 'NULL'
        print(Exception)

      time.sleep(1)
    # Ловим ошибки

    except requests.exceptions.HTTPError as err:
      raise SystemExit(err)

def main():

  get_links(start_page, headers)
# check()
  get_data(wallcovering_links, headers, count)

main()
print('links' + len(wallcovering_links))
print('amount' + count)