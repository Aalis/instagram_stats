import unittest
from unittest.mock import patch, MagicMock, Mock
from inst_profiles.tasks import (
    update_followers_count,
    get_followers_count,
    ChromeDriverManager,
)


class TestChromeDriverManager(unittest.TestCase):
    @patch("inst_profiles.tasks.webdriver.Chrome")
    @patch("inst_profiles.tasks.install_chromedriver")
    def test_enter_method_initializes_chrome_driver(
        self, mock_install_chromedriver, mock_webdriver
    ):
        """
        Test the __enter__ method of ChromeDriverManager initializes Chrome driver.
        """
        mock_webdriver_instance = Mock()
        mock_webdriver.return_value = mock_webdriver_instance

        with ChromeDriverManager() as manager_instance:
            # Your actual test logic can go here

            # Make sure to call initialize_chrome_driver before asserting
            manager_instance.initialize_chrome_driver()

            self.assertIsNotNone(manager_instance.chrome_driver)


class TestUpdateFollowersCount(unittest.TestCase):
    @patch("inst_profiles.tasks.ChromeDriverManager.initialize_chrome_driver")
    @patch("inst_profiles.tasks.ChromeDriverManager.login_to_instagram")
    def test_update_followers_count(self, mock_login, mock_initialize):
        # Debug information
        print("Before update_followers_count")

        # Run the method
        update_followers_count()

        # Debug information
        print("After update_followers_count")

        # Assertions
        mock_initialize.assert_called_once()
        mock_login.assert_called_once()


class TestGetFollowersCount(unittest.TestCase):
    @patch("inst_profiles.tasks.ChromeDriverManager.initialize_chrome_driver")
    @patch("inst_profiles.tasks.ChromeDriverManager.login_to_instagram")
    @patch("inst_profiles.tasks.WebDriverWait")
    def test_get_followers_count(self, mock_wait, mock_login, mock_initialize):
        # Set up mocks
        mock_chrome_driver = Mock()
        mock_initialize.return_value = mock_chrome_driver

        # Set up page source content
        page_source_content = "<html><span class='_ac2a' title='Followers: 123'>Followers: 123</span></html>"
        mock_chrome_driver.page_source = page_source_content

        # Call the method with a mock profile URL
        profile_url = "http://example.com/profile"
        get_followers_count(profile_url)

        # Assertions
        mock_initialize.assert_called_once()
        mock_login.assert_called_once()
        mock_chrome_driver.get.assert_called_once_with(profile_url)
        mock_wait.assert_called_once_with(mock_chrome_driver, 10)
        self.assertEqual(mock_chrome_driver.page_source, page_source_content)
        # Add more assertions based on your specific logic


if __name__ == "__main__":
    unittest.main()
