# Automatyczne Rezerwowanie Terminów Egzaminacyjnych na ULC

---

## Opis Projektu

Ten projekt to skrypt automatyzujący proces rezerwacji terminów egzaminacyjnych na platformie ULC (Urząd Lotnictwa Cywilnego). Skrypt automatycznie loguje użytkownika, odświeża stronę co określony interwał czasu, a w momencie, gdy dostępne są nowe terminy, wysyła powiadomienie na serwer Discord. Dzięki temu użytkownik może szybko zareagować i zarezerwować wolny termin.

## Funkcjonalności

- **Automatyczne logowanie**: Skrypt loguje użytkownika na stronie ULC przy użyciu podanych danych.
- **Automatyczne odświeżanie strony**: Strona jest odświeżana co określony czas (domyślnie co 10 minut) w poszukiwaniu dostępnych terminów.
- **Powiadomienia Discord**: Gdy zostanie znaleziony dostępny termin, skrypt wysyła powiadomienie na wybrany kanał Discord za pomocą webhooka.
- **Ręczne uzupełnianie CAPTCHA**: W przypadku znalezienia terminu użytkownik musi ręcznie uzupełnić CAPTCHA, aby dokończyć proces rezerwacji.

## Wymagania

- Python 3.6 lub nowszy
- Google Chrome zainstalowany na komputerze

**Biblioteki Python**:
- `selenium`
- `webdriver-manager`
- `requests`
- `keyboard`

## Konfiguracja

### 1. Discord Bot

- **Uzyskaj swój Discord User ID**:
  - Kliknij prawym przyciskiem myszy na swój profil Discord.
  - Wybierz opcję „Kopiuj ID użytkownika” (upewnij się, że masz włączoną opcję „Developer Mode” w ustawieniach Discorda).

- **Skonfiguruj wiadomość powiadamiającą**:
  - Edytuj zmienną `message` w sekcji `message()` w kodzie:
    
    ```python
    data = {
        "content": "<@1234567890> Reserved!!!",                 #change this numbers to your Discord User ID
        "username": "Essa"
    }
    ```

- **Uzyskaj Webhook URL**:
  - Wejdź w ustawienia wybranego kanału tekstowego na swoim serwerze Discord.
  - Przejdź do zakładki „Integracje” → „Webhooki” → „Nowy webhook”.

- **Skopiuj adres URL webhooka i wklej go w zmienną `url`**:

  ```python
  url = "https://discord.com/api/webhooks/your_webhook_ur"
  ```

### 2. Konfiguracja Konta ULC

- **Edytuj dane logowania w skrypcie**:
  
  ```python
  SESSION_ID = "YOUR_SESSION_ID"
  PIN = "YOUR_PIN"
  BIRTHDATE = "dd-mm-rrrr"
  PASSWORD = "YOUR_PASSWORD"
  ```

### 3. Konfiguracja Dnia Rezerwacji

- **Zmodyfikuj datę, na którą chcesz zarezerwować termin**:

  ```python
  if header in ["Piątek<br>16-05-2025", "Pon<br>12-05-2025"]:  # Zamień na własny dzień w formacie "Day_name<br>dd-mm-yyyy"
  ```

### 4. Konfiguracja Wyboru Wniosku

- **Można ją uzyskać klikając na stronie ULC "zbadaj", "select element to inspect" i klikając w suwak wyboru wniosku**

  ![image](https://github.com/user-attachments/assets/4c6bb53b-5191-4416-b686-ea755608ab96)

- **Zmień wartość odpowiadającą Twojemu wnioskowi**:

  ```python
  APPLICATION_ID = "12345"  # Zamień na własny numer wniosku
  ```
