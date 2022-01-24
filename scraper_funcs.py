# Functions to scrape th High-Temperature Simulated Distillation (HTSD) data for a crude
# import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup


def crude_list_fn(base_url_in):
    """
    Takes the base_url to the crudemonitor website and retrieves the list of all crudes (except 'Condensates')
    :param base_url_in: str -> base_url to the crudemonitor webpage
    :return: Pandas DataFrame -> Pandas DataFrame of crude names ('name') and abbreviation ('abbr')
    """

    # SEND REQUEST TO 'crudemonitor.ca/home.php'
    html = requests.get(base_url_in + '/home.php').text

    # GET THE BeautifulSoup OBJECT ('lxml' PARSING)
    soup = BeautifulSoup(html, 'lxml')

    # GET THE DIVISION ELEMENTS (div) FOR DIFFERENT CRUDE TYPES
    divs = soup.find_all('div', {'class': ['el-container']})

    # LOOP OVER EACH CRUDE CATEGORY TO GET A SINGLE CRUDE OIL AT A TIME (HERE LOOP RESTRICTED TO THE FIRST CATEGORY)
    crude_list = []
    for div in divs[1:]:
        if div:
            divs_crude = div.find_all('div')
            for _div in divs_crude[1:]:
                crude_str = _div.find('p', {'class': 'no-padding'}).text.rstrip(')').lstrip('▸ ').strip().split('(')
                crude_list.append({'name': crude_str[0].strip(),
                                   'abbr': crude_str[-1].strip()})
            _df = pd.DataFrame(crude_list)
            return _df


if __name__ == '__main__':

    base_url = 'https://crudemonitor.ca/'
    my_df = crude_list_fn(base_url_in=base_url)
    print(my_df.head(10))
