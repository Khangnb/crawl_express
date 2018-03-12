# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import json

client = MongoClient('localhost', 27017)
db = client.test

collection = db.express_page

def spider(max_pages):
    page = 1
    print page
    while page <= max_pages:
        url = 'https://vnexpress.net/tin-tuc/giao-duc/page/%s.html' % page
        #print url
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, from_encoding="utf-8")
        for link in soup.findAll('a', {'class': 'icon_commend'}):
            href = link.get('href')
            if 'video' in href:
                pass
            else:
                get_detail_page(href)
        page += 1

def get_detail_page(detail_page):
    url = detail_page
    data = {}
    title = ''
    list_content = []
    list_images = []
    list_comment = []
    #print url
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    #print url
    # get title news.
    for item in soup.findAll('section', {'class' : 'sidebar_1'}):
        title = item.find('h1', {'class','title_news_detail mb10'}).contents[0]
        images = item.findAll('img')
        for image in images:
            image = image['src']
            if image:
                list_images.append(image)
    # get content detail news
    for items in soup.findAll('p', {'class','Normal'}):
        content = items.string
        print content
        if content:
            list_content.append(content)
    # get comment
    for items in soup.findAll('div', {'class', 'comment_item width_common'}):
        full_content = items.find('p', {'class', 'full_content'}).string
        time_comment = items.find('span', {'class', 'left txt_666 txt_14'}).string
        user_name = items.b.string
        user_url = items.find('a', {'class', 'nickname txt_666'}).get('href')
        print full_content
        print time_comment
        print user_name
        print user_url

    data['url'] = url
    data['title'] = title
    data['list_content'] = list_content
    data['list_images'] = list_images
    data['list_comment'] = list_comment

    #print list_images
    print data
    #process_item(data)
    #print '------------end url ---------------'
    #get image if it have.
    #for tr in t.findAll('tr'):

file = open('scrawl.json', 'w')
def process_item(item):
    if item:
        line = json.dumps(dict(item)) + "\n"
        file.write(line)
        return item


spider(1)
