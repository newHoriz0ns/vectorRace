import matplotlib.pyplot as plt

from track import Track

MAP_WALL = "x"
MAP_SREET = " "
MAP_START = "s"
MAP_ZIEL = "#"

def importTrackFromBMP(filepath) -> dict: 
    return plt.imread(filepath)


def importTrackByName(trackName) -> Track:

    im = importTrackFromBMP("tracks/" + trackName + "/map.bmp")
    map = [[MAP_WALL for x in range(len(im[y]))] for y in range(len(im))]
    startSpots = {}

    for y in range (len(im)):
        for x in range(len(im[y])):
            code = im[y][x]
            if(sum(code) != 3*255):
                if(code[0] == 0):
                        map[y][x] = MAP_SREET                        
                elif(code[0] == 100):
                    if(code[1] == 100):
                        map[y][x] = MAP_ZIEL
                    elif(code[1] > 0 and code[1] <= 10):
                        map[y][x] = MAP_START
                        startSpots[str(code[1])] = ([x, y])

    return Track(trackName, map, startSpots)
