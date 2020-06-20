# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020-04-09
# @Author  : mrdon
# @FileName: main.py
# @Software: PyCharm


import csv
import random
import re
import time

import requests
from fake_useragent import UserAgent
from lxml import etree


def get_url_list():
    url_list = []
    for i in list(range(242)):  # fill in the number manually
        url_list.append('http://www.dianping.com/shop/22024293/review_all/p' + str(i + 1))
    return url_list


def get_css_content(html, headers):
    print('------begin to get css content------')
    css_l = re.search(r'<link rel="stylesheet" type="text/css" href="(//s3plus.meituan.net.*?.css)">', html)
    css_link = 'http:' + css_l.group(1)
    html_css = requests.get(css_link, headers).text
    return html_css


def get_font_dic(css_content):
    print('------begin to get font dictionary------')
    svg_l = re.search(r'svgmtsi.*?(//s3plus.meituan.net.*?svg)\);', css_content)
    svg_link = 'http:' + svg_l.group(1)
    svg_html = requests.get(svg_link).text
    y_list = re.findall('d="M0 (.*?) H600"', svg_html)
    font_dic = {}
    j = 0
    font_size = int(re.findall(r'font-size:(.*?)px;fill:#333;}', svg_html)[0])
    for y_l in y_list:
        # font_l = re.findall('<text .*?>(.*?)<', svg_html)
        font_l = re.findall(r'<textPath xlink:href="#' + str(j + 1) + '" textLength=".*?">(.*?)</textPath>', svg_html)
        font_list = re.findall(r'.{1}', font_l[0])
        for x in range(len(font_list)):
            font_dic[str(x * font_size) + ',' + y_l] = font_list[x]
        j += 1
    return font_dic, y_list


def get_html_full_review(html, css_content, font_dic, y_list):
    font_key_list = re.findall(r'<svgmtsi class="(.*?)"></svgmtsi>', html)
    # print(len(font_key))
    for font_key in font_key_list:
        pos_key = re.findall(r'.' + font_key + '{background:-(.*?).0px -(.*?).0px;}', css_content)
        pos_x = pos_key[0][0]
        pos_y_original = pos_key[0][1]
        for y in y_list:
            if int(pos_y_original) < int(y):
                pos_y = y
                break
        html = html.replace('<svgmtsi class="' + font_key + '"></svgmtsi>', font_dic[pos_x + ',' + pos_y])
    return html


def reviews_output(html_text, html_full_review, flag):
    print('------start extracting the comments and writing it to the file------')

    html_full_review = re.sub('<img class="emoji-img".*?/>', '', html_full_review).strip()
    # print(pinglun_text)
    # print(html_full_review)
    html = etree.HTML(html_full_review)
    list = re.findall(r'<span class="sml-rank-stars sml-str(.*?) star"></span>', html_text)
    j = 0
    reviews_items = html.xpath("//div[@class='reviews-items']/ul/li")
    for i in reviews_items:
        r = []
        r = i.xpath("./div/div[@class='review-words Hide']/text()")
        if r:
            pass
        else:
            r = i.xpath("./div/div[@class='review-words']/text()")
        flag += 1
        print(str(int(list[j]) / 10) + '  ' + r[0].replace(' ', '').replace('\n', '').replace('\r', ''))
        with open('reivew.csv', 'a+', encoding='utf-8-sig', newline='') as myFile:
            myWriter = csv.writer(myFile)
            # myWriter.writerow(["review-rank", "review-words"])
            myWriter.writerow([int(list[j]) / 10, r[0].replace(' ', '').replace('\n', '').replace('\r', '')])
            j = j + 1
    print('------write complete, delay 10-25 seconds------')
    time.sleep(10 + 15 * random.random())


if __name__ == '__main__':
    url_list = get_url_list()
    flag = 0
    # url = 'http://www.dianping.com/shop/18335920/review_all/p1'
    headers = {
        'Cookie': 'fill in your cookie',
        'Upgrade-Insecure-Requests': '1',
        'host': 'www.dianping.com',
        'User-Agent': UserAgent().random,
        # 'Accept': 'application/json, text/javascript'
    }
    res = requests.get(url_list[0], headers=headers)
    # get css content
    css_content = get_css_content(res.text, headers)
    # get font dictionary
    font_dic, y_list = get_font_dic(css_content)
    # parse the first web page
    print('------start parse the first web page------')
    html_full_review = get_html_full_review(res.text, css_content, font_dic, y_list)
    reviews_output(res.text, html_full_review, flag)
    flag += 15
    # parse all pages starting from the second page
    for n in list(range(len(url_list) - 1)):
        print('------start parse the ' + str(n + 2) + ' web page------')
        res = requests.get(url_list[n + 1], headers=headers)
        if res:
            html_full_review = get_html_full_review(res.text, css_content, font_dic, y_list)
            reviews_output(res.text, html_full_review, flag)
            n += 1
            flag += 15
        else:
            print('unable to access web page')
