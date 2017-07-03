import requests,time
from bs4 import BeautifulSoup
import os
import sys
import  requests 

#添加python包搜索路径
rootpath=os.path.dirname(os.getcwd())
print(rootpath)
syspath=sys.path
sys.path=[]
sys.path.append(rootpath)
sys.path.extend([rootpath+'\\'+i for i in os.listdir(rootpath) if i[0]!="."])
sys.path.extend(syspath)

from chedb.wxdb import dbforMysql


#base_url = 'https://tieba.baidu.com/f?kw=切尔西&ie=utf-8'
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

def get_detail(url):
    comments=[]
    html = get_html('http:'+url)
    soup = BeautifulSoup(html,'lxml')
    liTags = soup.find('div',attrs={'class': 'd_post_content j_d_post_content '})
    urlText = liTags.text.strip()
    imgUrls = liTags.find_all('img')
    tmpFile = 0
    imgFile = []
    for imgUrl in imgUrls:
        print(imgUrl["src"])
        imgTmp = requests.get(imgUrl["src"])
        fileName = str(tmpFile)+'.jpg'
        with open(fileName,'ab') as tmp:
            tmp.write(imgTmp.content)
            tmp.close()
            imgFile.append(fileName)
    return urlText,imgFile


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
    
def start_spider(tagName):
    base_url = 'https://tieba.baidu.com/f?kw={}&ie=utf-8'.format(tagName)
    return run_spider(base_url, deep)

if __name__ == '__main__':
    get_detail('//tieba.baidu.com/p/5195292884')
    #run_spider(base_url, deep)