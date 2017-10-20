from functools import wraps

from selenium.common.exceptions import TimeoutException


def timeout_handle(func):
    """
    string 을 반환하는 클래스 내부 메서드에 사용
    웹 페이지 소스 텍스트 대신 TIMEOUT ERROR 라는 텍스트를 반환합니다.
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except TimeoutException:
            return 'TIMEOUT ERROR'
    return wrapper


def context_manager(func):
    """
    Example class 내부의 transaction 메서드에 사용
    가장 상위 데코레이터로 사용
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        finally:
            # 웹 드라이버 파괴
            self.crawl.destroy_webdriver()

            # 에러 컬럼 업데이트
            self.update_error()

            # Database 종료
            self.mysql.connector.close()
    return wrapper
