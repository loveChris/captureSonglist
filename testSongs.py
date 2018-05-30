# coding:utf-8

import MySQLdb
import requests,re
from urllib import urlencode
from time import sleep

def getID():
    db = MySQLdb.connect("localhost", "root", "123456", "songlist",charset="utf8")
    cursor = db.cursor()
    sql = "select songlist_id from songlist_name;"
    cursor.execute(sql)
    ids = cursor.fetchall()
    db.close()
    return ids

def getDetails(id):
    url = "http://music.163.com/playlist?id=%s" % id
    kv = {"User-Agent": "Mozilla/5.0",
          "Host": "music.163.com",
          "Referer": "http://music.163.com/",
          "Upgrade-Insecure-Requests": "1",
          "Accept": "text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8",
          "Accept - Encoding": "gzip, deflate",
          "Accept - Language": "zh - CN, zh;q = 0.9",
          "Connection": "keep - alive"
          }
    r = requests.get(url, headers=kv)
    response = r.text
    sleep(1)
    # print response.encode("utf-8")
    # with open("html.txt", "w")as f:
    #     f.write(response.encode("utf-8"))
    description = []
    description = re.findall(r'(?<=class="intr f-brk f-hide">)(.*?\n)(?=</p>)', response, re.S)
    if len(description) == 0:
        description = re.findall(r'(?<=class="intr f-brk">)(.*?\n)(?=</p>)', response, re.S)
    if len(description) == 0:
        description = ["Null!"]
    description = description[0].replace('\n','').replace('<b>','').replace('</b>','').replace('<br>','')
    playcount = re.findall(r'(?<=class="s-fc6">).*?(?=</strong>)', response)
    playcount = int(playcount[0])
    print "playcount :" ,playcount
    sort = re.findall(r'(?<=order=hot"><i>).*?(?=</i>)', response)
    sortmore = ""
    for i in range(len(sort)):
        if i<len(sort)-1:
            sortmore = sortmore+sort[i]+"、"
        else:
            sortmore = sortmore+sort[i]
    # print sortmore
    return description,playcount,sortmore

def updateList(description,playcount,sortmore,id):
    db = MySQLdb.connect("localhost", "root", "123456", "songlist", charset="utf8")
    cursor = db.cursor()
    sql = "update songlist_name set sortmore='%s',description='%s', playcount='%s', update_date=now()" \
          " where songlist_id = '%s';" % (MySQLdb.escape_string(sortmore),MySQLdb.escape_string(description),playcount,id)
    cursor.execute(sql)
    db.commit()
    db.close()

if __name__ == '__main__':
    ids = getID()
    for i in range(len(ids)):
        id = ids[i][0]
        print id
        description, playcount, sortmore=getDetails(id)
        updateList(description,playcount,sortmore,id)
    # description, playcount, sortmore = getDetails(791293)
    # print description
    # description, playcount, sortmore = getDetails(id=9732637)
    # print description
    # print playcount
    # print sortmore
    # updateList(description,playcount,sortmore,id=9732637)




