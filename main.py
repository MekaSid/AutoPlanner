from playwright.sync_api import sync_playwright
import pandas as pd
import time

def get_user_preferences():
    print("Welcome to our Trip Planner! Please complete the following survey, so we can plan your trip.")

    user_preferences = {}

    user_preferences['destination'] = input("Where would you like to travel to? ")
    user_preferences['start_date'] = input("What day do you plan on leaving? Enter as YYYY-MM-DD format. ")
    user_preferences['return_date'] = input("What day do you plan on returning? Enter as YYYY-MM-DD format. ")
    user_preferences['budget'] = input("What is your budget for the trip? ")
    user_preferences['adults'] = input("How many adults will be travelling? ")
    user_preferences['children'] = input("How many children will be travelling? ")
    user_preferences['rooms'] = input("How many rooms will you require? ")

    print("Thank you for completing our survey.")
    print(user_preferences)

    return user_preferences

def main():
    preferences = get_user_preferences()

    with sync_playwright() as p:
        start = preferences['start_date']
        end = preferences['return_date']
        adults = preferences['adults']
        kids = preferences['children']
        rooms = preferences['rooms']

        url = 'https://www.booking.com/index.html?sid=42ef08eb3fbb8d92c6f47b2d5f85ffcb&aid=355028'
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto(url, timeout=60000)

        time.sleep(3)
        page.click('input[name="ss"]')
        page.fill('input[name="ss"]',preferences['destination'])

        time.sleep(1)
        page.click('button[type="submit"]')
        page.wait_for_load_state('networkidle')

        hotels = page.locator('//div[@data-testid="property-card"]').all()
        
        hotels_list = []
        for hotel in hotels:
            hotel_dict = {}
            hotel_dict['hotel'] = hotel.locator('//div[@data-testid="title"]').inner_text()
            hotel_dict['price'] = hotel.locator('//span[@data-testid="price-and-discounted-price"]').inner_text()

            hotels_list.append(hotel_dict)


        print(hotels_list)
        df = pd.DataFrame(hotels_list)

        browser.close()


if __name__ == '__main__':
    main()
