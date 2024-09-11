# OTA Scraper

This project scraps the hotels data from a given link for which the targetted site was https://us.trip.com/hotels/list?city=1187&locale=en-US&curr=USD. It uses scraping tools, handles javascript rendering, fetches the described data and stores athem in a csv file for reporting.

### Setup

1. Requirements:
   ```
   - Python 3.x
   - Google Chrome browser
   - ChromeDriver
   ```


2. Clone project:
   ```bash
   cd KabuKStyle-OTA\ Scraper/ (after downloading the project)
   ```

3. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Install Proxy Servers:
   ```
   pip3 install proxy.py
   ```
5. Configure Proxy Servers:
   ```
    proxy --port 8080
    proxy --port 8081
    proxy --port 8082
   ```

6. Running the scrapper locally:
   ```
    python scraper.py 
   ```

7. Subject
   ```
   “Senior Backend Python Engineer Assignment – [Aqsa Khalid]”.
   ```
