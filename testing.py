from playwright.sync_api import sync_playwright
import pandas as pd

def hotels(destination, checkin, checkout, num_people):

    with sync_playwright() as p:
        url = f'https://www.booking.com/searchresults.html?ss={destination}&checkin={checkin}&checkout={checkout}&group_adults={num_people}&no_rooms=1&group_children=0'
        print(url)
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url, timeout=60000)

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

def main2():

    with sync_playwright() as p:
        url = 'https://www.expedia.com/Hotel-Search?destination=New%20York%20%28and%20vicinity%29%2C%20New%20York%2C%20United%20States%20of%20America&regionId=178293&latLong=40.75668%2C-73.98647&flexibility=0_DAY&d1=2024-05-12&startDate=2024-05-12&d2=2024-05-16&endDate=2024-05-16&adults=2&rooms=1&theme=&userIntent=&semdtl=&useRewards=false&sort=RECOMMENDED'

        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url, timeout=60000)

        hotels = page.locator('//*[@class="uitk-spacing uitk-spacing-margin-blockstart-three"]').all()
        
        i = 0
        hotels_list = []
        for hotel in hotels:
            if i == 0:
                i+=1
                continue
            hotel_dict = {}
            hotel_dict['hotel'] = hotel.locator('//*[@class="uitk-layout-grid uitk-layout-grid-has-auto-columns uitk-layout-grid-has-rows uitk-layout-grid-display-grid uitk-layout-flex-item"]').inner_text()

            hotels_list.append(hotel_dict)


        print(hotels_list)
        df = pd.DataFrame(hotels_list)

        browser.close()

def main3():

    with sync_playwright() as p:
        url = 'https://travel.usnews.com/New_York_NY/Things_To_Do/'

        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url, timeout=60000)

        things = page.locator("//*[contains(concat(' ', normalize-space(@class), ' '), ' GenericList__ListItemContainer-tjuxmv-1 exYsXw ')]").all()
        
        i = 0
        thing_list = []
        for thing in things:
            if i == 0:
                i+=1
                continue
            thing_dict = {}
            thing_dict['name'] = thing.locator('//*[@class="uitk-layout-grid uitk-layout-grid-has-auto-columns uitk-layout-grid-has-rows uitk-layout-grid-display-grid uitk-layout-flex-item"]').inner_text()

            thing_list.append(thing_dict)


        print(thing_list)


        browser.close()
if __name__ == '__main__':
    #formated - orlando, 2024-05-10, 2024-05-14, 2
    #for two words use - "new+york"
    destination = "orlando"
    checkin = "2024-05-12"
    checkout = "2024-05-18"
    people = 1
    hotels(destination, checkin, checkout, people)
    

