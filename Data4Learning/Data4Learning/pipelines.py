# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymysql
from pymysql.cursors import DictCursor
from scrapy.exceptions import NotConfigured

class MySQLPipeline:
    @classmethod
    def from_crawler(cls, crawler):
        db_settings = crawler.settings.getdict("MYSQL_SETTINGS")
        if not db_settings:
            raise NotConfigured("MySQL settings not found")
        return cls(**db_settings)

    def __init__(self, host, port, user, password, db, charset='utf8mb4'):
        self.conn_params = {
            'host': host, 'port': port,
            'user': user, 'password': password,
            'db': db, 'charset': charset,
            'cursorclass': DictCursor, 'autocommit': True
        }

    def open_spider(self, spider):
        self.db = pymysql.connect(**self.conn_params)
        self.cursor = self.db.cursor()

    def close_spider(self, spider):
        self.cursor.close()
        self.db.close()

    def process_item(self, item, spider):
        table = f"{spider.name}_articles"
        keys = ', '.join(item.keys())
        cols = ', '.join(f"%({k})s" for k in item.keys())
        sql = f"INSERT INTO `{table}` ({keys}) VALUES ({cols})"
        self.cursor.execute(sql, dict(item))
        return item
