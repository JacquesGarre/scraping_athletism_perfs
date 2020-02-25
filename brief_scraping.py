import requests
import bs4 as BeautifulSoup
import os
import sys
import pandas as pd 
import time



def get_el_by_pos(html_content, element, position):
    soup = BeautifulSoup.BeautifulSoup(str(html_content), 'html.parser')
    return soup.find_all(element)[position]






# ===============================================================================================
#                             TRIPLE JUMP // 25 BEST // MEN
# ===============================================================================================

# url = 'http://trackfield.brinkster.net/25BestPerf.asp?EventCode=MF4&P=F'
# html = requests.get(url).text

dir_path = os.path.dirname(os.path.realpath(__file__))
txt = os.path.join(dir_path, "html.txt")
html = open(txt, "r").read()

table = get_el_by_pos(html, 'table', 4) # 5e balise <table> du DOM
rows = table.find_all('tr')[2:] # Exclusion des 2 premiers rows inutiles

performances = []
names = []
countries = []
cities = []
dates = []

for row in rows:
    performances.append(get_el_by_pos(row, 'td', 1).get_text())
    names.append(get_el_by_pos(row, 'td', 5).find('a').get_text())
    countries.append(get_el_by_pos(row, 'td', 6).get_text())
    cities.append(get_el_by_pos(row, 'td', 7).get_text())
    dates.append(get_el_by_pos(row, 'td', 8).get_text())

best_performances_of_triple_jump_men = pd.DataFrame({
    'names':names,
    'performances':performances,
    'countries': countries,
    'cities': cities,
    'dates': dates
})

# print(best_performances_of_triple_jump_men)








# ===============================================================================================
                    # 25 meilleures performances de l’année 1891 à 2019 en
                    # triple saut homme et femme dans un fichier Excel.
# ===============================================================================================

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

params = get_http_params(get_combinations_of_params())
dir_path = os.path.dirname(os.path.realpath(__file__))
txt = os.path.join(dir_path, "http_params.txt")
fichier = open(txt,'w') 
fichier.write(str(params))
fichier.close()

base_url = 'http://trackfield.brinkster.net/More.asp'

running = True
i = 0
x = 10
tries = 0
while(running):
    if(i == len(params)-1):
        running = False
    print('\n========================================\n')
    url = base_url + params[i]
    try:
        print('URL N°', i, '/', len(params)-1, ' : ', url)
        response = requests.get(url)
        print(response.status_code)
        # soup = BeautifulSoup.BeautifulSoup(response.text, 'html.parser')
        # dir_path = os.path.dirname(os.path.realpath(__file__))
        # txt = os.path.join(dir_path, param + '_' +  i + ".txt")
        # file = open(txt,'w') 
        # file.write(soup.find('table')) 
        # file.close()
        i += 1
    except:
        if tries > 2:
            print('An error occured, tried more than 2 times, passing...')
            i += 1
            tries = 0
        else:
            print('An error occured... Retrying in ', x, 'seconds')
            tries += 1
        time.sleep(x)
    

print('END.')

 