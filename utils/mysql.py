try:
    from _config import mysql_info
except ImportError:
    from config_template import mysql_info

import pymysql
import sqlalchemy
from pymysql.err import InternalError


class MySQL:
    """pymysql placeholder %s"""
    def __init__(self):
        self.connector = pymysql.connect(**mysql_info)

        # pandas.to_sql
        self.engine = sqlalchemy.create_engine('mysql+pymysql://', creator=self.connector)

        self.url_stack = None

        with self.connector.cursor() as cursor:
            try:
                cursor.execute('''CREATE TABLE page_list ( url TEXT, status TEXT ) CHARACTER SET utf8 COLLATE utf8_general_ci''')
            except InternalError:
                print('table `page_list` already exists!')

            try:
                cursor.execute('''CREATE TABLE raw_html ( url TEXT, html LONGTEXT ) CHARACTER SET utf8 COLLATE utf8_general_ci''')
            except InternalError:
                print('table `raw_html` already_exists!')

    def upload_page_lists(self, url_list):
        with self.connector.cursor() as cursor:
            cursor.executemany('''INSERT INTO page_list(url) VALUES (%s)''', url_list)
            self.connector.commit()

    def select_one_for_update(self):
        with self.connector.cursor() as cursor:
            cursor.execute('''SELECT url FROM page_list WHERE status!='OK' OR status IS NULL LIMIT 1 FOR UPDATE''')
            url = cursor.fetchone()
            if url:
                cursor.execute('''UPDATE page_list SET status='pending' WHERE url=%s''', url)
            self.connector.commit()

        self.url_stack = url

        # tuple format
        if url:
            url = url[0]

        return url

    def update_ok(self, url):
        with self.connector.cursor() as cursor:
            cursor.execute('''UPDATE page_list SET status='OK' WHERE url=%s''', (url,))
            self.connector.commit()

    def update_error(self):
        if self.url_stack is not None:
            with self.connector.cursor() as cursor:
                cursor.execute('''UPDATE page_list SET status='error' WHERE url=%s''', self.url_stack)
                self.connector.commit()

    def upload_html(self, url, html):
        with self.connector.cursor() as cursor:
            cursor.execute('''INSERT INTO raw_html VALUES(%(url)s, %(html)s)''', {'url': url, 'html': html})
            self.connector.commit()

        self.update_ok(url)
