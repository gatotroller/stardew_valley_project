import requests
from bs4 import BeautifulSoup
import pandas as pd
from lxml import html
import numpy as np

url_inicial = 'https://stardewvalleywiki.com/'

fruit_trees = url_inicial + 'Fruit_Trees'
respuesta = requests.get(fruit_trees)

if respuesta.status_code == 200:
    tree = html.fromstring(respuesta.content)
    soup = BeautifulSoup(respuesta.text, 'html.parser')

fruits = []
buy_price_list = []
sell_prices_list = []

for table in range(2, 17, 2):
    position = tree.xpath(f'/html/body/div[3]/div[3]/div[5]/div/table[{table}]/tbody/tr[1]/th[3]/text()')

    if position:
        if position[0] == 'Fruit\n':
            td_pos = 3
        else:
            td_pos = 4

    fruit_name = tree.xpath(f'/html/body/div[3]/div[3]/div[5]/div/table[{table}]/tbody/tr[2]/td[{td_pos}]/span/a/text()')
    if fruit_name:
        fruits.append(fruit_name[0])

    buy_price = tree.xpath(f'/html/body/div[3]/div[3]/div[5]/div/table[{table}]/tbody/tr[2]/td[2]/span[2]/text()')
    if buy_price and buy_price[0].endswith('g'):
        buy_price = buy_price[0]
        buy_price_list.append(buy_price[:buy_price.find('g')])
    else:
        buy_price_list.append('0')

    sell_price_l = []
    sell_price_rows = tree.xpath(f'/html/body/div[3]/div[3]/div[5]/div/table[{table}]/tbody/tr[2]/td[{td_pos + 1}]/table/tbody/tr')
    
    for row in sell_price_rows:
        sell_price = row.xpath('./td[2]/text()')[0]
        sell_price_l.append(sell_price[:sell_price.find('g')])
    sell_prices_list.append(sell_price_l)

category = ['Fruit Trees' for _ in range(len(fruits))]
growth_time = [28 for _ in range(len(fruits))]
regrowth_time = [1 for _ in range(len(fruits))]

column_names = ['fruit_name', 'category', 'growth_time', 'regrowth_time', 'buy_price', 'sell_price_standard', 'sell_price_silver', 'sell_price_gold', 'sell_price_iridium']
fruits_df = pd.DataFrame(columns=column_names)

fruits_df['fruit_name'] = fruits
fruits_df['category'] = category
fruits_df['growth_time'] = growth_time
fruits_df['regrowth_time'] = regrowth_time
fruits_df['buy_price'] = buy_price_list
fruits_df[['sell_price_standard', 'sell_price_silver', 'sell_price_gold', 'sell_price_iridium']] = sell_prices_list

fruits_df['buy_price'] = fruits_df['buy_price'].str.replace(',', '').astype('float').replace(0, np.nan)
fruits_df['sell_price_standard'] = fruits_df['sell_price_standard'].astype('float')
fruits_df['sell_price_silver'] = fruits_df['sell_price_silver'].astype('float')
fruits_df['sell_price_gold'] = fruits_df['sell_price_gold'].astype('float')
fruits_df['sell_price_iridium'] = fruits_df['sell_price_iridium'].astype('float')