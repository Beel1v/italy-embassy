import logging
import time

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.config import (
    get_prenotami_password,
    get_prenotami_user,
    get_tg_subscribed_users,
    get_tg_token,
)
from src.logger import CustomLogger
from src.notifier import send_telegram_message

logger = CustomLogger.make_logger()


def send_message(message: str) -> None:
    token = get_tg_token()
    users = get_tg_subscribed_users()
    for user in users:
        send_telegram_message(message, str(user), token)


def _login(driver: ChromeDriver) -> None:
    wait = WebDriverWait(driver, 30)
    wait.until(EC.presence_of_element_located((By.ID, "login-email")))
    time.sleep(2)
    username = driver.find_element(By.ID, "login-email")
    username.clear()
    username.send_keys(get_prenotami_user())
    password = driver.find_element(By.ID, "login-password")
    password.clear()
    password.send_keys(get_prenotami_password())
    driver.find_element(By.CLASS_NAME, "button").click()


def _book(driver: ChromeDriver) -> None:
    wait = WebDriverWait(driver, 30)
    by, value = (
        By.XPATH,
        "/html/body/main/div[3]/div/table/tbody/tr[2]/td[4]/a/button",
    )
    wait.until(EC.presence_of_element_located((by, value)))
    driver.find_element(by, value).click()


def _get_message(driver: ChromeDriver) -> str:
    wait = WebDriverWait(driver, 30)
    by, value = By.CLASS_NAME, "jconfirm-content"
    wait.until(EC.presence_of_element_located((by, value)))
    a = driver.find_element(by, value)
    return a.text


def _open(driver: ChromeDriver) -> None:
    driver.get("https://www.google.com/")
    time.sleep(1)
    driver.get("https://prenotami.esteri.it/Services")


def check_dates() -> None:
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Chrome(options=options)
    try:
        _open(driver)
        _login(driver)
        _book(driver)
        message = _get_message(driver)
        if "Sorry" in message:
            logging.info("0: No meetings available")
        else:
            send_message("Available slots! Hurry up!!!")
        time.sleep(2)
    except Exception:
        send_message("Exception: element not found")
        logger.exception("Exception")
    finally:
        driver.quit()


if __name__ == "__main__":
    check_dates()
