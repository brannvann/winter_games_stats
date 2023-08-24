#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json

safe_headers = {
	'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'
}
datafile = 'winter_data.json'

def process_winter_games(last_year:int = 2023):
    medals = {}
    years = [y for y in range(1956, 1993, 4)] + [y for y in range(1994, last_year, 4)]
    for year in years:
        url = f"https://en.wikipedia.org/wiki/{year}_Winter_Olympics_medal_table"
        try:
            req = urllib.request.Request( url, data=None, headers=safe_headers)
            html = urlopen(req)
            page = str(html.read().decode('utf-8'))
            bs = BeautifulSoup(page, 'html.parser')
            tables = bs.find_all('tbody')
            medal_table = tables[ 2 if year < 1992 else 3 ]
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


def main(args):
    medals = process_winter_games()
    with open(datafile, "w") as ofs:
        json.dump(medals, ofs)
    print(medals)

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
	