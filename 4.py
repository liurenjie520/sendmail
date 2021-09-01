# -*- coding: utf-8 -*-
import requests
import traceback
import sys
headers = {
'User - Agent': 'Mozilla / 5.0(Windows NT 10.0;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 86.0.4240.198Safari / 537.36'
}
 
def post_data(name, data):
    """
    调用Qmsg酱 发送消息~~
    :param name:
    :param data:
    :return:
    """
    QmsgKEY = "？？？？？"  # 申请地址https://qmsg.zendee.cn/me.html#/login
    try:
        qmsg_url = 'https://qmsg.zendee.cn/send/%s' % QmsgKEY
        res = requests.post(qmsg_url, data=data).json()
        print("当前模块名： %s" % name, res['reason'])
    except:
        print('调用Qmsg酱出错，代码为：')
        traceback.print_exc()
 
 
def morning(time):
    """
    早安/晚安的话~~~
    :return:
    """
    try:
        url = 'http://api.tianapi.com/txapi/%san/index?key=%s' % (time, key)  # 申请地址https://www.tianapi.com/apiview/142和https://www.tianapi.com/apiview/143
        res = requests.get(url).json()
        content = res['newslist'][0]['content']
        if time == "zao":
            greetings = "早上好呀，老公大人"
        elif time == "wan":
            greetings = "晚安了哦，老公大人"
        data = {
            'msg': "%s@face=49@@face=109@\n%s@face=175@" % (greetings, content)
        }
        post_data("早安/晚安心语", data)
    except:
        print('早安/晚安心语出错，代码为：')
        traceback.print_exc()
 
 
def weather(code):
    """
    每日的天气模块
    :param code:
    :return:
    """
    try:
        url = 'http://t.weather.itboy.net/api/weather/city/%d' % code
        res = requests.get(url, headers=headers).json()
 
        city = res['cityInfo']['city']  # 地区
        forecast = res['data']['forecast']  # 具体天气
        quality = res['data']['quality']
        pm25 = res['data']['pm25']
        pm10 = res['data']['pm10']
        ganmao = res['data']['ganmao']  # ganmao: "各类人群可自由活动"
        shidu = res['data']['shidu']
        wendu = res['data']['wendu'] + '℃'
 
        def poem(type_we):
            """
            天气诗句~~
            :param type_we:
            :return:
            """
            try:
                for type_line in list(type_we):  # 1=风、2=云、3=雨、4=雪、5=霜、6=露 、7=雾、8=雷、9=晴、10=阴
                    tqtype = 9
                    if type_line == '风':
                        tqtype = 1
                        break
                    elif type_line == '云':
                        tqtype = 2
                        break
                    elif type_line == '雨':
                        tqtype = 3
                        break
                    elif type_line == '雪':
                        tqtype = 4
                        break
                    elif type_line == '霜':
                        tqtype = 5
                        break
                    elif type_line == '露':
                        tqtype = 6
                        break
                    elif type_line == '雾':
                        tqtype = 7
                        break
                    elif type_line == '雷':
                        tqtype = 8
                        break
                    elif type_line == '晴':
                        tqtype = 9
                        break
                    elif type_line == '阴':
                        tqtype = 10
                        break
                url = "http://api.tianapi.com/txapi/tianqishiju/index?key=%s&tqtype=%d" % (key, tqtype)  # 申请地址https://www.tianapi.com/apiview/91
                res = requests.get(url).json()
                content = res['newslist'][0]['content']
                author = res['newslist'][0]['author']
                source = res['newslist'][0]['source']
            except:
                content = "东边日出西边雨，道是无晴却有晴"  # 万一请求失败，就随便来一句防止下面报错（、、、、）
                author = "刘禹锡"
                source = "竹枝词"
                print('天气诗句出错，代码为：')
                traceback.print_exc()
            return content, author, source
 
        for lmaki_data, lmaki in zip(forecast, ['今天', '明天']):  # 这你可以加个后天，来多请求几次。最多好像有10次？
            ymd = lmaki_data['ymd']  # 时间
            week = lmaki_data['week']  # 星期几
            sunrise = lmaki_data['sunrise']  # 日出
            sunset = lmaki_data['sunset']  # 日落
            high = lmaki_data['high']  # 最高温
            low = lmaki_data['low']  # 最低温
            fx = lmaki_data['fx']  # 风向
            fl = lmaki_data['fl']  # 几级风
            type_we = lmaki_data['type']  # 天气
            notice = lmaki_data['notice']  # 提示语
            content, author, source = poem(type_we)
            data = {
                'msg': f'@face=6@{lmaki}是{week},天气是 {type_we} 哦,温度为{wendu},湿度为{shidu}\npm2.5的值为{pm25},pm1.0的值是{pm10},{ganmao}\n'
                       f'{high}，{low},{notice}。\n{content}--{author}\n吹的是{fx}，风速达到了{fl}了。\n太阳将在 {sunrise} 升起，{sunset} 落下\n'
                       f'天气质量为 {quality}@face=13@   {ymd}   {city}'
            }
            post_data("天气", data)
    except:
        print('天气出错，代码为：')
        traceback.print_exc()
 
 
def earthy():
    """
    土味情话
    :return:
    """
    try:
        url = "http://api.tianapi.com/txapi/saylove/index?key=%s" % key  # 申请地址 https://www.tianapi.com/apiview/80
        rqs = requests.get(url).json()
        content = rqs["newslist"][0]["content"]
        data = {
            'msg': "%s\n@face=6@@face=6@@face=6@@face=6@" % content
        }
        post_data("土味情话", data)
    except:
        print('土味情话出错，代码为：')
        traceback.print_exc()
 
 
def zhen():
    """
    英语一句话
    :return:
    """
    try:
        url = "http://api.tianapi.com/txapi/ensentence/index?key=%s" % key  # 申请地址https://www.tianapi.com/apiview/62
        res = requests.get(url).json()
        content_zh = res['newslist'][0]['zh']
        content_en = res['newslist'][0]['en']
        data = {
            'msg': "%s@face=21@\n%s" % (content_en, content_zh)
        }
        post_data("英语一句话", data)
    except:
        print('英语一句话出错，代码为：')
        traceback.print_exc()
 
 
def poems():
    """
    古代情诗
    :return:
    """
    try:
        url = "http://api.tianapi.com/txapi/qingshi/index?key=%s" % key  # 申请地址https://www.tianapi.com/apiview/106
        res = requests.get(url).json()
        content = res['newslist'][0]['content']
        author = res['newslist'][0]['author']
        source = res['newslist'][0]['source']
 
        co = len(content.encode('utf-8')) - len(author.encode('utf-8')) - len(source.encode('utf-8'))
        data = {
            'msg': "%s@face=179@\n%s--%s《%s》" % (content, " " * co, author, source)
        }
        post_data("古代情诗", data)
    except:
        print('古代情诗出错，代码为：')
        traceback.print_exc()
 
 
def main():
    """
    主程序
    :return:
    """
    morning('wan')      # 这里改成zao就是早安，改成wan就是晚安
    earthy()
    weather(101210805)  # 改为你的城市代码
    zhen()
    poems()
 
 
if __name__ == '__main__':
    key = "？？？"  # 自己申请https://www.tianapi.com/，和上面的key通用，每天免费100次的调用，基本用不完
    main()
   
   -------------------------------------------------------
   
   
   
 def main(event,context):
    """
    主程序
    :return:
    """
    try:
        Tname=event["TriggerName"]     # 获取[color=rgba(0, 0, 0, 0.9)]触发器的名字
        if Tname=="zaoS" or Tname=="zaoF":      
            morning('zao')
            if Tname=="zaoS":            # 家和学校隔很远，在家就调用家那的天气，在学校就用学校那地的天气，可自己删
                weather(101210805)           # 城市代码
            elif Tname=="zaoF":
                weather(101210701)
        elif Tname=="wan":
            morning('wan')
        elif Tname=="twqh":
            earthy()
            zhen()
    except:
        print("直接调用测试")
        morning('wan')
        weather(101210805)
        earthy()
        zhen()
   
   

