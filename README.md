# Steam User Scraper

## About
Steam User Scraper (SUS) is a GUI based program designed to scrape a user's publicly available profile data, game stats and inventory for data visualization or tracking. 
SUS uses Steam's Public API to authorize and send requests which it then processes and parses in to easy to read formats such as .csv or .xslx for use in Excel or JSON for other applications. SUS features a settings file to allow for storing preferences to speed up the steam authentication process and preferred file formats. The results outputted by SUS are by default ranked in descending order (Highest -> Lowest) in terms of hours played.

### Primary Features
- JSON preferences file
- Single or batch scraping
- **File types supported**
  - xlsx 
  - CSV
  - JSON
- **Output Sorting Types**
  - Alphabetic (A-Z, Z-A)
  - Numeric (Highest->Lowest, Lowest->Highest)

### Limitations
- Only users with public profiles are supported
- Steam's public API allows for a maximum of 100,000 api calls per day/24 hours. On average for a user it may take up to 3 api calls to fetch the necessary details which could potentially limit the daily limit to 30,000 unique user searches per day.

## Installation

### Requirements
#### Python Version
  - 3.11.9 and above
#### Packages
See [Project Dependencies](https://github.com/Adrian-Sz1/SteamScraper/network/dependencies)

## How-To-Use
