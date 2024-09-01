from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Set up the WebDriver (ensure chromedriver is in your PATH)
driver = webdriver.Chrome()

try:
    # Open the local Flask application
    driver.get("http://localhost")

    # Give some time for the page to load
    time.sleep(2)

    # Find the score element by its ID
    score_element = driver.find_element(By.ID, "score")

    # Extract the score text
    score_text = score_element.text

    # Print the score (or you can add assertions here to validate the score)
    print(f"The score is: {score_text}")

finally:
    # Close the WebDriver
    driver.quit()