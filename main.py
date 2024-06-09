from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import genetic
from datetime import datetime
import pandas as pd
import re


# need to map destinations to attraction IDs lol
DESTINATION_ATTRACTION_IDS = {
    "greece": "100036",
    "los-angeles": "120518",
    "rome": "303",
    "milan" : "304", 
    "frankfurt" : "305", 
    "berlin" : "306",
    "paris" : "308",
    "new-york": "248",
    "atlanta": "944",
    "tokyo": "294",
    "las-vegas": "252",
    "osaka": "293",
    "san-francisco": "249",
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
        
        browser.close()

        return hotels_list

def activity_scrape(preferences):
    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)
        activity_page = browser.new_page()

        destination = preferences['destination'].replace(" ", "-")
        attraction_id = DESTINATION_ATTRACTION_IDS.get(destination)
        if not attraction_id:
            print(f"Error: No attraction ID found for destination '{preferences['destination']}'")
            return None

        activity_url = f"https://us.trip.com/travel-guide/attraction/{destination}-{attraction_id}/tourist-attractions/?locale=en-US&curr=USD"

        activity_page.goto(activity_url, timeout = 60000)

        activity_page.wait_for_load_state('networkidle')

        activities = activity_page.locator('//div[@class="card-right"]').all()

        activities_list = []
        for activity in activities: 
            activity_dict = {}
            numbered_title = activity.locator('//div[@class="poi-name margin-bottom-gap"]/h3').inner_text()
            title = re.sub(r'^\d+\. ', '', numbered_title)
            activity_dict["title"] = title
            try:
                price = float(activity.locator('//div[@class="tour-price"]/span').inner_text(timeout=10).replace('$', '').replace(',', ''))
            except PlaywrightTimeoutError:
                price = 0
            activity_dict["price"] = price
            rating = float(activity.locator('//span[@class="rating"]').inner_text())
            activity_dict["rating"] = rating
            activities_list.append(activity_dict)

        browser.close()
        
        return activities_list

def main():
    preferences = get_user_preferences()
    hotels = hotel_scrape(preferences)
    activities = activity_scrape(preferences)

    budget = float(preferences['budget'])
    trip_length = (datetime.strptime(preferences['return_date'], "%Y-%m-%d") - datetime.strptime(preferences['start_date'], "%Y-%m-%d")).days

    population_size = 20
    generations = 50
    mutation_rate = 0.1


    """activities = [
        {'name': 'Touring Universal Studios Hollywood', 'cost': 100, 'value': 9.5},
        {'name': 'Enjoying a day at Disneyland Resort', 'cost': 150, 'value': 9.5},
        {'name': 'Taking a studio tour at Warner Bros. Studio', 'cost': 60, 'value': 9.0},
        {'name': 'Watching a concert at the Hollywood Bowl', 'cost': 50, 'value': 9.0},
        {'name': 'Attending a performance at the Greek Theatre', 'cost': 50, 'value': 9.0},
        {'name': 'Visiting the Los Angeles County Museum of Art (LACMA)', 'cost': 25, 'value': 9.0},
        {'name': 'Attending a game at Dodger Stadium', 'cost': 30, 'value': 8.5},
        {'name': 'Visiting the Getty Center', 'cost': 20, 'value': 9.0},
        {'name': 'Taking a scenic drive along Pacific Coast Highway', 'cost': 0, 'value': 8.0},
        {'name': 'Exploring the Griffith Observatory', 'cost': 0, 'value': 8.5},
        {'name': 'Shopping on Rodeo Drive', 'cost': 0, 'value': 8.0},
        {'name': 'Strolling along Santa Monica Pier', 'cost': 0, 'value': 8.0},
        {'name': 'Attending a live taping of a TV show', 'cost': 0, 'value': 8.0},
        {'name': 'Exploring Venice Beach', 'cost': 0, 'value': 7.5},
        {'name': 'Hiking in Griffith Park', 'cost': 0, 'value': 8.5},
        {'name': 'Biking along the Venice Beach Boardwalk', 'cost': 0, 'value': 7.5},
        {'name': 'Checking out the Hollywood Walk of Fame', 'cost': 0, 'value': 7.0},
        {'name': 'Exploring the Museum of Contemporary Art (MOCA)', 'cost': 15, 'value': 8.0},
        {'name': 'Exploring the California Science Center', 'cost': 0, 'value': 8.0},
        {'name': 'Taking a scenic drive along Mulholland Drive', 'cost': 0, 'value': 8.0},
        {'name': 'Exploring the Japanese American National Museum', 'cost': 12, 'value': 8.0},
        {'name': 'Attending a performance at the Ahmanson Theatre', 'cost': 50, 'value': 9.0},
        {'name': 'Visiting the Griffith Park Merry-Go-Round', 'cost': 0, 'value': 7.0},
        {'name': 'Relaxing at Echo Park Lake', 'cost': 0, 'value': 7.5}
    ]"""

    best_individual = genetic.run_multiple_times(250, budget, hotels, activities, trip_length, population_size, generations, mutation_rate)

    if best_individual:
        print("Best Trip Plan:")
        print(f"Hotel: {best_individual['place']['hotel']} - Cost: {best_individual['place']['price']}, Rating: {best_individual['place']['rating']}")
        
        total_cost = genetic.calculate_cost(best_individual, trip_length)
        total_value = float(best_individual['place']['rating'])

        for activity in best_individual['activities']:
            print(f"Activity: {activity['title']} - Cost: ${activity['price']}, Value: {activity['rating']}")
            total_value += activity['rating']
        
        print(f"Total Cost: ${total_cost}")
        print(f"Total Value: {total_value}")
    else:
        print("No suitable trip found within the budget.")

    

if __name__ == '__main__':
    main()