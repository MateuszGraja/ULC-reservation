import time
import datetime
import keyboard
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
import requests

# === CONFIGURATION ===
SESSION_ID = "YOUR_SESSION_ID"      # Change the session ID to the one you want to reserve
PIN = "YOUR_PIN"                    # Replace with your own PIN
BIRTHDATE = "dd-mm-rrrr"            # Change the birth date in format dd-mm-yyyy
PASSWORD = "YOUR_PASSWORD"          # Replace with your own password
APPLICATION_ID = "12345"            # Change to the value corresponding to the selected application (how to get it described on github)

def message():
    url = "https://discord.com/api/webhooks/your_webhook_ur"    #paste your server webhook URL
    data = {
        "content": "<@1234567890> Reserved!!!",                 #change this numbers to your Discord User ID
        "username": "Essa"
    }
    try:
        result = requests.post(url, json=data)
        result.raise_for_status()
        print(f"Payload delivered successfully, code {result.status_code}.")
    except requests.exceptions.HTTPError as err:
        print(f"Błąd podczas wysyłania wiadomości: {err}")

def login(driver):
    try:
        driver.get("https://app.ulc.gov.pl/")
        time.sleep(2)
        driver.find_element(By.ID, "pub2_login_pin").send_keys(PIN)
        driver.find_element(By.ID, "pub2_login_birthdate").send_keys(BIRTHDATE)
        driver.find_element(By.ID, "pub2_login_password").send_keys(PASSWORD)
        driver.find_element(By.ID, "pub2_login_pin").click()
        driver.find_element(By.ID, "pub2_login_accept").click()
        time.sleep(1)
        driver.find_elements(By.TAG_NAME, "button")[1].click()
        time.sleep(1)
        driver.find_elements(By.CLASS_NAME, "btn")[0].click()
        time.sleep(1)

        session_links = driver.find_elements(By.CLASS_NAME, "list-group-item")
        for link in session_links:
            href = link.get_attribute("href")
            if href and f"sessions/{SESSION_ID}" in href:
                link.click()
                break
        else:
            raise Exception(f"Nie znaleziono sesji o ID {SESSION_ID}")
    except Exception as e:
        print(f"Błąd podczas logowania: {e}")
        raise

def select_application(driver):
    try:
        select = Select(driver.find_element(By.ID, 'pub2_reservation_application'))
        select.select_by_value(APPLICATION_ID)
    except Exception as e:
        print(f"Błąd podczas wybierania wniosku: {e}")
        raise

def check_availability(driver):
    try:
        arr = driver.find_elements(By.CLASS_NAME, "bg-success")
        for el in arr:
            try:
                header = el.find_elements(By.CLASS_NAME, "card-header")[0].get_attribute('innerHTML')
                print(f"Znaleziono nagłówek: {header}")
                if header in ["Piątek<br>16-05-2025", "Pon<br>12-05-2025"]:         # Change to the desired date
                    el.find_elements(By.TAG_NAME, "button")[0].click()
                    message()
                    return True
            except Exception as e:
                print(f"Błąd podczas przetwarzania elementu: {e}")
        return False
    except Exception as e:
        print(f"Błąd podczas sprawdzania dostępności: {e}")
        return False

def main(driver):
    try:
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Start odświeżania!")
        start_time = time.time()
        refresh_time_limit = 5
        loop_start_time = time.time()

        while time.time() - loop_start_time < refresh_time_limit:
            driver.refresh()
            select_application(driver)
            time.sleep(1)

            if check_availability(driver):
                print("Rezerwacja została dokonana. Zakończam odświeżanie.")
                return

        next_time = (datetime.datetime.now().replace(second=0, microsecond=0) + datetime.timedelta(minutes=10)).strftime('%H:%M:%S')
        print(f"Czekam do {next_time}...")
    except Exception as e:
        print(f"Błąd w funkcji main: {e}")

def initialize_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def run_task():
    driver = initialize_driver()
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Nowa instancja przeglądarki uruchomiona.")
    login(driver)

    while True:
        now = datetime.datetime.now()
        minute = now.minute
        second = now.second

        if minute % 10 == 9 and second == 0:
            print(f"[{now.strftime('%H:%M:%S')}] Restart przeglądarki minutę przed interwałem.")
            driver.quit()
            time.sleep(2)
            driver = initialize_driver()
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Nowa instancja przeglądarki uruchomiona.")
            login(driver)

        if minute % 10 == 0 and second == 0:
            main(driver)

        if second == 0:
            print(f"[{now.strftime('%H:%M')}] Czekam...")

        if keyboard.is_pressed('q'):
            print("Zatrzymuję skrypt (q).")
            driver.quit()
            break

        time.sleep(1)

if __name__ == "__main__":
    run_task()
