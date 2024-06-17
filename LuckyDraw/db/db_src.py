# coding:utf-8
# @Author:AZ5394
# GitHub:github.com/AZ5394
import sqlite3


class Sqlite:

    def __init__(self):
        # record database
        self.record_conn = sqlite3.connect('db/record/records.db')
        self.record_cursor = self.record_conn.cursor()
        self.record_cursor.execute("CREATE TABLE IF NOT EXISTS extract_record("
                                   "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                                   "record_time TEXT,"
                                   " record TEXT)")
        self.name_conn = sqlite3.connect('db/name/names.db')
        self.name_cursor = self.name_conn.cursor()
        self.name_cursor.execute("CREATE TABLE IF NOT EXISTS names(name TEXT)")
        # self.record_cursor.execute("CREATE TABLE IF NOT EXISTS extract_record("
        #                            "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        #                            "local_time NUMERIC DEFAULT (strftime('%Y-%m-%d %H:%M:%f', datetime('now'))),"
        #                            "record TEXT)")
        self.record_cursor.close()
        self.record_conn.close()
        self.name_cursor.close()
        self.name_conn.close()

    # 名字数据库
    def name_data(self):
        self.name_conn = sqlite3.connect('db/name/names.db')
        self.name_cursor = self.name_conn.cursor()
        self.name_cursor.execute("SELECT name FROM names")
        self.all_name = [name[0] for name in self.name_cursor.fetchall()]
        return self.all_name

    def add_name(self, names):  # 添加名字到数据库
        names = names.split()
        self.name_conn = sqlite3.connect('db/name/names.db')
        self.name_cursor = self.name_conn.cursor()
        if len(names) > 1:
            for name in names:
                self.name_cursor.execute(f"INSERT INTO names VALUES('{name}')")
                self.name_conn.commit()
        else:
            self.name_cursor.execute(f"INSERT INTO names VALUES('{names[0]}')")
            self.name_conn.commit()
        self.name_cursor.close()
        self.name_conn.close()

    def delete_name(self, name):  # 从数据库中删除名字
        self.name_conn = sqlite3.connect('db/name/names.db')
        self.name_cursor = self.name_conn.cursor()
        self.name_cursor.execute(f"DELETE FROM names WHERE name='{name}'")
        self.name_conn.commit()
        self.name_cursor.close()
        self.name_conn.close()

    # 记录数据库
    def add_record(self, record, record_time):  # 添加记录到数据库
        self.record_conn = sqlite3.connect('db/record/records.db')
        self.record_cursor = self.record_conn.cursor()
        self.record_cursor.execute(
            f"INSERT INTO extract_record(record_time, record) VALUES('{record_time}','{record}')")
        self.record_conn.commit()
        self.record_cursor.close()
        self.record_conn.close()

    def clear_name(self):  # 清空名字数据库
        ...

    def clear_record_table(self):  # 清空记录数据库
        self.record_conn = sqlite3.connect('db/record/records.db')
        self.record_cursor = self.record_conn.cursor()
        self.record_cursor.execute("DROP TABLE extract_record")
        self.record_conn.commit()
        self.record_cursor.close()
        self.record_conn.close()

    def last_column(self):
        self.record_conn = sqlite3.connect('db/record/records.db')
        self.record_cursor = self.record_conn.cursor()
        self.record_cursor.execute("SELECT id FROM extract_record ORDER BY id DESC LIMIT 1")
        last_column = self.record_cursor.fetchone()
        self.record_cursor.close()
        self.record_conn.close()
        return last_column[0] if last_column else 0

    def query(self, num):
        self.record_conn = sqlite3.connect('db/record/records.db')
        self.record_cursor = self.record_conn.cursor()
        self.record_cursor.execute(f"SELECT * FROM extract_record WHERE id='{num}'")
        self.data = self.record_cursor.fetchall()
        self.record_cursor.close()
        self.record_conn.close()
        return self.data
