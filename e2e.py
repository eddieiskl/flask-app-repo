from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize the Chrome driver
driver = webdriver.Chrome()

# Open the application URL
driver.get('http://localhost:8777/score')

# Wait for the element with ID 'score' to be visible (max wait time: 10 seconds)
try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'score'))
    )
    print(f"Test Passed: Found score element with text: {element.text}")
except Exception as e:
    print("Test Failed: Score content not found!")
    print(e)
finally:
    driver.quit()