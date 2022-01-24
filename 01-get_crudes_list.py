# Scrapes crudemonitor.ca to get the list of all crudes (except Condensates) and stores them in crudes_list.csv
import os
from scraper_funcs import *


# Base url to crudemonitor.ca
base_url = 'https://crudemonitor.ca/'

# Scrape crudemonitor.ca and store the crudes list in crudes_list.csv
fname = 'crudes_list.csv'
if not os.path.isfile(fname):
    crude_list_fn(base_url_in=base_url).to_csv('crudes_list.csv')
    print('File Saved!')
else:
    print('Nothing to do!')
