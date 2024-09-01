from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("http://localhost:5000/score")

try:
    score_element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "current_score"))
    )
    print("Element found:", score_element.text)
except Exception as e:
    print("Error:", e)
    print(driver.page_source)
finally:
    driver.quit()