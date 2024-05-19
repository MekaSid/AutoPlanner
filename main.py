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

def activity_scrape(preferences):

    with sync_playwright() as p:
        place = preferences['destination']
        place = place.replace(" ", "-").lower()

        browser = p.chromium.launch(headless=False)
        activity_page = browser.new_page()

        activity_url = f'https://www.lonelyplanet.com/{place}/attractions'
        activity_page.goto(activity_url, timeout = 60000)

        #time.sleep(5)
        
        activity_page.wait_for_load_state('networkidle')

        activity_page.click('#ibuact-10650012671-top-getcity-293-0') #click to for location input dropdown
        time.sleep(3)
        activity_page.type('.input_val input_val_search',place) #not currently typing location in correct box
        activity_page.click('.city_list_content_item') #click first location option
        activity_page.wait_for_load_state('networkidle')
        activities = activity_page.locator('//a[@class="js-poi-card-link"]')

        #activities = activity_page.locator('//*[@id="ottd-smart-platform"]/section/div[2]/div[3]/div[2]/div/div/div[2]/div[2]/ul/li/a').all()

        activities_list = []
        for activity in activities:
            activity_dict = {}
            activity_dict['title'] = activity.inner_text()
            activity_dict['description'] = activity.parent.query_selector("p").inner_text()
            activity_dict['link'] = activity.get_attribute("href")
            activities_list.append(activity_dict)
                                                    
        print("Scraped activities:", activities_list)

        browser.close()

def main():
    preferences = get_user_preferences()
    #hotel_scrape(preferences)
    activity_scrape(preferences)
    


if __name__ == '__main__':
    main()