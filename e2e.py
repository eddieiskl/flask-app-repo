from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

# Update the URL to match the port 8777
driver.get('http://localhost:8777/score')

try:
    element = driver.find_element(By.ID, 'score')
    print(f"Test Passed: Score is {element.text}")
except Exception as e:
    print("Test Failed: Score content not found!")
    print(e)
    raise Exception("Test Failed")

driver.quit()