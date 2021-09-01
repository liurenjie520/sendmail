import requests
import parsel
import os
import concurrent.futures

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}

def send_requests(url):
    response = requests.get(url=url,headers=headers)
    return response

def parse_data(data):
    selector = parsel.Selector(data)
    return  selector

def get_img_url(select):
    url_list = select.xpath('//*[@id="post"]/div[4]/p/span/a/@href').getall()
    return url_list

def save_data(file_name,img,path):
    img = send_requests(img).content
    img_path = f"D:\妹子图\{file_name}\{path}"
    with open(img_path,'wb') as fp:
        fp.write(img)
        print(file_name,path,'保存成功')


def run(url):
    data = send_requests(url=url)
    select = parse_data(data.text)
    all_url = select.xpath('//*[@id="main"]/div/div/a/@href').getall()
    for url1 in all_url:
        data1 = send_requests(url1)
        data1.encoding = 'utf-8'
        sel = parse_data(data1.text)
        url_list = get_img_url(sel)
        file_name = sel.xpath('//*[@id="title"]/h1[1]/text()').get()
        if not os.path.exists(f'D:\妹子图\{file_name}'):
            os.mkdir(f'D:\妹子图\{file_name}')
        for img in url_list:
            path1 = img[-8:]
            save_data(file_name,img,path1)


if __name__ == '__main__':

    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        for page in range(1,10):
            url = f'http://www.xiuren.org/category/XiuRen-{page}.html'
            executor.submit(run, url)
