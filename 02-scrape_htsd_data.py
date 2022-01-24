# Scrapes the High-Temperature Simulation Data (HTSD) from crudemonitor.ca for each crude and store it in ./data/
import os
from scraper_funcs import *


# Base url to crudemonitor.ca
base_url = 'https://crudemonitor.ca/'

# Read the list of crudes from crudes_list.csv
crudes = pd.read_csv('crudes_list.csv').drop('Unnamed: 0', axis=1)

for name, abbr in zip(crudes['name'].values, crudes['abbr'].values):
    fname_csv = f'data/htsd_{name.replace(" ", "_")}_{abbr}.csv'
    if not os.path.isfile(fname_csv):
        crude_htsd = crude_info_fn(base_url_in=base_url, crude_abbr_in=abbr)
        crude_htsd.to_csv(fname_csv)
        print(f'{name.replace(" ", "_")}\t{abbr}')
