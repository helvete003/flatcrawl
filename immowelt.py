import re
from datetime import datetime
from bs4 import BeautifulSoup

class Immowelt:
    realtor_blacklist = ['Grand City Property Ltd. Zweigniederlassung Deutschland','Vonovia Kundenservice GmbH','LEG Wohnen NRW  GmbH Bereich Zentrales Vermietungsmanagement']
    BASE_URL = 'https://www.immowelt.de'
    def __init__(self,start):
        self.start_url = start

    #Gibt die nächste übersichtsseite zurück
    def nextPageRule(self, bs):
        np = bs.find('a', id='nlbPlus')
        if np != None:
            return np.get('href')
        return None

    #gibt alle expose container von der übersicht zurück
    def realtorLinkListRule(self, bs):
        return bs.find_all('div', class_='listitem')

    #
    def isRealtorAllowed(self, bs):
        tag = bs.find('div', class_='company_name')
        if tag != None:
            name = tag.get_text().strip()
            if not name in self.realtor_blacklist:
                return True
        return False

    def getExposeLink(self, bs):
        #das erste a ist hier der link zur seite
        return bs.find('a')

    def exposeSearch(self, bs):
        energy = self.getEnergyCarrier(bs)
        date = self.getFreeDate(bs)
        search_date = datetime(2019,9,30)
        if energy == 'Gas' and date != None:
            if date > search_date:
                return True
        return False


    def getEnergyCarrier(self, bs):
        tag = bs.find('div', id='divImmobilie')
        data = None
        for row in tag.find_all('div', class_='datarow'):
            text = row.find('span', class_='datalabel').get_text().strip()
            if text == 'Wesentliche Energieträger':
                data = row.find('span', class_='datacontent').get_text().strip()
                break
        if data != None:
            return data
        return None

    def getFreeDate(self,bs):
        tag = bs.find('div', id='divImmobilie')
        parent = None
        for elem in tag.find_all('div', class_='section_label iw_left'):
            if elem.get_text().strip() == 'Die Wohnung':
                parent = elem.find_parent('div', class_="clear")
                break
        parent = parent.find('div',class_='iw_right')
        if parent != None:
            try:
                text = re.search(r'\d{2}\.\d{2}\.\d{4}', parent.get_text())
                return datetime.strptime(text.group(), '%d.%m.%Y')
            except:
                return None
        return None

    def getName(self,bs):
        tag = bs.find('div', class_='quickfacts iw_left')
        tag = tag.find('h1')
        if tag != None:
            return tag.get_text().strip()
        return None

    def getFullRent(self,bs):
        return 'Muss berechnet werden'

    def getBond(self,bs):
        tag = bs.find('div', id='divPreise')
        parent = None
        for elem in tag.find_all('div', class_='section_label iw_left'):
            if elem.get_text().strip() == 'Kaution':
                parent = elem.find_parent('div', class_="clear")
                break

        if parent != None:
            return parent.find('div',class_='iw_right').get_text().strip()
        return None
