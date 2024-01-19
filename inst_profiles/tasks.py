from celery import shared_task
from selenium import webdriver
from chromedriver_autoinstaller import install as install_chromedriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from lxml import html
from .models import InstProfile
from inst_history.models import InstHistory
from django.utils import timezone
from selenium.common.exceptions import TimeoutException
import time


@shared_task
def get_followers_count(profile_url):
    # Install ChromeDriver and get the path
    driver_path = install_chromedriver()

    # Set up the Chrome options
    chrome_options = ChromeOptions()

    # Create the Chrome WebDriver with the specified options
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(profile_url)

    # Let the page load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "_acan"))
    )

    soup = BeautifulSoup(driver.page_source, "lxml")

    # Convert BeautifulSoup object to lxml etree
    root = html.fromstring(str(soup))

    # Use XPath to extract the followers count
    followers_count = root.xpath('//span[@class="_ac2a"]/@title')[0]

    # Extract the numeric part from the title
    followers_count_numeric = "".join(filter(str.isdigit, followers_count))

    # Check if the InstProfile with the given link already exists
    inst_profile, created = InstProfile.objects.get_or_create(
        link=profile_url, defaults={"followers_count": followers_count_numeric}
    )

    # If the profile already exists, update the followers_count
    if not created:
        inst_profile.followers_count = followers_count_numeric
        inst_profile.save()

    driver.quit()


from selenium.common.exceptions import TimeoutException
import time


@shared_task
def update_followers_count():
    # Fetch all InstProfile instances
    inst_profiles = InstProfile.objects.all()

    for inst_profile in inst_profiles:
        try:
            # Check if the profile link is not None
            if inst_profile.link:
                # Install ChromeDriver and get the path
                driver_path = install_chromedriver()

                # Set up the Chrome options
                chrome_options = ChromeOptions()
                chrome_options.add_argument(
                    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
                )
                print("Chrome Options:", chrome_options.arguments)

                # Create the Chrome WebDriver with the specified options
                driver = webdriver.Chrome(options=chrome_options)

                driver.get(inst_profile.link)

                # Let the page load
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "_acan"))
                )

                soup = BeautifulSoup(driver.page_source, "lxml")

                # Convert BeautifulSoup object to lxml etree
                root = html.fromstring(str(soup))

                # Use XPath to extract the followers count
                followers_count = root.xpath('//span[@class="_ac2a"]/@title')[0]

                # Extract the numeric part from the title
                followers_count_numeric = "".join(filter(str.isdigit, followers_count))

                # Save the new followers count in InstProfile
                inst_profile.followers_count = followers_count_numeric
                inst_profile.save()

                # Save the history in InstHistory
                InstHistory.objects.create(
                    profile=inst_profile,
                    followers_count=followers_count_numeric,
                    created_at=timezone.now(),
                )

                time.sleep(5)  # Adjust sleep time as needed
            else:
                print("Profile link is None.")
        except TimeoutException as te:
            print(f"TimeoutException: {te}")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            # Close the driver in the 'finally' block to ensure it's always closed
            driver.quit()
