# -*- coding = utf-8 -*-
# @Time : 2022/3/3 14:13
# @Author : WZX
# @File : .py
# @Software : PyCharm



from bs4 import BeautifulSoup #页面解析 获取数据 拆分数据
import re #正则表达式 进行文字匹配
import urllib.request,urllib.error #指定URL 获取网页数据
import xlwt #进行excel操作
import sqlite3 #进行SQLite数据库操作
import json
import requests
import requests, bs4

def main():

    oneurl = "http://catalog.chinasuperview.com:6677/SYYG/productSearchKQ.do"  # 定义基础网址
    askURL(oneurl) #all,keys由ask（oneurl）函数获得


def askURL(oneurl):  # 一个页面的获取
    head = {
'Accept': 'application/json, text/javascript, */*; q=0.01',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
'Cache - Control': 'max - age = 0',
'Cookie': 'JSESSIONID=96322981E40050663FF80A798AEDC59E',
'access-agent': 'pc-dss',
'Connection': 'keep-alive',
'Content - Length': '328',
'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
'Host': 'catalog.chinasuperview.com:6677',
'ipaddr': '',
'murmur': '289106b88ea4b703911ac36ec2aa669c',
'Origin': 'http://catalog.chinasuperview.com:6677',
'Referer': 'http://catalog.chinasuperview.com:6677/SYYG/product.do',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
    }

    payload = {
        'sate': 'GJ1D', 'wheresql': "1=1 and ISRELEASE = 'TRUE' and cloudpercent <=100 and SCENEDATE >= 20180101 and SCENEDATE <= 20220303 order by SCENEDATE desc , CENTERLONGITUDE desc", 'polygonKuangnew': "[[109,40],[109.1,40],[109.1,40.1],[109,40.1],[109,40]]", 'maxcloudCoverage': 100, 'level': 1
    }

    #初级页面url：访问方法1和2的区别？为什么方法一访问失败？
    #==========================================================================
    #访问方法1
    # data = bytes(urllib.parse.urlencode(payload),encoding="utf-8")
    # print(1)
    # req = urllib.request.Request(url=oneurl,data=data,headers=head,method="POST")
    # print(2)
    # response = urllib.request.urlopen(req)
    # print(3)
    # print(response.read())
    #==========================================================================
    # 访问方法2
    # print("开始访问")
    res = requests.post(oneurl, data=payload, headers=head) #request不需要编码解码
    # print(res.content)
    dic = res.json()
    print(dic)
    # print(res.text)

    # html = bs4.BeautifulSoup(res.text, 'lxml')
    # htmls = html.content
    # print(html)



if __name__ == "__main__":
    # 当程序执行时 调用函数
    main()
print("爬取完毕！")