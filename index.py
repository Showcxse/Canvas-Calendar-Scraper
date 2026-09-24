import os
import time
from playwright.sync_api import sync_playwright
from notion_client import Client
from dotenv import load_dotenv


load_dotenv(".env.local")

CANVAS_CALENDAR_URL = os.getenv("CANVAS_CALENDAR_URL")
NOTION_TOKEN = os.getenv("NOTION_API_KEY")
NOTION_DB_ID = os.getenv("NOTION_DB_ID")
MONTHS_TO_SCRAPE = int(os.getenv("MONTHS_TO_SCRAPE", 4))

notion = Client(auth=NOTION_TOKEN)


# SCRAPER

def scrape_canvas_calender(canvas_url, term_length_months):
    assignments = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(canvas_url)

        print("LOGIN BURGER")
        print("RESUME AFTER LOGIN")
        page.pause()

        for month in range(term_length_months):
            print(f'Scraping month {month + 1}...')

            page.wait_for_selector('.fc-view-container')

            days = page.locator('.fc-day').all()
            for day in days:
                date_str =  day.get_attribute('data-date')

                events = day.locator('.fc-event').all()
                for event in events:
                    title = event.locator('.fc-title').inner_text()

                    assignments.append({
                        "title": title,
                        "date": date_str,
                        "class": "Imported" 
                    })
            page.locator('.fc-next-button').click()
            time.sleep(2)
        browser.close()
    return assignments


    # TO DO: ALL THE NOTION STUFF

    #ALSO TO DO: EXECUTING THE SCRIPT        