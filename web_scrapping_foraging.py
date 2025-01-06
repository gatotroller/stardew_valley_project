import requests
import pandas as pd
from lxml import html
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def df_harvest():

    url_inicial = 'https://stardewvalleywiki.com/'

    foraging = url_inicial + 'Foraging'
    respuesta = requests.get(foraging)

    if respuesta.status_code == 200:
        tree = html.fromstring(respuesta.content)

    driver = webdriver.Chrome()
    driver.get(foraging)

    foraging_name_list  = []
    sell_price_list = []

    for table in range(5, 13):
        rows = tree.xpath(f'/html/body/div[3]/div[3]/div[5]/div/table[{table}]/tbody/tr[position() > 1]')
        td_pos_condition = f'/html/body/div[3]/div[3]/div[5]/div/table[{table}]/thead/tr/th[3]'
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, td_pos_condition)))
        contenido = element.text

        if 'Found' in contenido:
            td_pos = 4
        else:
            td_pos = 3

        for row in rows:
            crop_name = row.xpath('./td[2]/a/text()')
            if crop_name:
                foraging_name_list.append(crop_name[0])
            
            prices_rows = row.xpath(f'./td[{td_pos}]/table/tbody/tr')
            sell_prices = []

            for price_row in prices_rows:
                price = price_row.xpath('./td[2]/text()')
                if price:
                    price = price[0]
                    price = price[:price.find('g')]
                    sell_prices.append(float(price))
            
            while len(sell_prices) != 4:
                sell_prices.append(np.nan)
            
            sell_price_list.append(sell_prices)

    driver.quit()

    categories = ['harvesting' for _ in range(len(foraging_name_list))]

    column_names = [['crop_name', 'category', 'sell_price_standard', 'sell_price_silver', 'sell_price_gold', 'sell_price_iridium']]
    harvest_df = pd.DataFrame(columns=column_names)

    harvest_df['crop_name'] = foraging_name_list
    harvest_df['category'] = categories
    harvest_df[['sell_price_standard', 'sell_price_silver', 'sell_price_gold', 'sell_price_iridium']] = sell_price_list

    return harvest_df