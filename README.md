# Automatyczne Rezerwowanie Terminów Egzaminacyjnych na ULC

Opis Projektu
Ten projekt to skrypt automatyzujący proces rezerwacji terminów egzaminacyjnych na platformie ULC (Urząd Lotnictwa Cywilnego). Skrypt automatycznie loguje użytkownika, odświeża stronę co określony interwał czasu, a w momencie, gdy dostępne są nowe terminy, wysyła powiadomienie na serwer Discord. Dzięki temu użytkownik może szybko zareagować i zarezerwować wolny termin.

Funkcjonalności
Automatyczne logowanie: Skrypt loguje użytkownika na stronie ULC przy użyciu podanych danych.
Automatyczne odświeżanie strony: Strona jest odświeżana co określony czas (domyślnie co 10 minut) w poszukiwaniu dostępnych terminów.
Powiadomienia Discord: Gdy zostanie znaleziony dostępny termin, skrypt wysyła powiadomienie na wybrany kanał Discord za pomocą webhooka.
Ręczne uzupełnianie CAPTCHA: W przypadku znalezienia terminu użytkownik musi ręcznie uzupełnić CAPTCHA, aby dokończyć proces rezerwacji.

Wymagania
- Python 3.6 lub nowszy
- Google Chrome zainstalowany na komputerze
Biblioteki Python:
- selenium
- webdriver-manager
- requests

Konfiguracja
1. Discord Bot
Uzyskaj swój Discord User ID:

Kliknij prawym przyciskiem myszy na swój profil Discord.
Wybierz opcję „Kopiuj ID użytkownika” (upewnij się, że masz włączoną opcję „Developer Mode” w ustawieniach Discorda).
Skonfiguruj wiadomość powiadamiającą:

Edytuj zmienną message w sekcji message() w kodzie:
message = "<@1234567890> Reserved!!!"  # Zamień na swój Discord User ID

Uzyskaj Webhook URL:
Wejdź w ustawienia wybranego kanału tekstowego na swoim serwerze Discord.
Przejdź do zakładki „Integracje” → „Webhooki” → „Nowy webhook”.

Skopiuj adres URL webhooka i wklej go w zmienną url:
url = "https://discord.com/api/webhooks/your_webhook_url"


2. Konfiguracja Konta ULC
Edytuj dane logowania w skrypcie:

pin.send_keys("TWÓJ_PIN")
birthdate.send_keys("dd-mm-rrrr")  # np. "12-12-1990"
password.send_keys("TWOJE_HASŁO")

3. Konfiguracja Dnia Rezerwacji
Zmodyfikuj datę, na którą chcesz zarezerwować termin:
if header == "Friday<br>13-12-2024":  # Zamień na własny dzień w formacie "Day_name<br>dd-mm-yyyy"

5. Konfiguracja Wyboru Wniosku
Można ją uzyskać klikając na stronie ulcu "zbadaj", "select element to inspect" i klikając w suwak wyboru wniosku
![image](https://github.com/user-attachments/assets/4c6bb53b-5191-4416-b686-ea755608ab96)

Zmień wartość odpowiadającą Twojemu wnioskowi:
select.select_by_value('12345')  # Zamień na własny numer wniosku

5. Konfiguracja Czasu Odświeżania Strony
6. Dostosuj częstotliwość odświeżania strony:

duration = 30  # Zmień na żądany czas trwania w sekundach
time.sleep(5)   # Zmień na żądany interwał odświeżania w sekundach

Uwagi dotyczące słabego internetu:
Jeśli masz wolniejsze połączenie internetowe, zwiększ wartości w time.sleep zarówno w funkcji main, jak i w funkcji login.
