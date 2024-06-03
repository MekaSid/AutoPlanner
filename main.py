from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import pandas as pd
import re
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

        hotels = page.locator('//div[@data-testid="property-card"]').all()
        
        hotels_list = []
        for hotel in hotels:
            try:
                hotel_dict = {}
                hotel_dict['hotel'] = hotel.locator('//div[@data-testid="title"]').inner_text(timeout=5000)
                hotel_dict['price'] = hotel.locator('//span[@data-testid="price-and-discounted-price"]').inner_text(timeout=5000)
                
                try:
                    rating_text = hotel.locator('//div[@data-testid="review-score"]').inner_text(timeout=5000)
                    rating = re.search(r'(\d+\.\d+)', rating_text).group(1)
                    print(rating)
                except PlaywrightTimeoutError:
                    rating = '0.0'
                if not rating == '0.0':
                    hotel_dict['rating'] = rating

                price = hotel_dict['price']
                price = price.replace('$', '').replace(',', '')
                if float(price) <= float(preferences['budget']):
                    hotels_list.append(hotel_dict)
            
            except (PlaywrightTimeoutError, Exception) as e:
                continue
        
        df = pd.DataFrame(hotels_list)

        print(df)

        browser.close()



def activity_scrape(preferences):

    with sync_playwright() as p:
        place = preferences['destination']
        place = place.replace(" ", "+")

        browser = p.chromium.launch(headless=False)
        activity_page = browser.new_page()

        activity_url = 'https://us.trip.com/things-to-do/list-293/city?citytype=dt&id=293&name=Osaka&keyword=&pshowcode=Ticket2&locale=en-US&curr=USD'
        activity_page.goto(activity_url, timeout = 60000)

        #time.sleep(5)
        
        activity_page.wait_for_load_state('networkidle')

        activity_page.click('#ibuact-10650012671-top-getcity-293-0') #click to for location input dropdown
        time.sleep(3)
        activity_page.fill('.input_val', place) #not currently typing location in correct box
        activity_page.click('.associate_card_item:first-child')

        activity_page.wait_for_load_state('networkidle')


        activities = activity_page.locator('//*[@id="ottd-smart-platform"]/section/div[2]/div[3]/div[2]/div/div/div[2]/div[2]/ul/li/a').all()

        activities_list = []
        for activity in activities:
            title = activity.locator("//div[@class='poi-name margin-bottom-gap']/h3").inner_text()
            activities_list.append(title)
                                                    
        print(activities_list)

        browser.close()

def main():
    preferences = get_user_preferences()
    hotel_scrape(preferences)
    # activity_scrape(preferences)
    


if __name__ == '__main__':
    main()
