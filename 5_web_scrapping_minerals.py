import requests
import pandas as pd
from lxml import html
import numpy as np

url_inicial = 'https://stardewvalleywiki.com/'

minerals = url_inicial + 'Minerals'
respuesta = requests.get(minerals)

if respuesta.status_code == 200:
    tree = html.fromstring(respuesta.content)

minerals = []
sell_price_list = []

for table in range(1, 5):
    rows = tree.xpath(f'/html/body/div[3]/div[3]/div[5]/div/table[{table}]/tbody/tr[position() > 1]')

    for row in rows:
        mineral_name = row.xpath('./td[2]/a/text()')
        sell_price = row.xpath('./td[4]/span[2]/text()')

        minerals.append(mineral_name[0] if mineral_name else np.nan)
        if sell_price:
            sell_price = sell_price[0].replace('g', '').strip()
            sell_price = sell_price.replace(',', '')
            sell_price_list.append(float(sell_price))

categories = ['Mineral' for _ in range(len(minerals))]

column_names = [['mineral_name', 'category', 'sell_price']]
mineral_df = pd.DataFrame(columns=column_names)

mineral_df['mineral_name'] = minerals
mineral_df['category'] = categories
mineral_df['sell_price'] = sell_price_list