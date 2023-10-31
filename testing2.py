from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

testusername = "ant3"
password = "Elmo123098"
custom_time = 2

# Create a WebDriver instance (e.g., for Chrome)
driver = webdriver.Chrome()

try:
    # Set the User-Agent string
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
    driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": user_agent})

    #Cookies Area
    cookies = driver.get_cookies()

    for cookie in cookies:
        driver.add_cookie(cookie)
    
    # Register
    driver.get("http://127.0.0.1:5000/auth/register")
    time.sleep(custom_time)
    username = driver.find_element(By.NAME, "user_name")
    password_element = driver.find_element(By.NAME, "password")
    register = driver.find_element(By.NAME, "submit")

    username.send_keys(testusername)
    password_element.send_keys(password)
    register.click()

    # Log in
    driver.get("http://127.0.0.1:5000/auth/login")
    time.sleep(custom_time)
    username = driver.find_element(By.NAME, "user_name")
    password_element = driver.find_element(By.NAME, "password")
    login = driver.find_element(By.NAME, "submit")

    username.send_keys(testusername)
    password_element.send_keys(password)
    login.click()

    # Browse trakcs
    driver.get("http://127.0.0.1:5000/browse")
    time.sleep(custom_time)
    card = driver.find_element(By.CLASS_NAME, 'test')
    card.click()
    time.sleep(1000)




except Exception as e:
    print("An error occurred:", str(e))

finally:
    # Close the browser window
    driver.quit()
