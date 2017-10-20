import platform

from utils.pathenv import get_path

from selenium import webdriver
from pyvirtualdisplay import Display


class Chrome:
    def __init__(self, gui=False):
        self.gui = gui

        driver_path = get_path('driver', platform.system(), 'chromedriver')
        chrome_options = webdriver.ChromeOptions()

        # [Option Lists] http://www.assertselenium.com/java/list-of-chrome-driver-command-line-arguments
        chrome_options.add_argument('--dns-prefetch-disable')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')

        # Install Xvfb
        if not self.gui:
            self.display = Display(visible=0, size=(800, 600))
            self.display.start()
            chrome_options.add_argument('--headless')

        self.browser = webdriver.Chrome(driver_path, chrome_options=chrome_options)

    def close(self):
        if self.browser.get_cookies():
            self.browser.delete_all_cookies()

        self.browser.quit()

        if not self.gui:
            self.display.stop()
