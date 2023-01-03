from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config

def insert_player_perf(map_id, player_team_num, player_team_name, player_name, player_agent, player_rating, player_acs, player_kills, player_deaths, player_assists, player_KAST, player_adr, player_hsperc, player_fk, player_fd):
    query = "INSERT INTO player_perf (map_id, player_team_num, player_team_name, player_name, player_agent, player_rating, player_acs, player_kills, player_deaths, player_assists, player_kast, player_adr, player_hsperc, player_fk, player_fd) " \
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    args = (map_id, player_team_num, player_team_name, player_name, player_agent, player_rating, player_acs, player_kills, player_deaths, player_assists, player_KAST, player_adr, player_hsperc, player_fk, player_fd)
    insert(query, args)
    print("Inserted player, auto increment")
                    
def insert_map(map_id, match_id, map_num, map_name, map_score_team1, map_score_team2, map_duration):
    query = "INSERT INTO gamemap (map_id, match_id, map_num, map_name, map_score_team1, map_score_team2, map_duration) " \
            "VALUES (%s, %s, %s, %s, %s, %s, %s)"
    args = (map_id, match_id, map_num, map_name, map_score_team1, map_score_team2, map_duration)
    insert(query, args)
    print("Inserted map " + map_id)
                
            
def insert_match(match_id, event_id, best_of, team1_name, team1_img, team2_name, team2_img, team1_score, team2_score, datetime, stage, patch):
    query = "INSERT INTO matchup (match_id, event_id, best_of, team1_name, team1_img, team2_name, team2_img, team1_score, team2_score, datetime, stage, patch) " \
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    args = (match_id, event_id, best_of, team1_name, team1_img, team2_name, team2_img, team1_score, team2_score, datetime, stage, patch)
    insert(query, args)
    print("Inserted match " + match_id)
        
def insert_event(event_id, series_id, title, subtitle, dates, location, img, num_matches):
    query = "INSERT INTO event (event_id, series_id, event_title, event_subtitle, event_dates, event_location, event_img, num_matches) " \
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    args = (event_id, series_id, title, subtitle, dates, location, img, num_matches)
    insert(query, args)
    print("Inserted event " + event_id)

def insert_series(series_id, title, subtitle, num_events):
    query = "INSERT INTO series (series_id, series_title, series_subtitle, num_events) " \
            "VALUES (%s, %s, %s, %s)"
    args = (series_id, title, subtitle, num_events)
    insert(query, args)
    print("Inserted series " + series_id)
    
def insert(query, args):
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        
        cursor = conn.cursor()
        cursor.execute(query, args)
        
        #not sure if this is needed.
        #else:
            #print('last insert id not found')
        
        conn.commit()
        
    except Error as e:
        print(e)
    
    finally:
        cursor.close()
        conn.close()