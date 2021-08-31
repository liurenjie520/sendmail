import requests
from urllib.parse import urlencode

import os
import time

param = 'cos'

def get_page(url, page):
    """一个函数，两个功能，取决于page"""
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36'
                      ' (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'
    }
    r = requests.get(url=url, headers=headers)

    if r.status_code == 200:

        #将返回的信息转换为字典
        r = r.json()

        #分析无限套娃的列表字典，提取出一页的doc_id
        if page == 'home':
            print("开始采集doc_id...")
            doc_ids = []
            items = r['data']['items']
            for article in items:
                item = article['item']
                doc_ids.append(item['doc_id'])
            return doc_ids

        #获取每篇文章返回的字典
        elif page == 'article':
            print("开始采集图片信息...")
            return r


def get_article(doc_ids):
    """根据doc_ids列表构造url，获取每篇文章返回的信息"""
    for doc_id in doc_ids:
        url = 'https://api.vc.bilibili.com/link_draw/v1/doc/detail?doc_id=' + \
              str(doc_id)
        article = get_page(url, page='article')
        time.sleep(1)
        save_images(article)


def save_images(article):
    """根据文章标签创建文件夹，把相同标签的图片存在一个文件夹里"""
    tags = article['data']['item']['tags']
    tag = tags[-1]['tag']
    title = article['data']['item']['title']
    title = title.replace(':', '')

    if not os.path.exists(tag):
        os.mkdir(tag)

    pictures = article['data']['item']['pictures']
    i = 1
    for p in pictures:
        img_src = p['img_src']
        try:
            r = requests.get(img_src)
            if r.status_code == 200:
                title2 = title + str(i)
                i += 1
                file_path = '{0}/{1}.{2}'.format(tag, title2, 'jpg')
                if not os.path.exists(file_path):
                    with open(file_path, 'wb') as f:
                        f.write(r.content)
                        print("成功保存" + file_path)
                else:
                    print("已存在" + file_path)
        except requests.ConnectionError:
            print("保存图片失败")

def main():
    category = input('搜集cos还是sifu图片:')
    page = input('搜集前几页:')

    page_num = 0
    while True:

        #根据输入拼接url
        params = {
            'category':category,
            'type':'hot',
            'page_num':page_num,
            'page_size':20
        }
        base_url = 'https://api.vc.bilibili.com/link_draw/v2/Photo/list?'
        url = base_url + urlencode(params)

        print('正在搜索第%d页'%page_num)
        doc_ids = get_page(url, page='home')
        get_article(doc_ids)
        if page_num == page:
            break
        else:
            page_num += 1

if __name__ == '__main__':
    main()
