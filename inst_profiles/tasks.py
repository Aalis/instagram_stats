from celery import shared_task
from selenium import webdriver
from chromedriver_autoinstaller import install as install_chromedriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from lxml import html
from .models import InstProfile
from inst_history.models import InstHistory
from django.utils import timezone
from selenium.common.exceptions import TimeoutException
import time
import random
from celery.utils.log import get_task_logger
from decouple import config

logger = get_task_logger(__name__)


class ChromeDriverManager:
    def __enter__(self):
        self.chrome_driver = None
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.chrome_driver:
            self.chrome_driver.quit()

    def initialize_chrome_driver(self, user_agent=None):
        print("initialize_chrome_driver is called")
        if self.chrome_driver is None:
            driver_path = install_chromedriver()
            chrome_options = ChromeOptions()
            # chrome_options.add_argument("--headless")  # Run in headless mode
            if user_agent:
                chrome_options.add_argument(f"user-agent={user_agent}")
            self.chrome_driver = webdriver.Chrome(options=chrome_options)
        return self.chrome_driver

    def rotate_user_agent(self, user_agents):
        return random.choice(user_agents)

    def login_to_instagram(self, username, password):
        try:
            self.chrome_driver.get("https://www.instagram.com/accounts/login/")

            WebDriverWait(self.chrome_driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )

            username_input = self.chrome_driver.find_element(By.NAME, "username")
            password_input = self.chrome_driver.find_element(By.NAME, "password")

            username_input.send_keys(username)
            password_input.send_keys(password)

            password_input.send_keys(Keys.RETURN)

            WebDriverWait(self.chrome_driver, 10).until(
                EC.url_changes("https://www.instagram.com/accounts/login/")
            )

            logger.info("Successfully logged in.")
        except TimeoutException:
            logger.error("Login failed. Timeout.")
            raise


@shared_task
def get_followers_count(profile_url):
    try:
        username = config("INSTAGRAM_USERNAME")
        password = config("INSTAGRAM_PASSWORD")

        with ChromeDriverManager() as manager:
            chrome_driver = manager.initialize_chrome_driver()
            manager.login_to_instagram(username, password)

            chrome_driver.get(profile_url)

            WebDriverWait(chrome_driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "_acan"))
            )

            soup = BeautifulSoup(chrome_driver.page_source, "lxml")
            root = html.fromstring(str(soup))
            followers_count = root.xpath('//span[@class="_ac2a"]/@title')[0]
            followers_count_numeric = "".join(filter(str.isdigit, followers_count))

            inst_profile, created = InstProfile.objects.get_or_create(
                link=profile_url, defaults={"followers_count": followers_count_numeric}
            )

            if not created:
                inst_profile.followers_count = followers_count_numeric
                inst_profile.save()

    except TimeoutException:
        logger.error("Login failed. Timeout.")
        raise


@shared_task
def update_followers_count():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.1234.5678 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15",
    ]

    with ChromeDriverManager() as manager:
        chrome_driver = manager.initialize_chrome_driver()

        username = config("INSTAGRAM_USERNAME")
        password = config("INSTAGRAM_PASSWORD")

        manager.login_to_instagram(username, password)

        try:
            inst_profiles = InstProfile.objects.all()

            for inst_profile in inst_profiles:
                try:
                    if inst_profile.link:
                        user_agent = manager.rotate_user_agent(user_agents)
                        chrome_driver.get(inst_profile.link)

                        WebDriverWait(chrome_driver, 10).until(
                            EC.presence_of_element_located((By.CLASS_NAME, "_acan"))
                        )

                        soup = BeautifulSoup(chrome_driver.page_source, "lxml")
                        root = html.fromstring(str(soup))
                        followers_count = root.xpath('//span[@class="_ac2a"]/@title')[0]
                        followers_count_numeric = "".join(
                            filter(str.isdigit, followers_count)
                        )

                        inst_profile.followers_count = followers_count_numeric
                        inst_profile.save()

                        InstHistory.objects.create(
                            profile=inst_profile,
                            followers_count=followers_count_numeric,
                            created_at=timezone.now(),
                        )

                        countdown_seconds = random.uniform(5, 10)
                        logger.info(f"Waiting for {countdown_seconds} seconds.")
                        time.sleep(countdown_seconds)

                    else:
                        logger.warning("Profile link is None.")
                except TimeoutException as te:
                    logger.error(f"TimeoutException: {te}")
                except Exception as e:
                    logger.error(f"An error occurred: {e}")
        finally:
            # Close the Chrome driver after processing all profiles
            chrome_driver.quit()
