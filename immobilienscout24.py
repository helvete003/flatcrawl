from datetime import datetime
from bs4 import BeautifulSoup

class Immobilienscout24:
    realtor_blacklist = ['Grand City Property','Vonovia SE','LEG Wohnen NRW GmbH']
    BASE_URL = 'https://www.immobilienscout24.de'
    def __init__(self,start):
        self.start_url = start

    #Gibt die nächste übersichtsseite zurück
    def nextPageRule(self, bs):
        np = bs.find('a', attrs={"data-is24-qa": "paging_bottom_next"})
        if np != None:
            return np.get('href')
        return None

    #gibt alle expose container von der übersicht zurück
    def realtorLinkListRule(self, bs):
        return bs.find_all('li', class_='result-list__listing')

    #
    def isRealtorAllowed(self, bs):
        tag = bs.find('div', class_='result-list-entry__realtor-data').find('span').find_next('span')
        if tag != None:
            name = tag.get_text().strip()
            if not name in self.realtor_blacklist:
                return True
        return False

    def getExposeLink(self, bs):
        return bs.find('a', class_='result-list-entry__brand-title-container')

    def exposeSearch(self, bs):
        energy = self.getEnergyCarrier(bs)
        date = self.getFreeDate(bs)
        search_date = datetime(2019,9,30)
        if energy == 'Gas' and date != None:
            if date > search_date:
                return True
        return False


    def getEnergyCarrier(self, bs):
        tag = bs.find('dd', class_='is24qa-wesentliche-energietraeger')
        if tag != None:
            return tag.get_text().strip()
        return None

    def getFreeDate(self,bs):
        tag = bs.find('dd', class_='is24qa-bezugsfrei-ab')
        if tag != None:
            try:
                return datetime.strptime(tag.get_text().strip(), '%d.%m.%Y')
            except:
                return None
        return None

    def getName(self,bs):
        tag = bs.find('h1', id='expose-title')
        if tag != None:
            return tag.get_text().strip()
        return None

    def getFullRent(self,bs):
        tag = bs.find('dd', class_='is24qa-gesamtmiete')
        if tag != None:
            return tag.get_text().strip()
        return None

    def getBond(self,bs):
        tag = bs.find('div', class_='is24qa-kaution-o-genossenschaftsanteile')
        if tag != None:
            return tag.get_text().strip()
        return None
