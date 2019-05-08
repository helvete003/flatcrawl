#!/usr/bin/env python3
import csv
from crawler import Crawler
from bs4 import BeautifulSoup
from immowelt import Immowelt
from immobilienscout24 import Immobilienscout24

if __name__ == "__main__":
    data = []
    immo = Crawler(Immobilienscout24('/Suche/S-T/Wohnung-Miete/Umkreissuche/Wuppertal/42119/-195778/2370902/-/-/50/2,00-/60,00-/EURO--450,00'))
    immo2 = Crawler(Immowelt('/liste/wuppertal-elberfeld/wohnungen/mieten?lat=51.2482&lon=7.1538&sr=50&roomi=2&prima=400&wflmi=60&sort=distance'))
    #immo2 = Crawler(Immowelt('/liste/wuppertal-elberfeld/wohnungen/mieten?lat=51.2482&lon=7.1538&sr=10&roomi=2&prima=400&wflmi=60&sort=distance'))
    data.extend(immo.start())
    data.extend(immo2.start())
    if len(data) > 0:
        print("Erstelle CSV...")
        with open('output.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(data)
        print("Done")
