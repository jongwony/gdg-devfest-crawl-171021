try:
    from _config import mysql_info
except ImportError:
    from config_template import mysql_info

import pymysql
import sqlalchemy


class MySQL:
    def __init__(self):
        self.connector = pymysql.connect(**mysql_info)

        # pandas.to_sql
        self.engine = sqlalchemy.create_engine('mysql+pymysql://', creator=self.connector)

    def __del__(self):
        self.connector.close()

    def query(self, query, schema=None):
        """Recommend SQL Alchemy"""
        with self.connector.cursor() as cursor:
            cursor.execute(query(schema), schema)
