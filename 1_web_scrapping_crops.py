import requests
from bs4 import BeautifulSoup
import pandas as pd
from lxml import html
import numpy as np
import time
import re

url_inicial = 'https://stardewvalleywiki.com/'

crops = url_inicial + 'Crops'
respuesta = requests.get(crops)

if respuesta.status_code == 200:
    tree = html.fromstring(respuesta.content)
    soup = BeautifulSoup(respuesta.text, 'html.parser')

h3_tags = soup.find_all('h3')
crops_names = []

for h3 in h3_tags:
    item_name = h3.find('a', title=True)
    if item_name and item_name.has_attr('title'):
        crops_names.append(item_name['title'])

tablas_precios_venta = soup.find_all('table', class_='no-wrap')
precios_list = []

for num, tabla in enumerate(tablas_precios_venta):
    celdas = tabla.find_all('td')
    precios = []
    for celda in celdas:
        texto = celda.get_text(strip=True)
        if texto.endswith('g'):
            precios.append(texto)
    if len(precios) != 0:
        precios_list.append(precios)

indexes = []

indexes.append(crops_names.index('Mixed Seeds'))
crops_names.remove('Mixed Seeds')
indexes.append(crops_names.index('Fiber'))
crops_names.remove('Fiber')
indexes.append(crops_names.index('Mixed Flower Seeds'))
crops_names.remove('Mixed Flower Seeds')
crops_names.remove('Crafting')

for precio in precios_list:
    if len(precio) != 4:
        while len(precio) != 4:
            precio.append(np.nan)

precios_compra = []

for table in range(3, 51):
    data = tree.xpath(f'/html/body/div[3]/div[3]/div[5]/div/table[{table}]/tbody/tr[2]/td[1]/div[2]/span[2]/text()')
    if data:
        precios_compra.append(data[0])
    else:
        precios_compra.append('Mision')

for index in indexes:
    precios_compra.pop(index)

buy_price = []

for price in precios_compra:
    precio = re.sub(r'\D', '', price)
    buy_price.append(precio)

tiempo = []

for table in range(3, 51):
    tiempos = list()

    growth = tree.xpath(f'/html/body/div[3]/div[3]/div[5]/div/table[{table}]/tbody/tr[3]/td[contains(text(), "Total")]/text()')
    regrowth = tree.xpath(f'/html/body/div[3]/div[3]/div[5]/div/table[{table}]/tbody/tr[3]/td[contains(text(), "Regrowth")]/text()[1]')

    try:
        if regrowth[0] == 'Regrowth:':
            regrowth = tree.xpath(f'/html/body/div[3]/div[3]/div[5]/div/table[{table}]/tbody/tr[3]/td[contains(text(), "Regrowth")]/text()[2]')
    except IndexError:
        pass

    if growth and regrowth:
        tiempos.append(growth)
        tiempos.append(regrowth)
        tiempo.append(tiempos)
    elif growth:
        tiempo.append(growth[0])
    else:
        tiempo.append(np.nan)

for index in indexes:
    tiempo.pop(index)

growth_time_list = []

for time in tiempo:
    if isinstance(time, str):
        dias = re.sub(r'\D', '', time)
        growth_time_list.append(dias)
    elif isinstance(time, list):
        time = time[0][0]
        dias = re.sub(r'\D', '', time)
        growth_time_list.append(dias)

regrowth_time_list = []

for time in tiempo:
    if isinstance(time, str):
        regrowth_time_list.append(np.nan)
    elif isinstance(time, list):
        time = time[1][0]
        dias = re.sub(r'\D', '', time)
        regrowth_time_list.append(dias)

crops_urls = [name.replace(' ', '_') for name in crops_names]
seasons = []

for crop in crops_urls:
    crop_url = url_inicial + crop
    respuesta = requests.get(crop_url)

    if respuesta.status_code == 200:
        tree = html.fromstring(respuesta.content)

    season = tree.xpath('/html/body/div[3]/div[3]/div[5]/div/div[1]/table/tbody/tr[td[contains(text(), "Season")]]/td[2]//span//a/text()')
    seasons.append(season)

    time.sleep(1)

for season in seasons:
    if 'Ginger Island' in season:
        season.remove('Ginger Island')
        season.remove('Summer')

category = ['Crop' for num in range(45)]

column_names = ['crop_name', 'category', 'season', 'growth_time', 'regrowth_time', 'buy_price', 'sell_price_standard', 'sell_price_silver', 'sell_price_gold', 'sell_price_iridium']

df = pd.DataFrame(index=range(45), columns=column_names)
df['crop_name'] = crops_names
df['category'] = category
df['season'] = seasons
df['season'] = df['season']
df['growth_time'] = growth_time_list
df['growth_time'] = df['growth_time'].astype(float)
df['regrowth_time'] = regrowth_time_list
df['regrowth_time'] = df['regrowth_time'].astype(float)
df['buy_price'] = buy_price
df.replace('', np.nan, inplace=True)
df['buy_price'] = df['buy_price'].astype(float)
df[['sell_price_standard', 'sell_price_silver', 'sell_price_gold', 'sell_price_iridium']] = precios_list
df[['sell_price_standard', 'sell_price_silver', 'sell_price_gold', 'sell_price_iridium']] = df[['sell_price_standard', 'sell_price_silver', 'sell_price_gold', 'sell_price_iridium']].map(lambda x: int(str(x).replace('g', '').replace(',', '')) if pd.notnull(x) else x)
df = df.explode('season', ignore_index=True)