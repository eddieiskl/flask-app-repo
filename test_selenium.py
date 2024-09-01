from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import traceback

def test_scores_service(app_url):
    # Initialize the WebDriver
    driver = webdriver.Chrome()

    try:
        # Open the application URL
        driver.get(app_url)

        # Wait until the current score element is present on the page
        score_element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "current_score"))
        )

        # Extract the score text and parse the number
        score_text = score_element.text  # This will give you the full text like "Your current score is: 8"
        score = int(score_text.split()[-1])  # Extract the actual score number from the text

        # Check if the score is between 1 and 1000
        if 1 <= score <= 1000:
            return True
        else:
            return False

    except Exception as e:
        print("An error occurred during the test:")
        print(driver.page_source)  # Print the HTML source of the page
        traceback.print_exc()
        return False

    finally:
        # Close the browser
        driver.quit()

def main_function():
    # The URL of your Flask application
    app_url = "http://localhost:5000/score"  # Correct URL for the score page

    # Run the test
    if test_scores_service(app_url):
        print("Test passed!")
        return 0
    else:
        print("Test failed!")
        return -1

if __name__ == "__main__":
    exit(main_function())