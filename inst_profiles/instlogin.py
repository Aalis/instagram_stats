# from celery import shared_task
# from decouple import config
# from selenium import webdriver
# from chromedriver_autoinstaller import install as install_chromedriver
# from selenium.webdriver.chrome.options import Options as ChromeOptions
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.keys import Keys
# from bs4 import BeautifulSoup
# from lxml import html
# from .models import InstProfile
# from inst_history.models import InstHistory
# from django.utils import timezone
# from selenium.common.exceptions import TimeoutException
# import time
# import random
# from celery.utils.log import get_task_logger

# logger = get_task_logger(__name__)


# def initialize_chrome_driver(user_agent=None):
#     driver_path = install_chromedriver()
#     chrome_options = ChromeOptions()
#     if user_agent:
#         chrome_options.add_argument(f"user-agent={user_agent}")

#     return webdriver.Chrome(options=chrome_options)


# def rotate_user_agent(user_agents):
#     return random.choice(user_agents)


# @shared_task
# def get_followers_count(profile_url):
#     chrome_driver = initialize_chrome_driver()

#     try:
#         # Log in to Instagram
#         login_to_instagram(chrome_driver)

#         with chrome_driver:
#             chrome_driver.get(profile_url)
#             WebDriverWait(chrome_driver, 10).until(
#                 EC.presence_of_element_located((By.CLASS_NAME, "_acan"))
#             )
#             soup = BeautifulSoup(chrome_driver.page_source, "lxml")
#             root = html.fromstring(str(soup))
#             followers_count = root.xpath('//span[@class="_ac2a"]/@title')[0]
#             followers_count_numeric = "".join(filter(str.isdigit, followers_count))
#             inst_profile, created = InstProfile.objects.get_or_create(
#                 link=profile_url, defaults={"followers_count": followers_count_numeric}
#             )
#             if not created:
#                 inst_profile.followers_count = followers_count_numeric
#                 inst_profile.save()
#     finally:
#         chrome_driver.quit()


# def login_to_instagram(driver):
#     # Navigate to Instagram login page
#     driver.get("https://www.instagram.com/accounts/login/")

#     # Wait for the login form to load
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.NAME, "username"))
#     )

#     # Find username and password fields and enter credentials
#     username_input = driver.find_element(By.NAME, "username")
#     password_input = driver.find_element(By.NAME, "password")

#     username_input.send_keys(config("INSTAGRAM_USERNAME"))
#     password_input.send_keys(config("INSTAGRAM_PASSWORD"))

#     # Submit the login form
#     password_input.send_keys(Keys.RETURN)

#     # Wait for the login process to complete
#     WebDriverWait(driver, 10).until(
#         EC.url_changes("https://www.instagram.com/accounts/login/")
#     )

#     print("Successfully logged in.")
