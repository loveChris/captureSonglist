# coding:utf-8

import requests,re,os
from urllib import urlencode
from xlutils.copy import copy
from xlrd import open_workbook


sorting = {"cat":"欧美"}
sorting = urlencode(sorting)
print sorting
url = r"http://music.163.com/discover/playlist/?%s" % sorting
kv = {"User-Agent": "Mozilla/5.0",
      "Host": "music.163.com",
      "Referer":"http://music.163.com/",
      "Upgrade-Insecure-Requests": "1",
      "Accept": "text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8",
      "Accept - Encoding": "gzip, deflate",
      "Accept - Language": "zh - CN, zh;q = 0.9",
      "Connection": "keep - alive"
      }
r = requests.get(url,headers=kv)
with open("html.txt","w") as f:
    f.write(r.text.encode("utf-8"))