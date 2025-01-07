from sqlalchemy import create_engine

from web_scrapping_crops import df_crops
from web_scrapping_animals import df_animals
from web_scrapping_fruit_trees import df_fruits
from web_scrapping_artifacts import df_artifacts
from web_scrapping_minerals import df_minerals
from web_scrapping_fish import df_fish
from web_scrapping_foraging import df_harvest

crops = df_crops()
animals = df_animals()
fruit = df_fruits()
artifacts = df_artifacts()
minerals = df_minerals()
fish = df_fish()
harvest = df_harvest()

server = r'GATOTROLLER\SQLEXPRESS'
database = 'stardew_v_raw'
driver = 'ODBC Driver 17 for SQL Server'

connection_string = f"mssql+pyodbc://{server}/{database}?trusted_connection=yes&driver={driver}"
engine = create_engine(connection_string)

crops.to_sql("crops", engine, if_exists="replace", index=False)
animals.to_sql("animals", engine, if_exists="replace", index=False)
fruit.to_sql("fruit", engine, if_exists="replace", index=False)
artifacts.to_sql("artifacts", engine, if_exists="replace", index=False)
minerals.to_sql("minerals", engine, if_exists="replace", index=False)
fish.to_sql("fish", engine, if_exists="replace", index=False)
harvest.to_sql("harvest", engine, if_exists="replace", index=False)