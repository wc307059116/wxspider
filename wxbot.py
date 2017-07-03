from wxpy import *
import logging
import os
import sys
import re

rootpath=os.getcwd()
syspath=sys.path
sys.path=[]
sys.path.append(rootpath)
sys.path.extend([rootpath+'\\'+i for i in os.listdir(rootpath) if i[0]!="."])
sys.path.extend(syspath)
print(sys.path)

from chedb.wxdb import dbforMysql
from chespider.tieba import get_detail,start_spider

logging.basicConfig(level=logging.DEBUG)
getAll = ['all','所有数据']
global bot

def new_message(core, msg):
    print('- {}: new message: {}, latency: {:.2f}'.format(core, msg, msg.latency))

def new_friend(core, friend):
    print('- {}: new friend: {}'.format(core, friend))

def new_group(core, group):
    print('- {}: new group: {}'.format(core, group))

def new_member(core, member):
    print('- {}: new member: {}, from {}'.format(core, member, member.group))

def deleting_friend(core, friend):
    print('- {}: deleting friend: {}'.format(core, friend))

def deleting_group(core, group):
    print('- {}: deleting group: {}'.format(core, group))

def deleting_member(core, member):
    print('- {}: deleting member: {}, from {}'.format(core, member, member.group))

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
    selRsl = re.search(sub,strr)
    if not selRsl :
        return False
    else :
        return True

def getDetail(strr,sub = '详细：'):
    selRsl = re.search(sub,strr)
    if not selRsl :
        return False
    else :
        return True

def getTieba(strr,sub = '爬取：'):
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
                if getTieba(rcvMsg.text):
                    tarName = rcvMsg.text.split(':')[-1]
                    return start_spider(tarName)
                elif rcvMsg.text in getAll:
                    db = dbforMysql()
                    result = db.select_all()
                    with open('info.txt', 'w') as f:
                        for comment in result:
                            f.write('标题： {} \t 链接：{} \t 发帖人：{} \t 发帖时间：{}  \n'.format(comment['title'], comment['link'], comment['author'], comment['time']))
                        f.close()
                    rcvMsg.reply_file('info.txt')
                    os.remove('info.txt')
                elif getName(rcvMsg.text) :
                    selData = rcvMsg.text.split(':')[-1]
                    db = dbforMysql()
                    result = db.select_db(selData)
                    return result
                elif getDetail(rcvMsg.text):
                    detailUrl = rcvMsg.text.split(':')[-1]
                    rslText,rslImg = get_detail(detailUrl)
                    rcvMsg.reply(rslText)
                    if len(rslImg):
                        for imgName in rslImg:
                            rcvMsg.reply_image(imgName)
                            os.remove(imgName)
                else:
                    return rcvMsg.text

if __name__ == '__main__':
    start_bot()
    register_friend()
    bot.join()
