import os
from dotenv import load_dotenv
import requests
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

load_dotenv() 
MAP_KEY = os.getenv("NASA_KEY")
SOURCE='VIIRS_NOAA21_NRT' # (str) 'VIIRS_NOAA21_NRT' & 'VIIRS_NOAA20_NRT' 
AREA_COORDINATES='-141,42,-53,83'  # (str) 'west,south,east,north'
DAY_RANGE='1' # (str) discrete value from '1' to '10'
DATE='' # (str) 'YYYY-MM-DD' or empty

def save_to_sqlite(df, table_name):
    engine = create_engine('sqlite:///firms_data.db')
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    print(table_name,' saved successfully.')

try:
    status_url = 'https://firms.modaps.eosdis.nasa.gov/mapserver/mapkey_status/?MAP_KEY=' + MAP_KEY
    response = requests.get(status_url) #Fetching status
    data = response.json()
    df = pd.Series(data)
    print(df)
except:
    print('Error: Invalid NASA Key or unable to connect to the service.')

try:
    area_url = 'https://firms.modaps.eosdis.nasa.gov/api/area/csv/' + MAP_KEY + '/' + SOURCE + '/' + AREA_COORDINATES + '/' + DAY_RANGE + '/' + DATE
    df = pd.read_csv(area_url) # Fetching data 
    print(df.head())
    data_name = datetime.now().strftime('%Y%m%d_%H%M%S'+'_' + SOURCE + '_' + AREA_COORDINATES.replace(',','_') + '_' + DAY_RANGE + '_' + DATE)
    save_to_sqlite(df, data_name)
except:
    print('Error: Unable to fetch data for source:', SOURCE)


