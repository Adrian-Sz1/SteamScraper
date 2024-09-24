# Steam User Scraper

## About
Steam User Scraper (SUS) is a GUI based program designed to scrape a user's publicly available profile data, game stats and inventory for data visualization or data tracking. It primarily communicates with [Steam's Web API](https://partner.steamgames.com/doc/webapi_overview) which requires a user of SUS to posses a valid [Steam API key](https://steamcommunity.com/dev/apikey) and consequently a Steam account to gather information. It does not store any sensitive data (usernames, passwords etc.), except the Steam API key which is exclusively stored on the client machine and used for communicating with the Steam's Web API.

### Primary Features
- Modifiable settings.json file for saving scraping preferences:
  - STEAM API Key
  - Output file type (csv, json and yaml)
  - Output directory
  - User output sub-folders e.g. ("../Steam User Scraper/json/{STEAMID}/output.json")
- Fetching options:
  - Inventory
  - Games
  - Friends
  - Reviews
  - Profile Comments 
- Single or batch scraping using comma delimited strings

### Limitations
- Only users with public profiles are supported
- Steam's Web API allows for a maximum of 100,000 api calls per day/24 hours. On average for a user it may take up to 3 api calls to fetch the necessary details which could potentially limit the daily limit to 30,000 unique user searches per day.
- You must use either a user's steamId OR a user's custom url name, display names do NOT work as they are not unique!
  - For steam account https://steamcommunity.com/id/robinwalker/ 
    - Custom-URL - robinwalker **Will work**
    - Steam64Id - 76561197960435530 **Will work**
    - Display Name - Robin **Will not work**


## Installation

### Requirements
#### Python Version
  - 3.11.9 and above
#### Packages
See [Project Dependencies](https://github.com/Adrian-Sz1/SteamScraper/network/dependencies)

## How-To-Use
1. Firstly, you must obtain your Steam API Key, head to https://steamcommunity.com/dev/apikey and follow the instructions to obtain your key.
   ![image](https://github.com/user-attachments/assets/70f3a25d-7ff1-4336-95aa-55f7eae7cf16)

3. Once you obtain your key you will need to paste it in to the 'Your Steam API key' field.
   ![image](https://github.com/user-attachments/assets/e1dc6ad8-6e03-41d1-8d33-ccbc3db797f4)

5. Check that your key is valid by clicking the 'Check Key' button. If the key is valid, you should see a green 'OK' text appear.
   ![image](https://github.com/user-attachments/assets/553ca49e-1889-43af-b018-037e6062fb8a)

7. Select your desired folder directory, file type and the user details you would like to retrieve
8. Input the users that you would like to retrieve information for in the 'Parameters' panel. User's must be seperated by a comma (,) like this "username1,username2".
   ![image](https://github.com/user-attachments/assets/7b72f82d-6c0b-4ea9-97b8-4661bf788e0b)
9. Hit 'Start' button to begin the scrapping process
10. Once finished, navigate to the output folder directory to see the output results
