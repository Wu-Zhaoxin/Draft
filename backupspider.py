# -*- coding = utf-8 -*-
# @Time : 2022/2/28 17:35
# @Author : WZX
# @File : .py
# @Software : PyCharm

# 流程：
# a.在循环的第一页中urllib获取到html
# b.在获取到的一个页面中 BeautifulSoup筛选标签+re.findall正则提取（字符串类型）
# c.附加到空列表中保存数据

from bs4 import BeautifulSoup  # 页面解析 获取数据 拆分数据
import re  # 正则表达式 进行文字匹配
import urllib.request, urllib.error  # 指定URL 获取网页数据
import xlwt  # 进行excel操作
import sqlite3  # 进行SQLite数据库操作

findTitle = re.compile(r'<a class.*?>(.*?)</a>', re.S)  # 提取标题信息的正则表达式规则制定 re.S让换行符包含在字符中（忽略换行符影响）
# findLink = re.compile(r'<a href="(.*)" target="_blank">.*</a>')
findLink = re.compile(r'<a class.*?href="(.*?)".*?</a>')
findPrice = re.compile(r'<span class="fr las yj4">(.*)</span>')
findBrowse = re.compile(r'</i>(.*)</span>')


def main():
    baseurl = "https://www.cgmodel.com/model/rw_"  # 定义基础网址
    datalist = getData(baseurl)  # 调用
    # savepath = "爬取数据1.xls" #定义保存路径
    dbpath = "mobel1.db"

    # saveData(datalist,savepath) #调用
    saveData2DB(datalist, dbpath)


# 1.爬取网页
def getData(baseurl):
    datalist = []  # 将datalist定义为一个空的数据列表
    for i in range(2, 20):
        url = baseurl + str(i) + str("_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_1_0_0")
        print(url)
        html = askURL(url)

        # 2.解析数据（逐一）
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div', class_="case_onpo03"):  # 找到指定标签内容
            data = []  # 定义一个空列表数据
            item = str(item)  # 将获取的标签类型转为字符串
            item = item.replace("\t", "");  # 替换字符串中的\t为空

            Title = re.findall(findTitle, item)[0]  # 用re库：在生成的item文档中正则匹配查找Title 在item中查找
            data.append(Title)  # 给data列表添加数据

            Link = re.findall(findLink, item)
            Link = "".join(Link)
            # print(Link)
            # Link = Link.replace('"',"");
            Link = "https://www.cgmodel.com" + Link
            data.append(Link)

            Price = re.findall(findPrice, item)
            print(type(Price))
            Price = "".join(Price)
            print(type(Price))
            if len(Price) == 0:
                Price = "免费"
            data.append(Price)

            Browse = re.findall(findBrowse, item)  # 正则表达式生成列表
            Browse = ''.join(Browse)  # join（）：列表转为字符串
            Browse = Browse.split()  # 字符串按空格分割成列表后变为列表 效果：去除空格
            Browse = "".join(Browse)
            data.append(Browse)

            print(data)
            print("=============================================================")
            datalist.append(data)
    # print(datalist)
    return datalist


def askURL(url):  # 一个页面的获取
    head = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.56"
    }
    request = urllib.request.Request(url, headers=head)
    # html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:  # hasattr（e,"code“): 判断e这个对象里面是否包含code这个属性
        if hasattr(e, "code"):  # hasattr()函数用于判断对象是否包含对应属性
            print(e.code)
        if hasattr(e.reason):  # 报错原因
            print(e.reason)

    return html


# 3.保存数据
def saveData2DB(datalist, dbpath):
    print("save...")
    init_db(dbpath)
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()

    for data in datalist:
        for index in range(len(data)):
            if index == 3:
                continue
            data[index] = '"' + str(data[index]) + '"'  # sql语句字符需要加引号

        sql = '''
        insert into model1(Model,Link,Price,Browse)
        values(%s)''' % ",".join(data)
        print(sql)
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()


def init_db(dbpath):
    sql = '''
    create table model1
    (
    id integer primary key autoincrement,
    Model varchar,
    Link text,
    Price varchar,
    Browse numeric 

    )


        '''
    conn = sqlite3.connect(dbpath)  # 连接或创建数据库
    cursor = conn.cursor()  # 获取游标
    cursor.execute(sql)  # 执行sql语句
    conn.commit()  # 提交
    conn.close()

    # book = xlwt.Workbook(encoding="utf-8",style_compression=0) #创建文件 workbook对象
    # sheet = book.add_sheet('模型网',cell_overwrite_ok=True) #创建工作表单 是否覆盖原有信息Ture
    #
    # col = ("模型名称","链接","价格","浏览数") #列名称
    # for i in range(0,4):
    #     sheet.write(0,i,col[i]) #0-2赋值列名称 写入位置：（0，0）（0，1）（0，2）
    # for i in range(0,199):
    #     print("第%d条" %(i+1))
    #     data = datalist[i]
    #     for j in range(0,4):
    #         sheet.write(i+1,j,data[j]) #数据 （1，0）（1，1）（1，2）-（2，0）（2，1）（3，2）-...
    #
    # book.save(savepath)
    print("爬取完毕！")


if __name__ == "__main__":
    # 当程序执行时 调用函数
    main()