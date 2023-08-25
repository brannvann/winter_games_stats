#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import matplotlib.pyplot as plt

safe_headers = {
	'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'
}
all_datafile = 'winter_data.json'
ski_datafile = 'ski_data.json'

def process_data(yearurl, table_index_function, last_year:int = 2023):
    medals = {}
    years = [y for y in range(1956, 1993, 4)] + [y for y in range(1994, last_year, 4)]
    for year in years:
        url = yearurl.replace('year', str(year))
        try:
            req = urllib.request.Request( url, data=None, headers=safe_headers)
            html = urlopen(req)
            page = str(html.read().decode('utf-8'))
            bs = BeautifulSoup(page, 'html.parser')
            tables = bs.find_all('tbody')
            table_index = table_index_function(year)
            medal_table = tables[ table_index ]
            rows = medal_table.findAll('tr')
            last_row = rows[-1]
            total_medals = int(last_row.findAll('td')[-1].contents[0])
            nations = [] 
            for row in rows[1:-1]:
                country = row.th.a.contents[0]
                country_medals = row.findAll('td')[-1].contents[0]
                print(f"{year} : {country} {country_medals}")
                nations.append( (country, int(country_medals)) )
            pass
            medals[year] = { 'total' : total_medals, 'nations' : nations }
        except Exception as e:
            print(f"error: {str(e)}")
        pass
    pass
    return medals

def read_medals_data(filename:str):
    medals = {}
    try:
        with open(filename, "r") as ifs:
            medals = json.load(ifs)
    except:
        medals = None
    return medals

def draw_medals_plot(medals, title:str):
    labels = []
    total, rus = [], []
    for year, data in medals.items():
        labels.append(year)
        total.append(data['total'])
        rus_medals = [ c[1] for c in data['nations'] if c[0] in ['Soviet Union', 'Unified Team', 'Russia', 'Olympic Athletes from Russia', 'ROC'] ]
        rus.append(rus_medals[0] if rus_medals else 0 )
    pass
    _,m = plt.subplots()
    m.set_ylabel('Количество медалей', fontsize=16)
    m.set_title(title, fontsize=16)
    m.bar(labels, total, label='Все страны', color='Navy')
    m.bar(labels, rus, label='СССР, РФ', color='Red')
    m.legend(fontsize=16)
    plt.xticks(range(len(labels)), labels, rotation=60)
    plt.show()
    return

def main(args):
    all_medals = read_medals_data(all_datafile)
    if not all_medals:
        games_url = "https://en.wikipedia.org/wiki/year_Winter_Olympics_medal_table"
        all_medals = process_data(games_url, table_index_function = lambda y : 2 if y < 1992 else 3)
        with open(all_datafile, "w") as ofs:
            json.dump(all_medals, ofs)
    pass
    ski_medals = read_medals_data(ski_datafile)
    if not ski_medals:
        ski_url = "https://en.wikipedia.org/wiki/Cross-country_skiing_at_the_year_Winter_Olympics"
        ski_medals = process_data(ski_url, table_index_function = lambda y : 2 if y < 2014 else 3)
        with open(ski_datafile, "w") as ofs:
            json.dump(ski_medals, ofs)
    pass
    draw_medals_plot(all_medals, 'Медали зимних Олимпийских игр')
    draw_medals_plot(ski_medals, 'Медали зимних Олимпийских игр в лыжном спорте')
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
	