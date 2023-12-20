from selenium.webdriver import Chrome, ChromeOptions
from bs4 import BeautifulSoup
import re
import csv
import time

chrome_options = ChromeOptions()
driver = Chrome(options=chrome_options)
# Add or remove options based on your requirements
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-gpu")

# Set the session ID and CSRF token as cookies
driver.get("https://www.instagram.com/")
driver.add_cookie({'name': 'sessionid', 'value': '#Enter id', 'domain': '.instagram.com'})
driver.add_cookie({'name': 'csrftoken', 'value': '#Enter tocken', 'domain': '.instagram.com'})

try:
    time.sleep(3)

    # Proceed to the user's profile
    username = "#username"  # Replace 'target_username' with your desired username variable
    profile_url = f"https://www.instagram.com/{username}/"
    driver.get(profile_url)

    time.sleep(3)   
    # Scroll to load more posts (you may adjust the number of scrolls as needed)
    prev_height = 0
    new_height = driver.execute_script("return document.body.scrollHeight")

    # Scroll through the entire page content
    while prev_height != new_height:
        prev_height = new_height
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(6)
        new_height = driver.execute_script("return document.body.scrollHeight")

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    all_links = soup.find_all('a', href=True)

    # Filter and collect only the post URLs following the pattern https://www.instagram.com/p/*
    post_urls = []
    for link in all_links:
        if re.match(r'^/p/', link['href']):
            post_urls.append(f"https://www.instagram.com{link['href']}")

    # Save the post URLs to a CSV file
    with open('instagram_post.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # writer.writerow([''])
        writer.writerows([[url] for url in post_urls])

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Quit the webdriver to release resources
    driver.quit()
