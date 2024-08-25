from seleniumbase import Driver
from selenium.webdriver.common.by import By
import json
from time import sleep


def initialize_driver():
    driver = Driver(uc=True, headless=True)
    print("Driver initialized.")
    return driver


def get_property_data_loop(driver, base_url):
    all_property_data = []
    page_number = 1  # Start from page 1

    while True:  # Continue until there are no more listings
        print(f"Scraping page {page_number}...")
        url = base_url + str(page_number)
        driver.get(url)
        sleep(1)

        try:
            element = driver.find_element(By.ID, "__NEXT_DATA__")
            attribute_value = element.get_attribute("innerHTML")
            json_data = json.loads(attribute_value)
            property_listings = json_data["props"]["pageProps"]["searchResult"][
                "listings"
            ]
        except Exception as e:
            print(f"Error occurred: {e}")
            break  # Exit if there's an error finding the element

        if not property_listings:  # Check if the listings are empty
            print("No more listings found. Stopping scraping.")
            break  # Stop the loop if no listings

        all_property_data.extend(property_listings)
        page_number += 1  # Move to the next page

    return all_property_data


def save_data_to_json(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def main():
    driver = initialize_driver()
    base_url = "https://www.propertyfinder.eg/en/search?c=1&fu=0&ob=nd&page="
    property_data = get_property_data_loop(driver, base_url)
    print(f"Total number of listings scraped: {len(property_data)}")
    print("Saving data to JSON file...")
    save_data_to_json(property_data, "property_data.json")
    print("Data saved to JSON file.")
    driver.quit()


if __name__ == "__main__":
    main()
