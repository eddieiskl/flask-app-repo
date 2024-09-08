from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

try:
    driver.get('http://localhost:8777/score')

    # Print the error message if score can't be read
    score_element = driver.find_element(By.ID, 'current_score')
    score_text = score_element.text

    print(score_text)  # Check what the score text actually says

    if "Could not read the score" not in score_text:
        print(f"Test Passed: Found current score element with text: {score_text}")
    else:
        print(f"Test Failed: {score_text}")
finally:
    driver.quit()