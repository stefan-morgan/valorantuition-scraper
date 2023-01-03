import requests
from bs4 import BeautifulSoup
from requests.api import head

class Series:
    
    def series(self, id):
        series={}
        
        series['id'] = id
        URL = "https://www.vlr.gg/series/" + id
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        
        header = soup.find_all('div', class_='event-header')[0]
        series['title'] = header.find_all('div', class_='wf-title')[0].get_text().strip()
        series['subtitle'] = header.find_all('div', class_='wf-title')[0].find_next_siblings('div')[0].get_text().strip()
        
        events = []
        completedEvents = soup.find_all('div', class_='events-container-col')[1].find_all('a', class_='event-item')
        
        for card in completedEvents:
            event = {}
            event['id'] = card['href'].split('/')[2]
            events.append(event)
        
        series["numEvents"] = len(events)
        series["events"] = events
        
        return series;