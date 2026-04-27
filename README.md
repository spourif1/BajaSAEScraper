## Project Title
BAJA SAE Point Predictor

## Project Description
Using the live results page provided by SAE during BAJA competitions, this code will give you project points based on the formula used for scoring points. All teams that have passed tech will have their times/distance compiled into a projective points scoreboard to allow teams to know what their time corresponds to in points. Also incorporates a points to dollar cost for the cost event. Using the HTML code, keywords are used to find times for each event which are then plugged into a dictionary for each team and scores are calculated for each event.


## How to Run
1. Have Python Installed and supporting libraries (BeautifulSoup4, Pandas, Selenium, Cloudscraper)
2. Verify URLBASE is the same for the live results website (if the URL changes, this code will still work as long as you change the URL properly)
3. Run code


## Languages Used
All code is written in Python. Scraping is done using BeautifulSoup4 and Selenium Libraries, Cloudscraper is used to get around any issues with cloudflare and Pandas is used for spreadsheet generation.

## Scope
All code is written by me except for libraries used.

## Sample Output
<img width="1512" height="645" alt="Screenshot 2026-04-26 at 10 28 52 PM" src="https://github.com/user-attachments/assets/c689debe-02d1-4347-a872-68830088219a" />

