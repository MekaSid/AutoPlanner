from playwright.sync_api import sync_playwright
import pandas as pd

# need to map destinations to attraction IDs lol
DESTINATION_ATTRACTION_IDS = {
    "greece": "100036",
    "los-angeles": "120518"
}

def get_user_preferences():
    print("Welcome to our Trip Planner! Please complete the following survey, so we can plan your trip.")
    user_preferences = {}

    user_preferences['destination'] = input("Where would you like to travel to? ").lower() 
    user_preferences['start_date'] = input("What day do you plan on leaving? Enter as YYYY-MM-DD format. ")
    user_preferences['return_date'] = input("What day do you plan on returning? Enter as YYYY-MM-DD format. ")
    user_preferences['budget'] = input("What is your budget for the trip? ")
    user_preferences['adults'] = input("How many adults will be travelling? ")
    user_preferences['children'] = input("How many children will be travelling? ")
    user_preferences['rooms'] = input("How many rooms will you require? ")

    print("Thank you for completing our survey.")
    print(user_preferences)

    return user_preferences

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
        
        attractions_data = []
        for price in prices:
            attraction_data = {
                'price': price.strip() 
            }
            attractions_data.append(attraction_data)

        return attractions_data

def main():
    preferences = get_user_preferences()
    attractions_data = activity_scrape(preferences)
    
    if attractions_data:
        df = pd.DataFrame(attractions_data)
        print(df)

if __name__ == '__main__':
    main()
