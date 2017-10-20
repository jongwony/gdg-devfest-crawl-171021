import time

from urllib.parse import urlunsplit, urlsplit, urlencode
from utils.webdrivers import Chrome
from utils.notify import TelegramBot
from utils.catch_exception import timeout_handle

from bs4 import BeautifulSoup


class Crawl:
    def __init__(self, delay=20, telegram_notify=False, gui=False):
        """
        [디버깅 및 상태 저장]
        web driver 추적: self.chrome.browser
        page source 추적: self.soup

        :param delay: timing
        :param telegram_notify: telegram bot 활성화 여부
        :param gui: headless 여부
        """
        self.delay = delay

        # Telegram bot
        self.telegram_bot = TelegramBot() if telegram_notify else None

        # Log file

        # launch web driver
        self.chrome = Chrome(gui)

        # default selenium timeout
        self.chrome.browser.set_page_load_timeout(30)

        # for debug stack
        self.soup = BeautifulSoup("", 'html.parser')

    def destroy_webdriver(self):
        """Explicit Destroy Chrome Driver"""
        self.chrome.close()

    def call_ajax(self, base_url, url, method, data):
        """
        selenium 에서 ajax javascript 요청

        :param base_url: ajax 요청을 위한 현재 페이지
        :param url: 수집할 url
        :param method: HTTP method
        :param data: HTTP method payload
        :return: page source string
        """
        # jquery script
        ajax_script = '''
        var done = arguments[0];
        jQuery.ajax({{
            accepts: '*/*',
            method: '{method}',
            url: '{url}',
            data: {data}
        }})
        .done(function(data, status, xhr) {{
            done(xhr.responseText)
        }})
        .fail(function(resp) {{
            done(resp.status)
        }})
        '''.format(url=url, method=method, data=data)

        # ajax root
        if self.chrome.browser.current_url != base_url:
            self.chrome.browser.get(base_url)

            # safe sleep
            time.sleep(5)
            self.chrome.browser.implicitly_wait(self.delay)

        # async must be set timeout
        self.chrome.browser.set_script_timeout(self.delay)
        self.chrome.browser.stop_client()

        # return BeautifulSoup string object
        html = self.chrome.browser.execute_async_script(ajax_script)
        self.soup = BeautifulSoup(html, 'html.parser')
        return html

    @timeout_handle
    def fetch(self, url, method='GET', ajax=False, payload=None, base_url=None):
        """
        raw page 데이터를 크롤링

        :param url: 수집할 url
        :param method: HTTP method (ajax True)
        :param ajax: 비동기 ajax 요청 여부
        :param payload: POST 및 ajax 요청을 위한 data (dictionary)
        :param base_url: ajax 요청을 위한 현재 페이지
        :return: page source string
        """
        if ajax:
            assert payload is not None
            return self.call_ajax(base_url, url, method, payload)
        else:
            if method == 'GET' and payload is not None:
                scheme, netloc, path, query, fragment = urlsplit(url)
                self.chrome.browser.get(urlunsplit((scheme, netloc, path, urlencode(payload), fragment)))
            else:
                self.chrome.browser.get(url)

            time.sleep(self.delay)
            self.chrome.browser.implicitly_wait(self.delay)

            html = self.chrome.browser.page_source
            self.soup = BeautifulSoup(html, 'html.parser')
            return html
