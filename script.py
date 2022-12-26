import os, sys, requests, json
from fastapi import FastAPI

KEY_API = "?api_key=70cd3ddd-bb98-4430-85a2-e0c732cd9811"
LINK_API = "https://api.opendota.com/api/matches/"  

app = FastAPI()

@app.post("/match/")
def root(match: str, mvp: str):
    if os.path.exists("statistics.json"):
        r = open("statistics.json")
        statistics = json.loads(r.read())
    else:
        statistics = dict()
    
    if len(sys.argv) < 1:
        print("Error")
        return 0
    id_match = sys.argv[1]

    if len(sys.argv) > 1:
        mvp = sys.argv[2]

    # p = open("test.json", "r")
    # j = json.loads(p.read())
    j = json.loads(requests.get(LINK_API + id_match + KEY_API).text)
    
    statistics = init_players(j, statistics)
    with open("statistics.json", "w") as w:
        w.write(json.dumps(statistics, indent=4))

    statistics = get_statistics(j, mvp, statistics)

    with open("statistics.json", "w") as w:
        w.write(json.dumps(statistics, indent=4))


def init_players(j, statistics):
    for player in j["players"]:
        if "personaname" in player:
            name = player["personaname"]
        else:
            name = None
        if not str(player["account_id"]) in statistics:    
            statistics[str(player["account_id"])] = {"name": name,
                                                    "mvp_qnt": 0,
                                                    "match_as_winner_qnt": 0,
                                                    "match_as_loser_qnt": 0,
                                                    "death_average": 0,
                                                    "total_death_all_matches": 0,
                                                    "kill_average": 0,
                                                    "total_kill_all_matches": 0,
                                                    "net_worth_average": 0,
                                                    "tower_damage_average": 0
    }
            
    return statistics

def get_statistics(j, mvp, statistics):
    for player in j["players"]:
        id = str(player["account_id"])
        

        if id == mvp:
            statistics[id]["mvp_qnt"] = statistics[id]["mvp_qnt"] + 1
        

        if player["win"] == 1:
            statistics[id]["match_as_winner_qnt"] = statistics[id]["match_as_winner_qnt"] + 1
        else:
            statistics[id]["match_as_loser_qnt"] = statistics[id]["match_as_winner_qnt"] + 1
         
        if statistics[id]["death_average"] == 0:
            statistics[id]["death_average"]  = player["deaths"]
        else:
            statistics[id]["death_average"] = int((statistics[id]["death_average"] + player["deaths"]) / 2)

        statistics[id]["total_death_all_matches"] = statistics[id]["total_death_all_matches"] + player["deaths"]
        
        if statistics[id]["kill_average"] == 0:
            statistics[id]["kill_average"] = player["kills"]
        else:
            statistics[id]["kill_average"] = int((statistics[id]["kill_average"] + player["kills"]) / 2)

        statistics[id]["total_kill_all_matches"] = statistics[id]["total_kill_all_matches"] + player["kills"]

        if statistics[id]["net_worth_average"] == 0:
            statistics[id]["net_worth_average"] = player["net_worth"]
        else:
            statistics[id]["net_worth_average"] = int((statistics[id]["net_worth_average"] + player["net_worth"]) + 2)
        
        if statistics[id]["tower_damage_average"] == 0:
            statistics[id]["tower_damage_average"] = player["tower_damage"]
        else:
            statistics[id]["tower_damage_average"] = int((statistics[id]["tower_damage_average"] + player["tower_damage"]) / 2)
        # print(id, statistics[id]["tower_damage_average"], player["tower_damage"])
        # input()
    return statistics

def main():

    if os.path.exists("statistics.json"):
        r = open("statistics.json")
        statistics = json.loads(r.read())
    else:
        statistics = dict()
    
    if len(sys.argv) < 1:
        print("Error")
        return 0
    id_match = sys.argv[1]

    if len(sys.argv) > 1:
        mvp = sys.argv[2]

    # p = open("test.json", "r")
    # j = json.loads(p.read())
    j = json.loads(requests.get(LINK_API + id_match + KEY_API).text)
    
    statistics = init_players(j, statistics)
    with open("statistics.json", "w") as w:
        w.write(json.dumps(statistics, indent=4))

    statistics = get_statistics(j, mvp, statistics)

    with open("statistics.json", "w") as w:
        w.write(json.dumps(statistics, indent=4))

if __name__ == "__main__":
    main()
