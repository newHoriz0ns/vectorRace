import json
import time

from track import Track


def saveRouteToFile(track: Track, poses, name):
    infos = {}
    infos["name"] = name
    infos["anzahl"] = len(poses) - 1
    infos["zuege"] = poses

    with open('tracks/' + track.name + '/' + str(int(time.time())) + '.sav', 'w', encoding ='utf8') as json_file: 
        json.dump(infos, json_file, ensure_ascii = False) 


def loadRouteFromFile(file) -> dict:
    try:
        with open(file) as f:
            return json.load(f)
            
    except:
        return None
        