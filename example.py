from utils.transaction import Crawl
from utils.aws import Resource

from selenium.common.exceptions import NoSuchElementException


def selenium_test():
    # sleep 3초(delay=3), no headless(gui=True)
    crawl = Crawl(delay=3, gui=True)

    # python 을 검색한 google 페이지
    crawl.fetch('https://www.google.co.kr/search?q=python')

    # <a> 태그를 모두 추출한 Selenium Web Element 들의 객체 리스트
    a_tags = crawl.chrome.browser.find_elements_by_css_selector('#rso div.rc h3.r a')

    # <a> 태그를 타고 들어간 페이지
    depth1 = [a.get_attribute('href') for a in a_tags]
    for link in depth1:
        crawl.fetch(link)

    # 웹 드라이버 파괴
    crawl.destroy_webdriver()


class MainExample:
    def __init__(self):
        # Selenium headless
        self.crawl = Crawl(delay=20, telegram_notify=False, gui=True)
        self.aws = Resource()

    def transaction(self, keyword):
        # Base page, 생략된 결과를 포함하여 검색
        self.crawl.fetch('https://www.google.co.kr/search?q={}&filter=0'.format(keyword))

        # 페이지 탐색
        self.navigate_page(0)

        # <a> 태그 추출
        # 데이터베이스에서 fetch, parsing, upload

        # AWS 'Auxiliary' 인스턴스 실행
        self.aws.ec2_on_off('Auxiliary')

        # 웹 드라이버 파괴
        self.crawl.destroy_webdriver()

    def navigate_page(self, max_page):
        # paginate pattern
        # nav > tbody > tr > td.cur > span
        # nav > tbody > tr > td:nth-child([next]) > a > span
        cur_page = None
        for _ in range(max_page):
            # 현재 페이지 데이터베이스 저장

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

            self.crawl.fetch(next_page)


class AuxExample:
    def __init__(self):
        # Selenium headless
        self.crawl = Crawl(delay=20, telegram_notify=False, gui=False)

    def transaction(self):
        # 데이터베이스에서 URL 가져오기
        url = None

        self.crawl.fetch(url)

        # raw_html 테이블에 업로드

        # 웹 드라이버 파괴
        self.crawl.destroy_webdriver()

        # 인스턴스 종료


if __name__ == '__main__':
    example = MainExample()

    # 검색어 변경 가능
    example.transaction('python')

