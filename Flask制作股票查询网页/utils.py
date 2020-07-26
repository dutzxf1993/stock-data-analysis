import time
import pymysql
import urllib.request
import pandas as pd
import requests
import re
from bs4 import BeautifulSoup



def get_time():
    time_str = time.strftime("%Y{}%m{}%d{} %X")
    return time_str.format("年", "月", "日")


def get_conn():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='199395', db='stock', charset='utf8')
    cursor = conn.cursor()
    return conn,cursor


def close_conn(conn,cursor):
    cursor.close()
    conn.close()


def query(sql,*args):
    conn,cursor = get_conn()
    cursor.execute(sql,args)
    res = cursor.fetchall()
    close_conn(conn,cursor)
    return res


# def get_be_data(*args):
#     sql = "SELECT * FROM hangqing where stockid = %s"
#     res = query(sql, args)
#     print(res)
#     return res[0]
def get_be_data(code):
    url = 'http://qt.gtimg.cn/q=sh' + str(code)
    content = urllib.request.urlopen(url, timeout=2).read()
    content = content.decode("gbk").encode("utf-8").decode("utf8", "ignore")
    content = content.split('~')
    return content


def get_history_data(code):
    url = 'http://quotes.money.163.com/service/chddata.html?code=0'+str(code)
    try:
        content = urllib.request.urlopen(url).read()
        content = content.decode("gbk").encode("utf-8")
        with open('E:/hisdata.csv', 'wb')as f:
            f.write(content)
        data = pd.read_csv('E:/hisdata.csv')
        # data = data.to_dict('record')
        data = data[["日期","开盘价","收盘价","最低价","最高价"]]
        # print(data)
        data = data.to_dict()
        data['日期'] = list(data['日期'].values())
        data['开盘价'] = list(data['开盘价'].values())
        data['收盘价'] = list(data['收盘价'].values())
        data['最低价'] = list(data['最低价'].values())
        data['最高价'] = list(data['最高价'].values())
        data['日期'] = data['日期'][::-1]
        data['开盘价'] = data['开盘价'][::-1]
        data['收盘价'] = data['收盘价'][::-1]
        data['最低价'] = data['最低价'][::-1]
        data['最高价'] = data['最高价'][::-1]
    except Exception as e:
        print(e)
    return data


def get_guping(id):
    max_page = 2  # input('请输入爬取页数')
    b = []
    # head = {'User-Agent':' Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}

    for page in range(1, int(max_page) + 1):
        url = 'http://guba.eastmoney.com/list,{}_{}.html'.format(id, page)
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        urllist = soup.find_all('div', {'class': 'articleh'})
        for i in urllist:
            if i.find('a') != None:
                try:
                    title = i.find('a').get_text()
                    yuedu = i.find('span',{'class':'l1 a1'}).get_text()
                    # time = i.find('span', {'class': 'l5 a5'}).get_text()
                    # a = [title + yuedu]
                    b.append(title + yuedu)
                except Exception as e:
                    print(e)
                    pass
    return b[7:]


if __name__ == '__main__':
    msg = get_guping(600002)
    print(msg)
