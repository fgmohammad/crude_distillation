# Functions to scrape th High-Temperature Simulated Distillation (HTSD) data for a crude
import numpy as np
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


def crude_info_fn(base_url_in, crude_abbr_in):
    """
    Takes the base_url for the crudemonitor website and the crude abbreviation and retrieves
    the High-Temperature Simulated Distillation (HTSD) table for the 1st crude
    :param base_url_in: str -> base_url to the crudemonitor webpage
    :param crude_abbr_in: str -> crude abbreviation
    :return: Pandas DataFrame containing HTSD data
    """

    # url TO THE CRUDE HDST PAGE
    url_htsd = base_url_in + f'/crudes/dist.php?acr={crude_abbr_in}&time=recent'

    # GET THE HTSD DATA IN A Pandas DataFrame FORMAT
    _df = htsd_fn(url_htsd)

    return _df


def htsd_fn(url):
    """
    Takes the url to HTSD data for a given crude, reads the values from the HTSD table and put them in a Pandas
    DataFrame
    :param url: str ->  url to the crude HTSD data
    :return: Pandas DataFrame with HTSD data
    """

    # GET THE WEBPAGE WITH HTSD DATA
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')

    # GET THE TABLE DIVISION
    div_tbl = soup.find('div', {'id': 'tblData'})

    # GET THE TABLE BODY
    tab_body = div_tbl.find('tbody')

    # GET THE TABLE ROWS
    trs = tab_body.find_all('tr')

    # LOOP OVER ALL ROWS (EXCEPT THE 1ST FOR IBP), READ MASS FRACTIONS, TEMPERATURE VALUES AND PUT THEM IN A
    # LIST OF DICTIONARIES dict_list
    dict_list = []
    for tr in trs:
        tds = tr.find_all('td', {'class': 'celsius'})
        my_dict = {'mass [%]': tr.find('th').text.replace('IBP', '0'),
                   'T_recent [C]': tds[0].text,
                   'T_avg [C]': tds[1].text,
                   'T_std [C]': tds[0].text
                   }
        dict_list.append(my_dict)

    # GET HTSD DATA INTO A Pandas DataFrame
    _df = pd.DataFrame(dict_list)

    # FOR SOME CRUDES THE ROW FOR 99% OF MASS RECOVERED IS EMPTY, SET THE VALUES HERE TO np.nan
    _df.loc[_df['T_recent [C]'] == '-', 'T_recent [C]'] = np.nan
    _df.loc[_df['T_avg [C]'] == '-', 'T_avg [C]'] = np.nan
    _df.loc[_df['T_std [C]'] == '-', 'T_std [C]'] = np.nan
    _df = _df.astype('float')
    return _df


if __name__ == '__main__':

    # Base url to crudemonitor.ca
    base_url = 'https://crudemonitor.ca/'
    my_df = crude_info_fn(base_url_in=base_url, crude_abbr_in='P')
    print(my_df.head(20))
