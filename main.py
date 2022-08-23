from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random
import http.client, urllib

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
city2 = os.environ['CITY2']
birthday = os.environ['BIRTHDAY']
birthday2 = os.environ['BIRTHDAY2']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
user_id2 = os.environ["USER_ID2"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['low']), math.floor(weather['high']), weather['date'], weather['airQuality']

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_birthday2():
  next = datetime.strptime(str(date.today().year) + "-" + birthday2, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def lucky():
  conn = http.client.HTTPSConnection('api.tianapi.com')
  params = urllib.parse.urlencode({'key':'ef4370c0fbe5eed37c23c7ba6e48e948','astro':'pisces'})
  headers = {'Content-type':'application/x-www-form-urlencoded'}
  conn.request('POST','/star/index',params,headers)
  res = conn.getresponse()
  data = res.read()
  data = json.loads(data)
  data = "速配星座："+str(data["newslist"][7]["content"])+"\n爱情指数："+str(data["newslist"][1]["content"])+"   工作指数："+str(data["newslist"][2]["content"])+"\n今日概述："+str(data["newslist"][8]["content"])
  return data      
      
def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, low ,high ,jintian ,airQuality = get_weather()
data = {"jintian":{"value":jintian, "color":get_random_color()},
        "city":{"value":city, "color":get_random_color()},
        "weather":{"value":wea, "color":get_random_color()},
        "low":{"value":low, "color":get_random_color()},
        "high":{"value":high, "color":get_random_color()},
        "airQuality":{"value":airQuality, "color":get_random_color()},
        "love_days":{"value":get_count(), "color":get_random_color()},
        "birthday_left":{"value":get_birthday(), "color":get_random_color()},
        "birthday_left2":{"value":get_birthday2(), "color":get_random_color()},
        "words":{"value":get_words(), "color":get_random_color()},
        "lucky":{"value":lucky(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
res2 = wm.send_template(user_id2, template_id, data)
print(res)
print(res2)
