import json
from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
from requests import get, post
import random
import http.client, urllib
import os


today = datetime.now()
print(today)
week_list = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
year  = datetime.now().year
month = datetime.now().month
day   = datetime.now().day
today1 = datetime.date(datetime(year=year, month=month, day=day))
print(today)
week = week_list[today.isoweekday() % 7]
print(week)
start_date = '2020-12-28'
province = '江苏'
city = '苏州'
birthday1 = '05-22'
birthday2 = '11-30'
app_id = "wx93ec76c537d9b640"
app_secret = "42449570663daf7a28e4168b48e04604"

user1_id = "onnQy51zuXw2-UP5r1G5ucIS6yHU"
user2_id = "onnQy5xz9wZQRK_T7FYDmihtuNnk"
template_id = "nlRa5EClwwBgSi_Ac2Acnzp_1ZfOpJ-qQSK_IXxj4Qs"


def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  print(res)
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp']), math.floor(weather['low'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday(birthday):
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)

#词霸每日一句
def get_ciba():

        url = "http://open.iciba.com/dsapi/"
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
        }
        r = get(url, headers=headers)
        note_en = r.json()["content"]
        note_ch = r.json()["note"]
        return note_ch, note_en


# 励志名言
def lizhi():

        conn = http.client.HTTPSConnection('api.tianapi.com')  # 接口域名
        params = urllib.parse.urlencode({'key': 'c7e0a561f3ed3818a25889218162fde3'})
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        conn.request('POST', '/lzmy/index', params, headers)
        res = conn.getresponse()
        data = res.read()
        data = json.loads(data)
        return data["newslist"][0]["saying"]



client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)

wea, temperature1, temperature2 = get_weather()
love_days=get_count()
# 获取词霸每日金句
note_ch, note_en = get_ciba()

data = {

    "date": {
      "value": "{} {}".format(today1, week),
      "color": get_random_color()
    },
    "city": {
      "value": city,
      "color": get_random_color()
    },
    "weather": {
      "value": wea,
      "color": get_random_color()
    },
    "min_temperature": {
      "value": temperature2,
      "color": get_random_color()
    },
    "max_temperature": {
      "value": temperature1,
      "color": get_random_color()
    },
    "love_day": {
      "value": love_days,
      "color": get_random_color()
    },

    # "note_en": {
    #   "value": note_en,
    #   "color": get_random_color()
    # },
    # "note_ch": {
    #   "value": note_ch,
    #   "color": get_random_color()
    # },


     "birthday1": {
      "value": get_birthday(birthday1),
      "color": get_random_color()
     },
     "birthday2": {
      "value": get_birthday(birthday2),
      "color": get_random_color()
     },

    "lizhi": {
      "value": get_words(),
      "color": get_random_color()
    },

    # "pop": {
    #   "value": pop,
    #   "color": get_random_color()
    # },
    #
    # "health": {
    #   "value": health_tip,
    #   "color": get_random_color()
    # },
    #
    # "tips": {
    #   "value": tips,
    #   "color": get_random_color()
    # }

}
res = wm.send_template(user1_id, template_id, data)
print(res)
res = wm.send_template(user2_id, template_id, data)
print(res)
