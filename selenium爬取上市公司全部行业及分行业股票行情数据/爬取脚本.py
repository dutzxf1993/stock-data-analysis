# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 08:05:26 2020

@author: zxf
"""

from selenium import webdriver
import xlsxwriter
import time
from selenium.webdriver.common.keys import Keys
import re
import csv

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

browser=webdriver.Chrome('D:/chromedriver')   
    
def get_total_page(url):            #获取某行业股票总页数
#     browser=webdriver.Chrome('D:/chromedriver')
#     browser.get(url)
    time.sleep(1)
    inputpage = browser.find_element_by_css_selector('#PageCont')
#     print(inputpage.text)
    pa = re.findall(r'\d+',inputpage.text)
    print(pa)
    if len(pa)==0:
#         browser.close()
        return 1
    elif len(pa)==5:
        try:
            nextclick = browser.find_element_by_css_selector('.next')
            nextclick.click()
            time.sleep(1)
            pa1 = re.findall(r'\d+',inputpage.text)
            print(pa1)
            return len(pa1)
        except Exception as e:
            print(e)
            return len(pa)
    else:
        return len(pa)
    
def get_url():                   #获取各行业股票列表网址
    url_dic = {}
    browser=webdriver.Chrome('D:/chromedriver')
    browser.get("http://quote.eastmoney.com/center/boardlist.html#industry_board")
    time.sleep(1)
    for i in range(1,5):
        inputpage = browser.find_element_by_css_selector('.paginate_input')
        inputpage.clear()
        inputpage.send_keys(str(i))
        inputclick = browser.find_element_by_css_selector('.paginte_go')
        inputclick.click()
        time.sleep(1)
        hangye = browser.find_element_by_css_selector('table#table_wrapper-table>tbody')
        tr_contents = hangye.find_elements_by_tag_name('tr')
        for tr in tr_contents:
            td = tr.find_elements_by_css_selector('td:nth-child(2)')
            for tdd in td:
                hre = tdd.find_elements_by_tag_name('a')
#                 print(tdd.text)
                for h in hre:
                    href = h.get_attribute('href')
#                     print(href)
                    url_dic[tdd.text] = href
#     print(url_dic)
    browser.close()
    return url_dic


def get_perpage_stock():            #获取每页股票具体数据
#     browser=webdriver.Chrome('D:/chromedriver')
#     browser.get(url)
    time.sleep(1)
    element = browser.find_element_by_css_selector('#dt_1')
    tr_contents = element.find_elements_by_tag_name('tr')
    dat = []
    for tr in tr_contents:
        lis = []
        for td in tr.find_elements_by_tag_name('td'):     
            lis.append(td.text) 
        dat.append(lis)    
    return dat 

def get_all_stock():
    for i,url in enumerate(dic.values()):
        url_tar = 'http://data.eastmoney.com/bkzj/'+url[-6:]+'.html'
        print(url_tar)
        dat =[]
        stock_data = []
        all_data = {}
        browser.get(url_tar)
        wait = WebDriverWait(browser,10,0.5)
        wait.until(EC.presence_of_element_located((By.ID,"dt_1")))
        total_page = get_total_page(url_tar)
        print('该行业股票总页数为{}'.format(total_page))
        if total_page==1:
            print('正在爬取{}行业股票数据'.format(list(dic.keys())[i]))
            time.sleep(3)
            d = get_perpage_stock()
            d = d[2:]
            print(d)
            all_data[list(dic.keys())[i]] = d 
#         browser.close()
            with open('E:/hangye/'+list(dic.keys())[i]+'.csv','w',newline='')as f:
              writer = csv.writer(f)
              writer.writerows(d)
        else:
            for page in range(1,total_page+1): 
                dat =[]
                time.sleep(1)                
                inpupage = browser.find_element_by_css_selector('#PageContgopage')
                inpupage.clear()
                inpupage.send_keys(page)
                inpuclick = browser.find_element_by_css_selector('.btn_link')
                inpuclick.click()   
                time.sleep(1)
                print('正在爬取{}股票第{}页数据'.format(list(dic.keys())[i],page))
                time.sleep(3)
                dat = get_perpage_stock() 
                dat = dat[2:]
                stock_data.extend(dat)
                print(stock_data)
            all_data[list(dic.keys())[i]] = stock_data 
            with open('E:/hangye/'+list(dic.keys())[i]+'.csv','w',newline='')as f:
                writer = csv.writer(f)
                writer.writerows(stock_data)
    return all_data


def clear_url():
    try:
        if not url_tar is null:
            del url_tar
    except Exception:
        pass


    
if __name__=='__main__':
    time_start = time.time()
    clear_url()
    all_data = {}
    dic = get_url()
    all_data = get_all_stock()
    time_end = time.time()
    print('爬取完成,总耗时{}'.format(time_end-time_start))
    print(all_data)
    
    
