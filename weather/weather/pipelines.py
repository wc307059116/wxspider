# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import requests
import json
import codecs
import pymysql.cursors

class WeatherPipeline(object):
    def process_item(self, item, spider):
        base_dir = os.getcwd()
        fiename = base_dir + '\\weather.txt'
        
        with open(fiename, 'a') as f:
             f.write(item['date'] + '\n')
             f.write(item['week'] + '\n')
             f.write(item['temperature'] + '\n')
             f.write(item['weather'] + '\n')
             f.write(item['wind'] + '\n\n')
        f.close()
        #with open(base_dir + '\\data\\' + item['date'] + '.png', 'wb') as f:
            #f.write(requests.get(item['img']).content)  
        #f.close()

        return item

class W2json(object):
    def process_item(self, item, spider):
        base_dir = os.getcwd()
        filename = base_dir + '\\weather.json'
        with codecs.open(filename, 'a') as f:
            line = json.dumps(dict(item), ensure_ascii=False) + '\n'
            f.write(line)
        f.close()
        return item

class W2mysql(object):
    def process_item(self,item,spider):
        config = {
                    'host':'127.0.0.1',
                    'port':3306,
                    'user':'root',
                    'password':'!@#$%^',
                    'db':'test',
                    'charset':'utf8mb4',
                    'cursorclass':pymysql.cursors.DictCursor,
                 }
        dbCon = pymysql.connect(**config)
        try:
            with dbCon.cursor() as cursor:
                #cursor.execute('TRUNCATE TABLE WEATHERS')
                sql = """INSERT INTO WEATHERS(date,week,temperature,weather,wind)
                        VALUES (%s, %s,%s,%s,%s)"""
                cursor.execute(sql, (item['date'],item['week'],item['temperature'],item['weather'],item['wind']))
            dbCon.commit()

        finally:
            dbCon.close()