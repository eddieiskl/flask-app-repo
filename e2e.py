from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

# Test the /score endpoint
driver.get('http://localhost:8777/score')

try:
    element = driver.find_element(By.ID, 'score')
    print(f"Test Passed: Found score element with text: {element.text}")
except:
    print("Test Failed: Score content not found!")
finally:
    driver.quit()