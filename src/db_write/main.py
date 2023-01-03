import sys
sys.path.append('../')
import requests

from scrape_methods.series import Series
from scrape_methods.event import Event
from scrape_methods.matches import Matches
from db_write import insert

# Populate the database.
# First take the series IDs as arguments to the script
# For each series ID, store the name and description of the series in the database.
# For each series ID, iterate through each event ID that it has. 
# Inside each event ID, store its respective information, then iterate through all its matches. 
# Inside each match, go through the JSON and store the match info, map info
# For each map in the match, store each player's performance info

def start_script():
    seriesIDs = ["14"] # 14 = VCT 2022
    
    for seriesID in seriesIDs:
        # Fetch information on one series.
        curSeries = Series().series(seriesID)
        # Store the series id, series title, and series subtitle.
        series_id = curSeries['id']
        series_title = curSeries['title']
        series_subtitle = curSeries['subtitle']
        num_events = len(curSeries['events'])

        # Insert into database
        insert.insert_series(series_id, series_title, series_subtitle, num_events)
        
        print("Fetching data for " + str(num_events) + " events.")
        
        # Fetch each event. Lets limit the events to... 5.

        for idx, event in enumerate(curSeries['events']):
            print("Scraping event #" + str(idx))
            if idx == 10:
                break
            event_id = event['id']
            curEvent = Event().event(event_id)
            event_title = curEvent['title']
            event_subtitle = curEvent['subtitle']
            event_dates = curEvent['dates']
            event_location = curEvent['location']
            event_img = curEvent['img']
            num_matches = len(curEvent['matches'])
            
            # Insert event into database
            insert.insert_event(event_id, series_id, event_title, event_subtitle, event_dates, event_location, event_img, num_matches)
            
            print("Fetching data for " + str(num_matches) + " matches.")
            # Fetch each match id
            for match in curEvent['matches']:
                match_id = match['id']
                curMatch = Matches().match(match_id)
                team1_name = curMatch["teams"][0]["name"]
                team2_name = curMatch["teams"][1]["name"]
                team1_img = curMatch["teams"][0]["img"]
                team2_img = curMatch["teams"][1]["img"]
                team1_score = curMatch["score"].split(':')[0]
                team2_score = curMatch["score"].split(':')[1]
                datetime = curMatch["event"]["date"]
                stage = curMatch["event"]["stage"]
                patch = curMatch["patch"]
                best_of = curMatch["best-of"]
                
                insert.insert_match(match_id, event_id, best_of, team1_name, team1_img, team2_name, team2_img, team1_score, team2_score, datetime, stage, patch)

                map_num = 1
                data = curMatch['data']
                for idx, map in enumerate(data):
                    if idx == 1:
                        continue
                    map_id = map['map-id']
                    map_name = map['map']
                    map_score_team1 = map['teams'][0]['score']
                    map_score_team2 = map['teams'][1]['score']
                    map_duration = map['map-duration']
                    
                    # Now store in gamemap table
                    insert.insert_map(map_id, match_id, map_num, map_name, map_score_team1, map_score_team2, map_duration)
                    
                    # for loop to store all player performances
                    for idx, player in enumerate(map["members"]):
                        # 
                        # player_performance_id = str(match_id) + str(map_id) + str(idx)
                        player_team_num = 1 # 0, 1, 2, 3, 4
                        player_team_name = team1_name
                        if idx >= 5: # 5, 6, 7, 8, 9
                            player_team_num = 2
                            player_team_name = team2_name
                        player_name = player["name"]
                        player_agent = player["agents"][0]["name"]
                        if player['rating'] == '':
                            player_rating = None
                        else:
                            player_rating = float(player["rating"])
                        player_acs = int(player["acs"])
                        player_kills = int(player["kills"].split("\n")[0])
                        player_deaths = int(player["deaths"].split("\n")[0])
                        player_assists = int(player["assists"].split("\n")[0])
                        player_KAST = int(player["kast"].split("\n")[0].replace("%",""))
                        player_adr = int(player["adr"].split("\n")[0])
                        player_hsperc = int(player["hsperc"].split("\n")[0].replace("%",""))
                        player_fk = int(player["fk"].split("\n")[0])
                        player_fd = int(player["fd"].split("\n")[0])
                        
                        insert.insert_player_perf(map_id, player_team_num, player_team_name, player_name, player_agent, player_rating, player_acs, player_kills, player_deaths, player_assists, player_KAST, player_adr, player_hsperc, player_fk, player_fd)
                    
                    map_num += 1


if __name__ == "__main__":
    start_script()