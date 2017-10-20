import os


def get_path(*argv):
    """
    루트 경로를 포함시키면 초기화됩니다.

    >>> get_path('/data') -> '/data'
    >>> get_path('data') -> 'script_path/data'   # Absolute path
    >>> get_path() -> 'script_path'              # Absolute path
    """
    script_path = os.path.realpath(os.path.dirname(os.path.dirname(__file__)))
    return os.path.join(script_path, *argv)
