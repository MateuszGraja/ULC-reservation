import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests

def listToString(s):
    """Converts a list of characters into a string."""
    return "".join(s)

def message():
    """Sends a message to Discord using a webhook."""
    message = "<@1234567890>Reserved!!!"            #change this numbers to your Discord User ID
    message = listToString(message)
    url = "webhook url"                             #paste your server webhook URL

    data = {
        "content": message,
        "username": "Essa"
    }

    try:
        result = requests.post(url, json=data)
        result.raise_for_status()
        print(f"Payload delivered successfully, code {result.status_code}.")
    except requests.exceptions.HTTPError as err:
        print(f"Error sending message: {err}")

def login(driver):
    """Logs into the ULC website."""
    try:
        print("Navigating to the login page...")
        driver.get("https://app.ulc.gov.pl/")
        time.sleep(2)

        print("Entering PIN...")
        pin = driver.find_element(By.ID, "pub2_login_pin")
        pin.send_keys("YOUR_PIN")                           # Replace with your own PIN

        print("Entering birth date...")
        birthdate = driver.find_element(By.ID, "pub2_login_birthdate")
        birthdate.send_keys("12-12-1234")                   # Change the birth date in format dd-mm-yyyy

        print("Entering password...")
        password = driver.find_element(By.ID, "pub2_login_password")
        password.send_keys("YOUR_PASSWORD")                 # Replace with your own password

        print("Clicking PIN...")
        pin.click()

        print("Accepting terms and conditions...")
        driver.find_element(By.ID, "pub2_login_accept").click()
        time.sleep(1)

        print("Clicking the second button...")
        driver.find_elements(By.TAG_NAME, "button")[1].click()
        time.sleep(1)

        print("Clicking the button with class 'btn'...")
        driver.find_elements(By.CLASS_NAME, "btn")[0].click()
        time.sleep(1)

        print("Clicking the first element with class 'list-group-item'...")
        driver.find_elements(By.CLASS_NAME, "list-group-item")[0].click()
    except Exception as e:
        print(f"Error during login: {e}")
        raise

def select_application(driver):
    """Selects the appropriate type of application from the dropdown list."""
    try:
        print("Selecting the appropriate application...")
        select = Select(driver.find_element(By.ID, 'pub2_reservation_application'))
        select.select_by_value('12345')             # Change to the value corresponding to the selected application(how to get it described on github)
        print("Application selected!")
    except Exception as e:
        print(f"Error selecting application: {e}")
        raise

def main(driver):
    """Main function handling the reservation process."""
    try:
        print("Refreshing the page...")
        driver.refresh()
        time.sleep(1)

        select_application(driver)
        time.sleep(1)

        print("Searching for elements with class 'bg-success'...")
        arr = driver.find_elements(By.CLASS_NAME, "bg-success")

        for el in arr:
            try:
                header = el.find_elements(By.CLASS_NAME, "card-header")[0].get_attribute('innerHTML')
                print(f"Found header: {header}")
                if header == "Friday<br>13-12-2024":                # Change date that you want to reserve "Day_name<br>dd-mm-yyyy"
                    print("Found the appropriate date, clicking the button...")
                    el.find_elements(By.TAG_NAME, "button")[0].click()
                    message()
                    return False
            except Exception as e:
                print(f"Error processing element: {e}")

        print("Did not find the appropriate date, continuing to refresh...")
        return True
    except Exception as e:
        print(f"Error in main function: {e}")
        return True

def initialize_driver():
    """Initializes the Chrome browser with appropriate options."""
    try:
        print("Initializing Chrome browser...")
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")  # Optionally: start the browser in maximized mode
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    except Exception as e:
        print(f"Error initializing ChromeDriver: {e}")
        raise

def run_refresh_task(driver):
    """Function to perform refreshing and checking for appointments for 30 seconds."""
    try:
        start_time = time.time()
        duration = 30                               # Duration of refreshing in seconds

        while True:
            elapsed_time = time.time() - start_time
            if elapsed_time > duration:
                print("30 seconds have passed. Ending refresh.")
                break

            continue_refresh = main(driver)
            if not continue_refresh:
                print("Appointment found. Ending refresh.")
                break

            time.sleep(5)                           # Refresh every 5 seconds
    except Exception as e:
        print(f"Exception in run_refresh_task: {e}")

def calculate_next_run():
    """Calculates the next time marker (on the full 10-minute mark) and the start time (1 minute before)."""
    now = datetime.datetime.now()
    minutes = (now.minute // 10 + 1) * 10
    if minutes == 60:
        minutes = 0
        next_hour = now.hour + 1
    else:
        next_hour = now.hour
    try:
        next_run = now.replace(hour=next_hour, minute=minutes % 60, second=0, microsecond=0)
    except ValueError:
        next_run = (now + datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    if next_run <= now:
        next_run += datetime.timedelta(hours=1)
    start_time = next_run - datetime.timedelta(minutes=1)
    return start_time, next_run

def wait_until(target_time):
    """Waits until the specified time (datetime object)."""
    now = datetime.datetime.now()
    wait_seconds = (target_time - now).total_seconds()
    if wait_seconds > 0:
        print(f"Waiting for {int(wait_seconds)} seconds until {target_time.strftime('%Y-%m-%d %H:%M:%S')}")
        time.sleep(wait_seconds)
    else:
        print(f"Time {target_time.strftime('%Y-%m-%d %H:%M:%S')} has already passed.")

def run_task():
    """Main function managing the script's execution cycle."""
    while True:
        try:
            start_time, next_run = calculate_next_run()

            wait_until(start_time)

            print(f"Starting browser and logging in at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

            driver = initialize_driver()
            login(driver)

            wait_until(next_run)

            print(f"Starting refresh and checking for appointments at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

            run_refresh_task(driver)

        except Exception as e:
            print(f"Exception in run_task: {e}")
        finally:
            print("Closing the browser...")
            try:
                driver.quit()
            except:
                pass
            print("Task completed.\n")

if __name__ == "__main__":
    run_task()
