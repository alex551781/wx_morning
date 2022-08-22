from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = '2020-12-28'
province = '江苏'
city = '苏州'
birthday = '05-22'

app_id = "wx93ec76c537d9b640"
app_secret = "42449570663daf7a28e4168b48e04604"

user1_id = "onnQy51zuXw2-UP5r1G5ucIS6yHU"
user2_id = "onnQy5xz9wZQRK_T7FYDmihtuNnk"
template_id = "P22mZGpn2lODSqow1CUhyrg7iplLgnpqapheirOh_Uo"


def get_weather(province, city):
  # 城市id
  try:
    city_id = cityinfo.cityInfo[province][city]["AREAID"]
  except KeyError:
    print("推送消息失败，请检查省份或城市是否正确")
    os.system("pause")
    sys.exit(1)
  # city_id = 101280101
  # 毫秒级时间戳
  t = (int(round(time() * 1000)))
  headers = {
    "Referer": "http://www.weather.com.cn/weather1d/{}.shtml".format(city_id),
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
  }
  url = "http://d1.weather.com.cn/dingzhi/{}.html?_={}".format(city_id, t)
  response = get(url, headers=headers)
  response.encoding = "utf-8"
  response_data = response.text.split(";")[0].split("=")[-1]
  response_json = eval(response_data)
  # print(response_json)
  weatherinfo = response_json["weatherinfo"]
  # 天气
  weather = weatherinfo["weather"]
  # 最高气温
  temp = weatherinfo["temp"]
  # 最低气温
  tempn = weatherinfo["tempn"]
  return weather, temp, tempn

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
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


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
weather, max_temperature, min_temperature = get_weather(province, city)
data = {"weather":{"value":wea},"max_temperature":{"value":max_temperature},"min_temperature":{"value":min_temperature},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user1_id, template_id, data)
print(res)
res = wm.send_template(user2_id, template_id, data)
print(res)
