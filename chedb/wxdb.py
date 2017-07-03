import pymysql.cursors
import time

class dbforMysql(object):
    def __init__(self):
        self.config = {
                    'host':'127.0.0.1',
                    'port':3306,
                    'user':'root',
                    'password':'!@#$%^',
                    'db':'test',
                    'charset':'utf8mb4',
                    'cursorclass':pymysql.cursors.DictCursor,
                    }

    def  con_db(self):
        self.dbCon = pymysql.connect(**self.config)

    def insert_db(self,comments):
        self.con_db()
        try:
            with self.dbCon.cursor() as cursor:
                sql = 'INSERT INTO CHE (title,author,link,time) VALUES(%s,%s,%s,%s)'
                for comment in comments:
                    try:
                        time.strptime(comment['time'],"%H:%M")
                        cursor.execute(sql, (comment['title'],comment['name'],comment['link'], comment['time']));
                    except:
                        continue
            self.dbCon.commit()
        finally:
            self.dbCon.close()

    def clear_db(self):
        self.con_db()
        try :
            with self.dbCon.cursor() as cursor:
                sql = 'TRUNCATE TABLE CHE'
                cursor.execute(sql)
            self.dbCon.commit()
        finally :
            self.dbCon.close()
    
    def select_db(self,data):
        self.con_db()      
        try :
            with self.dbCon.cursor() as cursor:
                sql = 'SELECT * FROM CHE WHERE '+data
                cursor.execute(sql)
                result = cursor.fetchone()
            print(result)
            self.dbCon.commit()
            return result
        except:
            return '查询不到数据'
        finally :
            self.dbCon.close()

    def select_all(self):
        self.con_db()
        try :
            with self.dbCon.cursor() as cursor:
                sql = 'SELECT * FROM CHE '
                cursor.execute(sql)
                result = cursor.fetchall()
            self.dbCon.commit()
            return result
        finally :
            self.dbCon.close()

    def select_weather(self):
        self.con_db()
        try :
            with self.dbCon.cursor() as cursor:
                sql = 'SELECT * FROM WEATHERS '
                cursor.execute(sql)
                result = cursor.fetchall()
            self.dbCon.commit()
            return result
        finally :
            self.dbCon.close()
            
    def clear_weather(self):
        self.con_db()
        try :
            with self.dbCon.cursor() as cursor:
                sql = 'TRUNCATE TABLE WEATHERS'
                cursor.execute(sql)
            self.dbCon.commit()
        finally :
            self.dbCon.close()