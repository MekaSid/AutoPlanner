from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import pandas as pd
import re
import time 

# need to map destinations to attraction IDs lol
DESTINATION_ATTRACTION_IDS = {
    "greece": "100036",
    "los-angeles": "120518",
    "rome": "303"
}

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

def hotel_scrape(preferences):
    with sync_playwright() as p:
        ss = preferences['destination']
        ss = ss.replace(" ", "+")
        checkin = preferences['start_date']
        checkout = preferences['return_date']
        group_adults = preferences['adults']
        group_children = preferences['children']
        no_rooms = preferences['rooms']
        
        base_url = "https://www.booking.com/searchresults.html?"
        url_params = [
            f"ss={ss}",
            f"checkin={checkin}",
            f"checkout={checkout}",
            f"group_adults={group_adults}",
            f"no_rooms={no_rooms}",
            f"group_children={group_children}"
        ]
        url = base_url + "&".join(url_params)
        
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto(url, timeout=60000)

        #time.sleep(3)
        #page.click('input[name="ss"]')
        #page.fill('input[name="ss"]',preferences['destination'])

        #time.sleep(1)
        #page.click('button[type="submit"]')
        #page.wait_for_load_state('networkidle')

        hotels = page.locator('//div[@data-testid="property-card"]').all()
        
        hotels_list = []
        for hotel in hotels:
            hotel_dict = {}
            hotel_dict['hotel'] = hotel.locator('//div[@data-testid="title"]').inner_text()
            hotel_dict['price'] = hotel.locator('//span[@data-testid="price-and-discounted-price"]').inner_text()
            price = hotel_dict['price']
            price = price.replace('$','').replace(',','')
            if float(price) <= float(preferences['budget']):
                hotels_list.append(hotel_dict)

        print(hotels_list)
        
        df = pd.DataFrame(hotels_list)

        browser.close()

# still need to get the rest of the prices
# need to figure out how to get ratings
def activity_scrape(preferences):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        destination = preferences['destination'].replace(" ", "-")  
        attraction_id = DESTINATION_ATTRACTION_IDS.get(destination)
        if not attraction_id:
            print(f"Error: No attraction ID found for destination '{preferences['destination']}'")
            return None

        url = f"https://us.trip.com/travel-guide/attraction/{destination}-{attraction_id}/tourist-attractions/?locale=en-US&curr=USD"
        
        page.goto(url)
        page.wait_for_selector('.tour-price')
        prices = page.inner_text('.tour-price')
        prices = prices.split('\n')
        prices = list(filter(None, prices))

        ratings = page.inner_text('.online-trip-review')
        ratings = ratings.split('\n')
        ratings = list(filter(None, ratings))
        
        attractions_data = []
        for price, rating in zip(prices, ratings):
            attraction_data = {
                'price': price.strip(),
                'rating': rating.strip() if rating.strip() else None  
            }
            attractions_data.append(attraction_data)

        return attractions_data


def main():
    preferences = get_user_preferences()
    #hotel_scrape(preferences)
    print(activity_scrape(preferences))

if __name__ == '__main__':
    main()