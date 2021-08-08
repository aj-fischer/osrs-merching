import os
import json
import requests
import time

bloodRuneID = 565

url = "https://secure.runescape.com/m=itemdb_oldschool/api/catalogue/detail.json?item="+str(bloodRuneID)

def getCurrentTime():
    t = time.time()
    currentTime = time.strftime("%Y-%m-%d %H:%M %Z", time.localtime(t))
    return currentTime

def getCurrentPrice():
    r = requests.get(url)
    data = json.loads(r.content)
    currentPrice = data["item"]["current"]["price"]
    return currentPrice

def getLastPrice():
    file = open("blood-prices.csv", "a")
    if os.stat("blood-prices.csv").st_size == 0:
        return
    with open("blood-prices.csv", "r") as f:
        lines = f.read().splitlines()
        lastLine = lines[-1]
        lastLineItems = lastLine.split(",")
        lastPrice = lastLineItems[1]
        return lastPrice

def logData(currentTime, currentPrice, lastPrice):
    file = open("blood-prices.csv", "a")
    if os.stat("blood-prices.csv").st_size == 0:
        file.write("Last Change,Price\n")
        file.write(str(currentTime)+","+str(currentPrice)+"\n")
    elif lastPrice == str(currentPrice):
        file.close()
        return
    else:
        file.write(str(currentTime)+","+str(currentPrice)+"\n")
    file.flush()
    file.close()
    
if __name__ == "__main__":
    logData(getCurrentTime(), getCurrentPrice(), getLastPrice())