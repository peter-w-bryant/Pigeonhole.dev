# Standard library imports
import json
import time
import os
import argparse
import importlib

# Selenium: Path to WebDriver
path_to_webdriver = os.path.join(os.getcwd(), 'chromedriver.exe')

# Selenium imports
from selenium import webdriver                                                  # Webdriver
from selenium.webdriver.common.by import By                                     # Find elements by
from selenium.webdriver.chrome.service import Service                           # Chrome service
from selenium.webdriver.support.ui import WebDriverWait                         # Wait for elements to load
from selenium.webdriver.support import expected_conditions as EC                # Expected conditions
from selenium.common.exceptions import TimeoutException, NoSuchElementException # Misc. exceptions

up_for_grabs_url = 'https://up-for-grabs.net/#/'

class UpForGrabsScrape:
    """
    Scrape up-for-grabs.net for projects
    """ 
    def __init__(self):
        self.service = Service(path_to_webdriver)
        self.service.start()
        self.options = webdriver.ChromeOptions()              # Create a new Chrome session

        # Ignore SSL certificate errors
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--ignore-ssl-errors')
        self.options.add_argument('--ignore-certificate-errors-spki-list')
        self.options.add_argument('log-level=3')

        self.driver = webdriver.Chrome(service=self.service, options=self.options) # Init Chrome driver
        self.target_json = os.path.join(os.getcwd(), 'repo_scrapers' ,'u4g.json')

    def __enter__(self):
        self.driver = webdriver.Chrome(service=self.service, options=self.options) # Init Chrome driver
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.driver.quit()
        self.service.stop()

    def get_projects(self):
        """
        Get all projects from up-for-grabs.net
        """
        projects = {}
        self.driver.get(up_for_grabs_url)
        time.sleep(2) # Wait for page to load
        try:
            idx = 1
            while True:
                project_xpath = f"//*[@id='projects-panel']/div[6]/div[{idx}]"
                title_xpath = f"{project_xpath}/div[1]/div/span/a"
                title = self.driver.find_element(By.XPATH, title_xpath).get_attribute('innerHTML')
                github_link_xpath = f"{project_xpath}/div[2]/div[1]/p/a"
                github_link = self.driver.find_element(By.XPATH, github_link_xpath).get_attribute('outerHTML')
                # Get href link
                github_link = github_link.split('href="')[1].split('"')[0]
                github_repo_base_url = github_link.split("/labels/")[0]
                idx += 1
                if "github.com" in github_link:
                    github_repo_base_url = github_link.split("/labels/")[0]
                    projects[title] = github_repo_base_url

        except NoSuchElementException:
            with open(self.target_json, 'w') as f:
                json.dump(projects, f, indent=4)
            return {"success": f"Added projects to {self.target_json}"}

        except Exception as e:
            print(e)
            return {"error": "Something went wrong"}
            
if __name__ == "__main__":
    with UpForGrabsScrape() as scraper:
        projects = scraper.get_projects()
        print(projects)