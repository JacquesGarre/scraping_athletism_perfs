import requests
import bs4 as BeautifulSoup
import os
import sys
import pandas as pd 
import time
import urllib3
import csv

# ===============================================================================================
                    # 25 meilleures performances de l’année 1891 à 2019 en
                    # toutes disciplines confondues, dans un fichier Excel.
# ===============================================================================================

def get_el_by_pos(html_content, element, position):
    soup = BeautifulSoup.BeautifulSoup(str(html_content), 'html.parser')
    return soup.find_all(element)[position]

def get_event_codes():
    url = 'http://trackfield.brinkster.net/Main.asp?P=F'
    html = requests.get(url).text
    soup = BeautifulSoup.BeautifulSoup(html, 'html.parser')
    men_table = get_el_by_pos(soup, 'table', 3)
    women_table = get_el_by_pos(soup, 'table', 4)
    men_links = men_table.find_all('a')
    women_links = women_table.find_all('a')
    hrefs = []
    for href in men_links + women_links:
        hrefs.append(href['href'].replace('events.asp?EventCode=', '').replace('&P=F', ''))
    return hrefs

def get_combinations_of_params():
    # ?Year=2019&EventCode=MA1&Gender=M
    params = {
        'Year': range(1891,2020),
        'Gender': ['M', 'F'], # Inutile après analyse des event codes
        'EventCode':  ['MA1', 'MA0', 'MA2', 'MA3', 'MA4', 'MA5', 'MA6', 'MA7', 'MA8', 'MA9', 'MB1', 'MB2', 'MB3', 'MC1', 'MC2', 'MC3', 'ME1', 'ME2', 'MF1', 'MF2', 'MF3', 'MF4', 'MF5', 'MF6', 'MF7', 'MF8', 'MF9', 'WA1', 'WA2', 'WA3', 'WA4', 'WA5', 'WA6', 'WA7', 'WA8', 'WA9', 'WB1', 'WB2', 'WB3', 'WC1', 'WC2', 'WE1', 'WE2', 'WE3', 'WF1', 'WF2', 'WF3', 'WF4', 'WF5', 'WF6', 'WF7', 'WF8', 'WF9']  
    }
    combinations = []
    for year in params['Year']:
        for event_code in params['EventCode']: 
            combinations.append([year, event_code])
    return combinations

def get_http_params(combinations):
    params = []
    for combination in combinations:
        http_params = '?Year=' + str(combination[0]) + '&EventCode=' + str(combination[1])
        params.append(http_params)
    return params

def write_params_to_file(params):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    txt = os.path.join(dir_path, "http_params.txt")
    fichier = open(txt,'w') 
    fichier.write(str(params))
    fichier.close()

def write_table_to_csv(html, title):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    csv_file = os.path.join(dir_path, title+'.csv')
    f = csv.writer(open(csv_file, "w", encoding="utf-8", newline=''))
    table = get_el_by_pos(html, 'table', 0)
    rows = table.find_all('tr')[2:]
    for row in rows:
        f.writerow([row.get_text().replace('\n', ';').replace(',','')])


i = 0
x = 20 # délai entre les essais
tries = 0
params = get_http_params(get_combinations_of_params())
base_url = 'http://trackfield.brinkster.net/More.asp'
running = True
while(running):

    if(i == len(params)-1):
        running = False

    print('\n========================================\n')
    url = base_url + params[i]

    try:
        response = requests.get(url)
    except (ConnectionError, ConnectionResetError, urllib3.exceptions.ProtocolError, requests.exceptions.ConnectionError):
        print('Connection aborted... Trying again in {} seconds'.format(x))
        time.sleep(x)
        continue

    print('Url N°', i, '/',len(params))
    if response.status_code == 200:
        print('Scraping...')
        write_table_to_csv(response.text, params[i].replace('?Year=','').replace('&EventCode=','_'))  
        i += 1
    elif response.status_code == 404 or response.status_code == 403:
        print('http error code 404, passing url "{}"...'.format(url))
        i += 1
    elif response.status_code == 500 or response.status_code == 503:
        print('http error code 500, retrying in {} seconds...'.format(x*6))
        time.sleep(x*6)

print('THE END.')

 
#              _( }        
#        _  <<  \
#       `.\__/`/\\        ** Getting a new world record of most csv files created on a computer... **
#         '--'\\  `
#             //
#             \)                    