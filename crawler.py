import requests, sys,time
from bs4 import BeautifulSoup

class Crawler:
    def __init__(self, portal):
        self.portal = portal

    def start(self):
        self.expose_links = []
        print("Crawle Wohnungen...")
        if self.crawl(self.portal.BASE_URL+self.portal.START_URL):
            print("Crawling Beendet")
            print("Crawle "+str(len(self.expose_links))+" Exposes...")
            return self.crawlExpose()
        else:
            print("Hat vorraussichtlich nicht alle Seiten gecrawlt")
        return []

    def crawl(self,url):
        code = requests.get(url)
        if code.status_code == requests.codes.ok:
            s = BeautifulSoup(code.text, "html.parser")
            next_page = self.portal.nextPageRule(s)
            for result in self.portal.realtorLinkListRule(s):
                if self.portal.isRealtorAllowed(result):
                    link = self.portal.getExposeLink(result)
                    if link != None:
                        self.expose_links.append(link.get('href'))
            if next_page != None:
                return self.crawl(self.portal.BASE_URL+next_page)
            else:
                return True
        return False

    def crawlExpose(self):
        found_expose = []
        expose_len = len(self.expose_links)
        for idx,url in enumerate(self.expose_links):
            try:
                code = requests.get(self.portal.BASE_URL+url)
                if code.status_code == requests.codes.ok:
                    s = BeautifulSoup(code.text, "html.parser")
                    if self.portal.exposeSearch(s):
                        found_expose.append([self.portal.getName(s), self.portal.getFullRent(s) ,self.portal.getBond(s) ,self.portal.getFreeDate(s).strftime('%d.%m.%Y'),self.portal.getEnergyCarrier(s),self.portal.BASE_URL+url])
            except requests.exceptions.ConnectionError as errc:
                print ("Konnte Expose nicht Crawlen")
            except requests.exceptions.Timeout as errt:
                print ("Konnte Expose nicht Crawlen")
            except requests.exceptions.RequestException as err:
                print ("Konnte Expose nicht Crawlen")
            sys.stdout.write("\r{0} von {1} {2}".format(idx+1,expose_len,self.portal.BASE_URL+url))
            sys.stdout.flush()
        print(" ")
        return found_expose
