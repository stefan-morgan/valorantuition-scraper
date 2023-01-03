import requests
from bs4 import BeautifulSoup
from requests.api import head



class Event:
    
    def getMatches(self, id):
        matches = []
        URL = "https://vlr.gg/event/matches/" + id
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
            
        atags = soup.find_all('a', class_='wf-module-item')
        
        for atag in atags:
            match = {}
            match['id'] = atag['href'].split('/')[1]
            matches.append(match)

        return matches
    
    def event(self, id):
        # return an object with some event details, and all match IDs
        event = {}
        event['id'] = id
        URL = "https://www.vlr.gg/event/" + id
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        
        header = soup.find_all('div', class_="event-header")[0]
        event['title'] = header.find_all('h1', class_="wf-title")[0].get_text().strip()
        event['subtitle'] = header.find_all('h2', class_="event-desc-subtitle")[0].get_text().strip()
        event['dates'] = header.find_all('div',class_='event-desc-item-value')[0].get_text().strip()
        event['location'] = header.find_all('div',class_='event-desc-item-value')[2].find_all('i', class_="flag")[0].get('class')[1].replace('mod-', '')
        img = header.find_all('div',class_='event-header-thumb')[0].find('img')['src']
        if img == '/img/vlr/tmp/vlr.png':
            img = "https://vlr.gg" + img
        else:
            img = "https:" + img
        event['img'] = img
        
        event['matches'] = self.getMatches(id)
        
        return event
        
        
        
        
    
    
        