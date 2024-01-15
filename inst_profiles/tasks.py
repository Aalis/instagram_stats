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


@shared_task
def celery_task(profile_url):
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
