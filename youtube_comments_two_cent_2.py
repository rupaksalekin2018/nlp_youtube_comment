# Import necessary libraries
import pandas as pd  # For data manipulation and analysis
import time  # To pause the script for a specified amount of time
from selenium import webdriver  # Core Selenium tools
from selenium.webdriver.chrome.service import Service  # To manage ChromeDriver service
from selenium.webdriver.support.ui import WebDriverWait  # To use Selenium's explicit waits
from selenium.webdriver.common.by import By  # To locate elements by their type
from selenium.webdriver.support import expected_conditions as EC  # To specify certain conditions for explicit waits
from selenium.webdriver.common.keys import Keys  # To simulate keyboard keys

# YouTube video URL to scrape
video_to_scrape = "https://www.youtube.com/watch?v=XcnEYDazhFQ&t=469s"

# Set up the Chrome WebDriver
chrome_path = "/opt/homebrew/bin/chromedriver"  # Path to your ChromeDriver
chrome_service = Service(chrome_path)  # Initialize ChromeDriver service
driver = webdriver.Chrome(service=chrome_service)  # Start Chrome using the ChromeDriver
driver.get(video_to_scrape)  # Open the specified YouTube video

# Initialize variables for scrolling and scraping logic
SCROLL_PAUSE_TIME = 2  # Time to pause after each scroll, allowing the page to load
delay = 30  # Max time to wait for elements to be located
scrolling = True  # Flag to indicate if we should continue scrolling
last_height = driver.execute_script("return document.documentElement.scrollHeight")  # Current scroll height of the document
all_comments_data = []  # List to store all scraped comments data

# Function to scrape loaded comments on the page
def scrape_loaded_comments():
    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="comments"]')))  # Wait until the comments section is present
    all_usernames = driver.find_elements(By.XPATH, '//h3[@class="style-scope ytd-comment-renderer"]')  # Find all usernames
    all_comments = driver.find_elements(By.XPATH, '//yt-formatted-string[@id="content-text"]')  # Find all comments

    for username, comment in zip(all_usernames, all_comments):
        all_comments_data.append((username.text, comment.text))  # Append each username and comment as a tuple to the list

scrolling_attempt = 5  # Number of attempts to scroll to the end of the page

# Main loop for scrolling through the page and scraping comments
while scrolling:
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)  # Scroll to the end of the page
    time.sleep(SCROLL_PAUSE_TIME)  # Pause to let the page load
    scrape_loaded_comments()  # Call the function to scrape loaded comments
    
    new_height = driver.execute_script("return document.documentElement.scrollHeight")  # Calculate new scroll height after scrolling
    if new_height == last_height:  # Check if the scroll height hasn't changed
        scrolling_attempt -= 1  # Decrement the attempt counter
        if scrolling_attempt == 0:  # If no more attempts left
            scrolling = False  # Stop scrolling
    last_height = new_height  # Update the last scroll height

driver.quit()  # Close the browser

# Creating and saving the DataFrame
df = pd.DataFrame(all_comments_data, columns=['Username', 'Comment'])  # Create a DataFrame from the scraped data
df.index.name = 'Index'  # Set the index name to 'Index'
df.to_csv('youtube_comments_formatted.csv', index=True)  # Save the DataFrame to a CSV file with the index

# Display the last few rows of the dataframe
df.tail()



'''

import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

video_to_scrape = "https://www.youtube.com/watch?v=XcnEYDazhFQ&t=469s"  # YouTube Video URL

chrome_path = "/opt/homebrew/bin/chromedriver"
chrome_service = Service(chrome_path)
driver = webdriver.Chrome(service=chrome_service)
driver.get(video_to_scrape)

SCROLL_PAUSE_TIME = 2
delay = 30
scrolling = True
last_height = driver.execute_script("return document.documentElement.scrollHeight")
all_comments_data = []  # Store username and comment as tuples

def scrape_loaded_comments():
    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="comments"]')))
    all_usernames = driver.find_elements(By.XPATH, '//h3[@class="style-scope ytd-comment-renderer"]')
    all_comments = driver.find_elements(By.XPATH, '//yt-formatted-string[@id="content-text"]')

    for username, comment in zip(all_usernames, all_comments):
        all_comments_data.append((username.text, comment.text))  # Append as tuple

scrolling_attempt = 5

while scrolling:
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    time.sleep(SCROLL_PAUSE_TIME)
    scrape_loaded_comments()
    
    new_height = driver.execute_script("return document.documentElement.scrollHeight")
    if new_height == last_height:
        scrolling_attempt -= 1
        if scrolling_attempt == 0:
            scrolling = False
    last_height = new_height

driver.quit()

# Creating DataFrame
df = pd.DataFrame(all_comments_data, columns=['Username', 'Comment'])
df.index.name = 'Index'

# Saving to CSV
df.to_csv('youtube_comments_formatted.csv', index=True)

# Display the last few rows of the dataframe
df.tail()


'''