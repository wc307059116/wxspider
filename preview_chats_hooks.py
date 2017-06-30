from wxpy import *
import logging
import os
import sys
import re

rootpath=os.path.dirname(os.getcwd())
print(rootpath)
syspath=sys.path
sys.path=[]
sys.path.append(rootpath)
sys.path.extend([rootpath+'\\'+i for i in os.listdir(rootpath) if i[0]!="."])
sys.path.extend(syspath)

from chedb.wxdb import dbforMysql
from chespider.tieba import *

logging.basicConfig(level=logging.DEBUG)

keyWord = ['爬虫','获取数据']
getAll = ['all','所有数据']

global bot

def new_friend(friend):
    global bot
    print('new friend: {}'.format(friend))
    print(bot.friends.update())


def new_group(group):
    print('new group: {}'.format(group))


def new_member(member):
    print('new member: {}, from {}'.format(member, member.group))


def deleting_friend(friend):
    global bot
    bot.friends.update()
    print('deleting friend: {}'.format(friend))
    print(bot.friends.update())


def deleting_group(group):
    print('deleting group: {}'.format(group))


def deleting_member(member):
    print('deleting member: {}, from {}'.format(member, member.group))


def start_bot():
    global bot
    bot = Bot('test.pkl', hooks=dict(
        new_friend=new_friend,
        new_group=new_group,
        new_member=new_member,
        deleting_friend=deleting_friend,
        deleting_group=deleting_group,
        deleting_member=deleting_member,
    ))

def sendFile(username,filenema):
    global msgBot
    searchFriend = bot.friends.search(username)[0]
    searchFriend.send_file(filenema)

def getName(strr,sub = '查询：'):
    #sub=re.compile(r''+sub,re.S)
    #result=sub.findall(strr)
    selRsl = re.search(sub,strr)
    if not selRsl :
        return False
    else :
        return True

def register_friend():
    global bot
    for friend in bot.friends:
        @bot.register(friend)
        def reply_myfriend(rcvMsg):
            if rcvMsg.type == 'TEXT': 
                if rcvMsg.text in keyWord:
                    return start_spider()
                elif rcvMsg.text in getAll:
                    db = dbforMysql()
                    result = db.select_all()
                    with open('所有信息.txt', 'a+') as f:
                        for comment in result:
                            f.write('标题： {} \t 链接：{} \t 发帖人：{} \t 发帖时间：{}  \n'.format(comment['title'], comment['link'], comment['author'], comment['time']))
                        f.close()
                    rcvMsg.reply_file('所有信息.txt')
                else :
                    if getName(rcvMsg.text) :
                        selData = rcvMsg.text.split(':')[-1]
                        db = dbforMysql()
                        result = db.select_db(selData)
                        return result
                    #rcvMsg.chat.send_file('所有信息.txt')
                    #print(rcvMsg.chat.name)
                    #rcvMsg.reply_image('1.jpg')
                    #sendFile(rcvMsg.chat.name,'所有信息.txt')
                return rcvMsg.text

if __name__ == '__main__':
    start_bot()
    register_friend()
    bot.join()
