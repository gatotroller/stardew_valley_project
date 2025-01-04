import requests
import pandas as pd
from lxml import html
import numpy as np

url_inicial = 'https://stardewvalleywiki.com/'

fish = url_inicial + 'Fish'
respuesta = requests.get(fish)

if respuesta.status_code == 200:
    tree = html.fromstring(respuesta.content)

fish_name_list = []
sell_price_list = []

for table in range(1, 7):
    rows = tree.xpath(f'/html/body/div[3]/div[3]/div[5]/div/table[{table}]/tbody/tr[position() > 1]')

    for row in rows:
        fish_name = row.xpath('./td[2]/a/text()')
        if fish_name:
            fish_name_list.append(fish_name[0])

        prices_rows = row.xpath('./td[4]/table/tbody/tr')
        sell_prices = []
        for price_row in prices_rows:
            sell_price = price_row.xpath('./td[2]/text()')
            if sell_price:
                sell_price = sell_price[0]
                sell_price = sell_price[:sell_price.find('g')]
                sell_price = sell_price.replace(',', '')
                sell_prices.append(float(sell_price))
        if len(sell_prices) == 0:
            sell_price = row.xpath('./td[4]/span[2]/text()')
            if sell_price:
                sell_price = sell_price[0]
                sell_price = sell_price[:sell_price.find('g')]
                sell_price = sell_price.replace(',', '')
                sell_prices.append(float(sell_price))
        if len(sell_prices) > 0:
            sell_price_list.append(sell_prices)

for prices in sell_price_list:
    while len(prices) != 4:
        prices.append(np.nan)

categories = ['fish' for _ in range(len(fish_name_list))]

column_names = [['fish_name', 'category', 'sell_price_standard', 'sell_price_silver', 'sell_price_gold', 'sell_price_iridium']]
fish_df = pd.DataFrame(columns=column_names)

fish_df['fish_name'] = fish_name_list
fish_df['category'] = categories
fish_df[['sell_price_standard', 'sell_price_silver', 'sell_price_gold', 'sell_price_iridium']] = sell_price_list