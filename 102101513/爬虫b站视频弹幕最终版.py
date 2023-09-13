import requests             # 发出请求
import re                   # 内置库 用于匹配正则表达式
import csv                  # 文件格式
import jieba                # 中文分词
import wordcloud            # 绘制词云
import json
import time
import warnings
import PIL.Image as image
import numpy as np
import pandas as pd
import os
from matplotlib import pyplot as plt


os.environ['NO_PROXY'] = 'bilibili.com'
# 忽略warning警告
warnings.filterwarnings("ignore")


def get_bvid(page, pos):
    # 通过搜索api“https://api.bilibili.com/x/web-interface/search/all/v2?page=1-15&keyword=”获取前300个视频的bvid
    _url = 'https://api.bilibili.com/x/web-interface/search/all/v2?page='+str(page+1)+'&keyword=日本核污染水排海'
    _headers = {
        # 个人浏览器的信息
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.69',
        'cookie': "buvid3=5CD968B6-5E6F-AA6C-D8BB-422744C1DB0054109infoc; b_nut=1673696354; _uuid=1092729F9-10FE3-DB8C-64A2-F27261E3B43153165infoc; buvid4=82DFB562-AF5C-F20C-AC96-E71C089E97E355884-023011419-hBTxrxbr8pWyUVDiIX7ZVw%3D%3D; CURRENT_FNVAL=4048; rpdid=|(u)luk|llRR0J'uY~RkuJ|Ju; buvid_fp_plain=undefined; i-wanna-go-back=-1; nostalgia_conf=-1; b_ut=5; header_theme_version=CLOSE; LIVE_BUVID=AUTO6216768194613696; home_feed_column=4; CURRENT_PID=8e025d90-cb08-11ed-8e36-15f3cf3099af; CURRENT_QUALITY=80; browser_resolution=1392-786; FEED_LIVE_VERSION=V_SEO_FIRST_CARD; fingerprint=efbe80e589d57838b8ff20cb5df98e9d; buvid_fp=a1198a46c9f71d42436ace10a9ab7448; bili_jct=416c2ad96c39091affdb9092e9a593d9; DedeUserID=414937912; DedeUserID__ckMd5=a09ace8891a7091a; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTQwODgxODUsImlhdCI6MTY5MzgyODk4NSwicGx0IjotMX0.pEBW75b3VX6p2lqx7jPuUpPvrAHz0QIoHtagLMp3_iU; bili_ticket_expires=1694088185; bp_video_offset_1480857975=837478778313637938; bp_video_offset_414937912=838225299482083363; sid=6udo3o89; PVID=3; b_lsid=B11E5210A_18A6ABF8D38"}
    res = requests.get(url=_url, headers=_headers,verify=False).text
    json_dict = json.loads(res)
    # print(json_dict)
    return json_dict["data"]["result"][11]["data"][pos]['bvid'] #返回视频的bvid信息


def get_cid(bvid):           # 获取b站视频的cid
    url1 = "https://api.bilibili.com/x/player/pagelist?bvid="+str(bvid)+"&jsonp=jsonp"
    response = requests.get(url1).text
    dirt = json.loads(response)
    cid = dirt['data'][0]['cid']        # 找到视频的cid
    return cid


def get_danmu(cid):                      # 获取弹幕
    url = 'https://api.bilibili.com/x/v1/dm/list.so?oid=' + str(cid)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.69"
    }                                   # 需要给出计算机浏览器用户客户端的信息，否则容易访问网站失败
    response = requests.get(url, headers=headers)
    html_doc = response.content.decode('utf-8')
    # 正则表达式的匹配模式
    res = re.compile('<d.*?>(.*?)</d>')
    # 根据模式提取网页数据
    danmu = re.findall(res, html_doc)
    for i in danmu:                     # 打印弹幕信息到相应的excel表格中
        with open('b站弹幕.csv', 'a', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            danmu = []
            danmu.append(i)
            writer.writerow(danmu)      # 写入excel表格


#绘制云图
def get_wordcloud():
    f = open('b站弹幕.csv', encoding='utf-8')
    txt = f.read()
    # print(txt_list)
    txt_list = jieba.lcut(txt)
    # print(string)
    string = ' '.join(txt_list)
    mask_image = "china.png"
    # 导入中国地图，使得词云生成的图片在轮廓中
    mask = np.array(image.open(mask_image))
    # 词云的参数设置
    w = wordcloud.WordCloud(
                            mask=mask,
                            width=1000,
                            height=700,
                            background_color='white',
                            font_path='C:/Windows/SIMLI.TTF',
                            # scale=15,
                            # stopwords={' '},
                            # contour_width=5,
                            # contour_color='red'
                            )

    w.generate(string)
    # 打印词云图片
    w.to_file('wordcloud.png')


def print_danmu():
        plt.rc('font', family='SimHei', size=13)
        # 读取 xlsx 文件，从第一行开始读取数据
        all_danmu = pd.read_csv('b站弹幕.csv', header=None, encoding='utf-8')
        # 统计每个弹幕出现的次数
        counter = all_danmu.stack().value_counts()
        # 转换为DataFrame并重置索引
        top_20 = counter.head(20).reset_index()
        top_20.columns = ['弹幕', '出现次数']
        print(top_20)
        # 按出现次数升序排序
        top_20 = top_20.sort_values(by='出现次数', ascending=True)
        # 设置图表样式和布局
        plt.style.use('ggplot')
        plt.figure(figsize=(15, 10))
        # 绘制水平条形图，提供xy轴的坐标信息
        plt.barh(top_20['弹幕'], top_20['出现次数'], color='red')
        plt.xlabel('出现次数')
        plt.ylabel('弹幕')
        plt.title('Top 20 弹幕统计')
        plt.show()
        # 统计弹幕出现次数并存入danmu_arrangement.csv中
        counter.to_csv('danmu_arrangement.csv')

def main():
    for i in range(1):
        for j in range(1):                 # 因为bilibili的api搜索页面一页有20个视频的信息，所以内循环设置为20，外循环设置为15
            get_danmu(get_cid(get_bvid(i,j)))  # 获取搜索记录前300个视频的弹幕
        time.sleep(1)
    print_danmu()
    get_wordcloud()
main()
