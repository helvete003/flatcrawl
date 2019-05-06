from datetime import datetime
from bs4 import BeautifulSoup

class Immowelt:
    realtor_blacklist = ['Grand City Property Ltd. Zweigniederlassung Deutschland','Vonovia Kundenservice GmbH','LEG Wohnen NRW  GmbH Bereich Zentrales Vermietungsmanagement']
    BASE_URL = 'https://www.immowelt.de'
    START_URL = '/liste/wuppertal-elberfeld/wohnungen/mieten?lat=51.2482&lon=7.1538&sr=50&roomi=2&prima=400&wflmi=60&sort=distance'

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
        search_date = datetime(2019,8,30)
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
