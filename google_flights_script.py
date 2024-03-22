from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
from dotenv import load_dotenv
import os

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

consent_url = "https://consent.google.com/m?continue=https://www.google.com/travel/flights/search?tfs%3DCBwQAhotEgoyMDI0LTAyLTA4MgJMT2oMCAISCC9tLzA0OTF5cg0IAhIJL20vMDk5NDltGi0SCjIwMjQtMDItMTUyAkxPag0IAhIJL20vMDk5NDltcgwIAhIIL20vMDQ5MXlAAUgBcAGCAQsI____________AZgBAQ&gl=PL&m=0&pc=trv&cm=2&hl=pl&src=1"

firefox_options = Options()
firefox_options.add_argument("-private")

driver = webdriver.Firefox(options=firefox_options)

driver.get(consent_url)

try:
    # cookie_button = WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.CLASS_NAME, "VfPpkd-dgl2Hf-ppHlrf-sM5MNb"))
    # )

    # cookie_button.click()

    # WebDriverWait(driver, 10).until(
    #     EC.url_to_be("https://www.google.com/travel/flights")
    # )


    div_element = driver.find_element(By.CLASS_NAME, "YMlIz.FpEdX.jLMuyc")

    span_element = div_element.find_element(By.TAG_NAME, "span")

    button_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (
                By.CSS_SELECTOR,
                ".VfPpkd-LgbsSe.VfPpkd-LgbsSe-OWXEXe-Bz112c-M1Soyc.ksBjEc.lKxP2d.LQeN7.uRHSYe.JgWerc",
            )
        )
    )

    ActionChains(driver).move_to_element(button_element).click().perform()


    div_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".QB2Jof.DmxQAb"))
    )

    text_array = [element.text for element in div_elements]

    sliced_text_array = [element.split(" z", 1)[0] for element in text_array]

    converted_integers = []
    for element in sliced_text_array:
        cleaned_element = "".join(element.split())
        try:
            converted_integers.append(int(cleaned_element))
        except ValueError:
            converted_integers.append(None)

    smallest_integer = min(filter(lambda x: x is not None, converted_integers), default=None)
    print("Smallest price:", smallest_integer)


finally:
    driver.quit()


if smallest_integer < 800:
    # Replace these values with your own info
    sender_email = os.getenv('SENDER')
    receiver_email = os.getenv('RECEIVER')
    password = os.getenv('PASSWORD')

    subject = "Lot Krakow Istanbul za " + str(smallest_integer) + " PLN!"
    body = "Dobra cena??"
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

    print("Email sent successfully!")

else:
    print("Too expensive...")

