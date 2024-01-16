import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

video_to_scrape = "https://www.youtube.com/watch?v=XcnEYDazhFQ&t=469s"
chrome_path = "/opt/homebrew/bin/chromedriver"
chrome_service = Service(chrome_path)
driver = webdriver.Chrome(service=chrome_service)
driver.get(video_to_scrape)

SCROLL_PAUSE_TIME = 2
delay = 30
scrolling = True
last_height = driver.execute_script("return document.documentElement.scrollHeight")
all_comments_data = []

def scrape_loaded_comments_and_replies():
    # Wait until the comments section is present
    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="comments"]')))

    # Expand reply threads
    reply_buttons = driver.find_elements(By.XPATH, '//yt-formatted-string[@class="more-button style-scope ytd-comment-replies-renderer"]')
    for button in reply_buttons:
        try:
            driver.execute_script("arguments[0].scrollIntoView();", button)
            button.click()
            time.sleep(1)
        except:
            continue

    # Find all usernames and comments
    all_usernames = driver.find_elements(By.XPATH, '//h3[@class="style-scope ytd-comment-renderer"]')
    all_comments = driver.find_elements(By.XPATH, '//yt-formatted-string[@id="content-text"]')

    # Append each username and comment to the list
    for username, comment in zip(all_usernames, all_comments):
        all_comments_data.append((username.text, comment.text))

scrolling_attempt = 5

while scrolling:
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    time.sleep(SCROLL_PAUSE_TIME)
    scrape_loaded_comments_and_replies()

    new_height = driver.execute_script("return document.documentElement.scrollHeight")
    if new_height == last_height:
        scrolling_attempt -= 1
        if scrolling_attempt == 0:
            scrolling = False
    last_height = new_height

driver.quit()

df = pd.DataFrame(all_comments_data, columns=['Username', 'Comment'])
df.index.name = 'Index'
df.to_csv('youtube_comments_with_replies.csv', index=True)

df.tail()
