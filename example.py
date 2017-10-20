import os
import argparse

from utils.transaction import Crawl
from utils.aws import Resource
from utils.mysql import MySQL
from utils.catch_exception import *

from selenium.common.exceptions import NoSuchElementException


def selenium_test():
    # sleep 3초(delay=3), no headless(gui=True)
    crawl = Crawl(delay=3, gui=True)

    # python 을 검색한 google 페이지
    crawl.fetch('https://www.google.co.kr/search?q=python')

    # <a> 태그를 가진 Selenium Web Element 들의 객체 리스트
    a_tags_elements = crawl.chrome.browser.find_elements_by_css_selector('#rso div.rc h3.r a')

    # <a> 태그 추출
    a_tags = [a.get_attribute('href') for a in a_tags_elements]
    for link in a_tags:
        crawl.fetch(link)

    # 웹 드라이버 파괴
    crawl.destroy_webdriver()


class MainExample:
    def __init__(self):
        # Selenium headless
        self.crawl = Crawl(delay=20, telegram_notify=False, gui=True)
        self.aws = Resource()
        self.mysql = MySQL()

    @context_manager
    def transaction(self, keyword, control_instances):
        # Base page, 생략된 결과를 포함하여 검색
        self.crawl.fetch('https://www.google.co.kr/search?q={}&filter=0'.format(keyword))

        # 페이지 탐색
        self.navigate_page(5)

        # AWS 'Auxiliary' 인스턴스 실행
        self.aws.ec2_on_off(control_instances)

    def navigate_page(self, max_page):
        # paginate pattern
        # nav > tbody > tr > td.cur > span
        # nav > tbody > tr > td:nth-child([next]) > a > span
        cur_page = None
        for _ in range(max_page):
            # <a> 태그를 가진 Selenium Web Element 들의 객체 리스트
            a_tags_elements = self.crawl.chrome.browser.find_elements_by_css_selector('#rso div.rc h3.r a')

            # <a> 태그 추출
            a_tags = [a.get_attribute('href') for a in a_tags_elements]

            # 현재 페이지 데이터베이스 저장
            self.mysql.upload_page_lists(a_tags)

            # 현재 페이지 찾기
            paginate = self.crawl.chrome.browser.find_elements_by_css_selector('#nav > tbody > tr > td')
            for i, e in enumerate(paginate):
                if e.get_attribute('class') == 'cur':
                    cur_page = i
                    break

            # 다음 페이지 없음
            try:
                next_element = paginate[cur_page + 1].find_element_by_css_selector('a')
                next_page = next_element.get_attribute('href')
            except NoSuchElementException:
                break

            # 다음 페이지 요청
            self.crawl.fetch(next_page)


class AuxExample:
    def __init__(self):
        # Selenium headless
        self.crawl = Crawl(delay=20, telegram_notify=False, gui=False)
        self.mysql = MySQL()

    @context_manager
    def transaction(self):
        while True:
            # 데이터베이스에서 URL 가져오기
            url = self.mysql.select_one_for_update()
            if not url:
                break

            # 해당 URL 요청
            html = self.crawl.fetch(url)

            # raw_html 테이블에 업로드
            self.mysql.upload_html(url, html)

        # 정상적으로 완료된 경우 자동으로 인스턴스 종료
        os.system('poweroff')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--query')
    parser.add_argument('--instance_name')
    parser.add_argument('--aux', action='store_true')
    args = parser.parse_args()

    if args.aux:
        example = AuxExample()
        example.transaction()
    else:
        if args.query is not None:
            example = MainExample()

            # 검색어 변경 가능
            example.transaction(args.query, args.instance_name)
        else:
            print('Required Search Keyword!')
