# Steam User Scraper

## About
Steam User Scraper (SUS) is a Command-Line tool (GUI WiP) designed to scrape a user's play time. The basic premise is to allow a given user to rapidly retreive their or any other publicly accessible user's/users' profile statistics for data visualization or tracking. 
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

## Installation

### Requirements
#### Python Version
  - 3.11.9 and above
#### Packages
- ```Selenium```
- ```ChromeDriverManager```
- ```openyxl```
- ```bs4```
- ```Steam```
- ```PySimpleGUI```

## How-To-Use
