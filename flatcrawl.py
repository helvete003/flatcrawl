#!/usr/bin/env python3
import csv
from crawler import Crawler
from bs4 import BeautifulSoup
from immowelt import Immowelt
from immobilienscout24 import Immobilienscout24

if __name__ == "__main__":
    data = []
    immo = Crawler(Immobilienscout24())
    #immo2 = Crawler(Immowelt())
    data.extend(immo.start())
    if len(data) > 0:
        print("Erstelle CSV...")
        with open('output.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(data)
        print("Done")
