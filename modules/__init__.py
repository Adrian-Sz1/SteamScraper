from datetime import date

dataFolderPath = "../data/"
ScrapeDataPath = dataFolderPath + "ScrapeData/"
SteamAuthData = dataFolderPath + "SteamAuthData/"

currentDate = date.today().strftime("%d-%m-%Y")
currentSteamId = str()
currentUserName = str()
history = list()

status = None
currentGameData = list()

