import requests
from bs4 import BeautifulSoup
import pandas as pd
from lxml import html
import numpy as np

url_inicial = 'https://stardewvalleywiki.com/'

animals = url_inicial + 'Animals'
respuesta = requests.get(animals)

if respuesta.status_code == 200:
    tree = html.fromstring(respuesta.content)
    soup = BeautifulSoup(respuesta.text, 'html.parser')

animales = []
costos = []
ventas = []
productos = []

for table in range(2, 11):
    rows = tree.xpath(f'/html/body/div[3]/div[3]/div[5]/div/table[{table}]/tbody/tr[position() > 1]')
    for row in rows:
        name = row.xpath('./td[2]/a/text()')
        costo = row.xpath('./td[3]/span[2]/text()')
        
        prod = []
        prod1 = row.xpath('./td[4]/a[2]/text()')
        prod2 = row.xpath('./td[4]/a[4]/text()')

        if prod1:
            prod.append(prod1[0])
            if prod2:
                prod.append(prod2[0])
        else:
            prod1 = row.xpath('./td[5]/a[2]/text()')
            prod2 = row.xpath('./td[5]/a[4]/text()')
            if prod1:
                prod.append(prod1[0])
                if prod2:
                    prod.append(prod2[0])
            else:
                prod1 = row.xpath('./td[position()=4 or position()=5]/span[1]/a/text()')
                prod2 = row.xpath('./td[position()=4 or position()=5]/span[4]/a/text()')
                if prod1:
                    prod.append(prod1[0])
                if prod2:
                    prod.append(prod2[0])

        productos.append(prod)
        animales.append(name[0])
        if costo:
            costos.append(costo[0])
        else:
            costos.append('0')

for table in range(2, 6):
    rows = tree.xpath(f'/html/body/div[3]/div[3]/div[5]/div/table[{table}]/tbody/tr[position() > 1]')
    for row in rows:
        vent = []
        vent1 = row.xpath('./td[4]/span[2]/text()')
        vent2 = row.xpath('./td[4]/span[4]/text()')

        if not vent1:
            vent1 = row.xpath('./td[5]/span[2]/text()')
            vent2 = row.xpath('./td[5]/span[4]/text()')
       
        vent.append(vent1[0])
        if vent2:
            vent.append(vent2[0])
        ventas.append(vent)

for table in range(6, 11):
    rows = tree.xpath(f'/html/body/div[3]/div[3]/div[5]/div/table[{table}]/tbody/tr[position() > 1]')
    for row in rows:
        vent = []
        vent1 = row.xpath('./td[4]/span[3]/text()')
        vent2 = row.xpath('./td[4]/span[6]/text()')
        
        if not vent1:
            vent1 = row.xpath('./td[5]/span[3]/text()')
            vent2 = row.xpath('./td[5]/span[6]/text()')

        if vent1:
            vent.append(vent1[0])
        if vent2:
            vent.append(vent2[0])
        ventas.append(vent)
        
costos = [costo.replace('g', '') for costo in costos]
ventas = [[item.replace('g', '') for item in sublist] for sublist in ventas]

categorias = ['Animal' for _ in range(len(animales))]
column_names = ['animal_name', 'category', 'cost', 'produce', 'sell_price']
animal_df = pd.DataFrame(columns=column_names)

animal_df['animal_name'] = animales
animal_df['category'] = categorias
animal_df['cost'] = costos
animal_df['produce'] = productos
animal_df['sell_price'] = ventas
animal_df['cost'] = animal_df['cost'].replace('0', np.nan)
animal_df['cost'] = animal_df['cost'].str.replace(',', '').astype(float)

animal_df.drop_duplicates(['animal_name'], inplace=True)
animal_df.reset_index(drop=True, inplace=True)
animal_df = animal_df.explode(['produce', 'sell_price'], ignore_index=True)
animal_df['sell_price'] = animal_df['sell_price'].str.replace(',', '').astype(float)