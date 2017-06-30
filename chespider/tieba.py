import requests,time
from bs4 import BeautifulSoup
import os
import sys

#添加python包搜索路径
rootpath=os.path.dirname(os.getcwd())
print(rootpath)
syspath=sys.path
sys.path=[]
sys.path.append(rootpath)
sys.path.extend([rootpath+'\\'+i for i in os.listdir(rootpath) if i[0]!="."])
sys.path.extend(syspath)

from chedb.wxdb import dbforMysql


base_url = 'https://tieba.baidu.com/f?kw=切尔西&ie=utf-8'
deep =3 

def get_html(url):
    try:
        r=requests.get(url)
        r.raise_for_status()
        r.encoding='utf-8'
        return r.text
    except:
        return "error"

def get_content(url):
    comments=[]
    html = get_html(url)
    soup = BeautifulSoup(html,'lxml')
    liTags = soup.find_all('li', attrs={'class': ' j_thread_list clearfix'})
    for li in liTags:
        comment = {}
        try:
            comment['title'] = li.find(
                'a', attrs={'class': 'j_th_tit '}).text.strip()
            comment['link'] = "http://tieba.baidu.com/" + \
                li.find('a', attrs={'class': 'j_th_tit '})['href']
            comment['name'] = li.find(
                'span', attrs={'class': 'tb_icon_author'}).text.strip()
            comment['time'] = li.find(
                'span', attrs={'class': 'pull-right is_show_create_time'}).text.strip()
            comment['replyNum'] = li.find(
                'span', attrs={'class': 'threadlist_rep_num center_text'}).text.strip()
            comment['lastReplyname'] = li.find(
                'span', attrs={'class': 'tb_icon_author_rely j_replyer'}).text.strip()
            comment['lastReplytime'] = li.find(
                'span', attrs={'class': 'threadlist_reply_date pull_right j_reply_data'}).text.strip()
            comments.append(comment)
        except:
            print('error')
    return comments

def run_spider(base_url, deep):
    urlList = []
    for i in range(0, deep):
        urlList.append(base_url + '&pn=' + str(50 * i))
    print('所有的网页已经下载到本地！ 开始筛选信息。。。。')
    
    db = dbforMysql()
    db.clear_db()
    for url in urlList:
        content = get_content(url)
        db.insert_db(content)    
    print('所有的信息都已经保存完毕！')
    return '所有的信息都已经保存完毕！'
    #db.select_db('time = \'15\:05\'')
    
def start_spider():
    return run_spider(base_url, deep)

if __name__ == '__main__':
    run_spider(base_url, deep)