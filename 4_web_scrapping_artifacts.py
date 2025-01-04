import requests
import pandas as pd
from lxml import html
import numpy as np

url_inicial = 'https://stardewvalleywiki.com/'

artifacts = url_inicial + 'Artifacts'
respuesta = requests.get(artifacts)

if respuesta.status_code == 200:
    tree = html.fromstring(respuesta.content)

artifacts = []
sell_price_list = []

rows = tree.xpath('/html/body/div[3]/div[3]/div[5]/div/table[1]/tbody/tr[position() > 1]')

for row in rows:
    artifact_name = row.xpath('./td[2]/a/text()')
    artifacts.append(artifact_name[0] if artifact_name else np.nan)

    sell_price = row.xpath('./td[4]/span[2]/text()')
    if sell_price:
        sell_price = sell_price[0].replace('g', '').strip()
        sell_price = sell_price.replace(',', '')
        sell_price_list.append(float(sell_price))
    else:
        sell_price_list.append(np.nan)

categories = ['artifact' for _ in range(len(artifacts))]

column_names = [['artifact_name', 'category', 'sell_price']]
artifacts_df = pd.DataFrame(columns=column_names)

artifacts_df['artifact_name'] = artifacts
artifacts_df['category'] = categories
artifacts_df['sell_price'] = sell_price_list