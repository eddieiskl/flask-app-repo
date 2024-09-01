from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Set up the browser driver (e.g., Chrome)
driver = webdriver.Chrome()

# Navigate to the application URL
driver.get('http://localhost:8777')

# Example test: Check if the Scores.txt content is displayed on the page
try:
    element = driver.find_element(By.ID, 'score-content')
    print("Test Passed: Score content found!")
except:
    print("Test Failed: Score content not found!")
    driver.quit()
    raise Exception("Test Failed")

# Close the browser
driver.quit()