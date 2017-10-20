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
