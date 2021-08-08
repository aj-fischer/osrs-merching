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
    with open("blood-prices.csv", "r") as f:
        lines = f.read().splitlines()
        lastLine = lines[-1]
        lastLineItems = lastLine.split(",")
        lastPrice = lastLineItems[1]
        return lastPrice

def logData(currentTime, currentPrice):
    file = open("blood-prices.csv", "a")
    if os.stat("blood-prices.csv").st_size == 0:
        file.write("Last Change,Price\n")
    elif getLastPrice() == currentPrice:
        file.flush()
        file.close()
        return
    file.write(str(currentTime)+","+str(currentPrice)+"\n")
    file.flush()
    file.close()

# Logs data if program has just started and price has changed since last run
logData(getCurrentTime(), str(getCurrentPrice()))

while True:
    pastPrice = getLastPrice()
    time.sleep(360)
    currentPrice = str(getCurrentPrice())
    if (pastPrice != currentPrice):
        # Send notification as well
        currentTime = getCurrentTime()
        logData(currentTime, currentPrice)