# -*- coding = utf-8 -*-
# @Time : 2022/3/2 9:39
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

def main():

    oneurl = "http://36.112.130.153:7777/manage/meta/api/metadatas/records"  # 定义基础网址
    all,keys = askURL(oneurl) #all,keys由ask（oneurl）函数获得

    dbpath = "satelites1.db"
    saveSatelites(all,keys,dbpath)


def askURL(oneurl):  # 一个页面的获取
    head = {
'Accept': 'application/json, text/plain, */*',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9',
'access-agent': 'pc-dss',
'Connection': 'keep-alive',
'Content - Length': '268',
'Content-Type': 'application/json;charset=UTF-8',
'Host': '36.112.130.153:7777',
'ipaddr': '',
'murmur': '289106b88ea4b703911ac36ec2aa669c',
'Origin': 'http://36.112.130.153:7777',
'Referer': 'http://36.112.130.153:7777/',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
    }
    page = 0
    while True:
        page += 1
        payload = {

        "page": page, "size": 1000, "geom": ["POINT(109 40)"], "scenetime": ["2021-12-23", "2022-03-02"],
         "satelliteSensor": ["ZY302_MUX", "GF2_PMS", "GF1_PMS", "GF1_WFV"], "prodlevel": "1", "cloudpsd": 100,
         "dwxtype": "gx", "userType": 0, "userId": "218.56.38.236", "crossed": 'false', "desc": ["scenetime"]}

    #初级页面url：访问方法1和2的区别？为什么方法一访问失败？
    #==========================================================================
    #访问方法1
    # data = bytes(urllib.parse.urlencode(payload),encoding="utf-8")
    # print(1)
    # req = urllib.request.Request(url=url,data=data,headers=head,method="POST")
    # print(2)
    # response = urllib.request.urlopen(req)
    # print(3)
    # print(response.read().decode("utf-8"))
    #==========================================================================
    #访问方法2
        print("开始访问",page)
        res = requests.post(oneurl, data=json.dumps(payload), headers=head)
        dic = res.json()
        # print(dic)
    #==========================================================================
        result = dic['result']
        if len(result) == 0:
            print("访问结束")
            break
        idlist = []
        for i in result:
            idlist.append(i['id'])
        print(idlist)
     # return idlist

#获得次级页面url
# def getData(idlist,baseurl):
    baseurl = "http://36.112.130.153:7777/manage/meta/api/metadatas/record?"
    all = []
    keys = []
    i = 0
    for oneid in idlist:
        i+=1
        oneitem = []
        url = baseurl + str("id=") + oneid
        # print(url)
        try:
            results = urllib.request.urlopen(url).read()
            json1 = json.loads(results) #转为json格式
        except:
            print('超时')

        # req1 = requests.get(url, headers=head, timeout=4)
        # dic1 = req1.json()
        #提取json信息
        result = json1['result'][0] #提取json中相应键的值 并选取result中的第一个元素

        other = result['other'] #提取相应键的值
        base = result['base']
        system = result['system']

        new = {**other, **base,**system} #将三个字典合并

        value = new.values() #打印字典中所有的值形成dict_values类型
        value = list(value) #dict_values类型转为列表
        # print(value)
        # print(type(value))
        all.append(value)
        print("第%s条" %i)
    key = new.keys()
    key = list(key)
    keys.append(key)
    # print(all)
    # print(type(all))
    return all,keys
def saveSatelites(all,keys,dbpath):
    print("save...")
    init_db(dbpath)
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()

    for data1 in all:
        for index in range(len(data1)):
            # if index == 3:
            #     continue
            data1[index] = '"' + str(data1[index]) + '"'  # sql语句字符需要加引号
            # print(data1)

#insert into satelitetable(产品中间行时间,产品结束行时间,产品起始行时间,卫星,右上角纬度,右上角经度,右下角纬度,右下角经度,左上角纬度,左上角经度,左下角纬度,左下角经度,接收站,星下点,景path,景row,景中心纬度,景中心经度,轨道圈号,载荷,采集时间,geom,卫星平台平均俯仰角,卫星平台平均航偏角,卫星平台滚动角,卫星方位角,卫星高度角,增益模式,太阳方位角,太阳高度角天顶角,相机侧视角,相机前后视角,积分时间,积分级数,dem数据来源,云覆盖量,产品分辨率,产品大小,产品宽度,产品序列号,产品格式,产品类型,产品级别,产品谱段,产品谱段数,产品高度,原始数据条带号,地图投影,地球模型,投影带号,景序列号,椭球模型,浮动比例,生产日期,辐射校正方法,连续景数,重采样方法)

        sql = '''
        insert into satelitetable(%s)
        values(%s)''' % (",".join(keys),",".join(data1))
        try:
            cur.execute(sql)
            conn.commit()
        except sqlite3.OperationalError:
            print("此条失败")
        else:
            print("内容写入文件成功")
        print(sql)

    cur.close()
    conn.close()



def init_db(dbpath):
    sql = '''
    create table satelitetable
    (
    id integer primary key autoincrement,
产品中间行时间 varchar,
产品结束行时间 varchar,
产品起始行时间 varchar,
卫星 varchar,
右上角纬度 varchar,
右上角经度 varchar,
右下角纬度 varchar,
右下角经度 varchar,
左上角纬度 varchar,
左上角经度 varchar,
左下角纬度 varchar,
左下角经度 varchar,
接收站 varchar,
星下点 varchar,
景path varchar,
景row varchar,
景中心纬度 varchar,
景中心经度 varchar,
轨道圈号 varchar,
载荷 varchar,
采集时间 varchar,
geom varchar,
卫星平台平均俯仰角 varchar,
卫星平台平均航偏角 varchar,
卫星平台滚动角 varchar,
卫星方位角 varchar,
卫星高度角 varchar,
增益模式 varchar,
太阳方位角 varchar,
太阳高度角天顶角 varchar,
相机侧视角 varchar,
相机前后视角 varchar,
积分时间 varchar,
积分级数 varchar,
dem数据来源 varchar,
云覆盖量 varchar,
产品分辨率 varchar,
产品大小 varchar,
产品宽度 varchar,
产品序列号 varchar,
产品格式 varchar,
产品类型 varchar,
产品级别 varchar,
产品谱段 varchar,
产品谱段数 varchar,
产品高度 varchar,
原始数据条带号 varchar,
地图投影 varchar,
地球模型 varchar,
投影带号 varchar,
景序列号 varchar,
椭球模型 varchar,
浮动比例 varchar,
生产日期 varchar,
辐射校正方法 varchar,
连续景数 varchar,
重采样方法 varchar
    )
'''
    conn = sqlite3.connect(dbpath)  # 连接或创建数据库
    cursor = conn.cursor()  # 获取游标
    cursor.execute(sql)  # 执行sql语句
    conn.commit()  # 提交
    conn.close()


if __name__ == "__main__":
    # 当程序执行时 调用函数
    main()
print("爬取完毕！")