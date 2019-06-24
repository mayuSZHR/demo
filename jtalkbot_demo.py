#coding: utf-8
from datetime import datetime
import requests
import subprocess
import sys
import winsound


def jtalk(t):
    BIN = 'c:/open_jtalk/bin'
    DIC = 'c:/open_jtalk/dic'
    VOICE = 'c:/open_jtalk/bin/mei_normal.htsvoice'  # 任意の音響モデル
    open_jtalk=[BIN + '/open_jtalk.exe']
    mech=['-x',DIC]
    htsvoice=['-m',VOICE]
    speed=['-r','1.0']
    outwav=['-ow','jtalk.wav']
    cmd=open_jtalk+mech+htsvoice+speed+outwav
    popen = subprocess.Popen(cmd,stdin=subprocess.PIPE)

    popen.stdin.write(t.encode('shift-jis'))  # UTF-8からShift_JISに変換
    popen.stdin.close()
    popen.wait()

    winsound.PlaySound('jtalk.wav', winsound.SND_FILENAME)


def get_location(type):
    location = ''
    if type   == 'home':
        location = {'city' : '110010'}  # モブサイコ聖地：味玉県調味市
    elif type == 'office':
        location = {'city' : '120010'}  # モブサイコ聖地：タヨリの禁足地
    return location


def get_weather_forecast(type):
    url = 'http://weather.livedoor.com/forecast/webservice/json/v1'
    location = get_location(type)
    data = requests.get(url, location).json()
    
    result = data['forecasts'][0]['telop']
    return result


def can_dry_laundry():
    todays_weather = get_weather_forecast('home')  # 洗濯物は自宅に干す
    if '雨' in todays_weather:
        return False
    else:
        return True


def need_umbrella():
    todays_weather = get_weather_forecast('office')  # 外出先は職場
    if '雨' in todays_weather:
        return True
    else:
        return False


def res(t):
    print(t)
    jtalk(t)


def controller():
    while True:
        talk = input()
        if 'おはよう' in talk:
                res('おはよう！素敵な朝だね')
        elif 'おやすみ' in talk:
                res('おやすみ。いい夢を')
        elif 'ありがと' in talk:
                res('ふふ。どういたしまして')
        elif '洗濯物干していい' in talk:
            if can_dry_laundry() == True:
                res('うん。干して大丈夫')
            else:
                res('うーん……今日はやめておいた方がいいかも')
        elif '傘必要か' in talk:
            if need_umbrella() == True:
                res('持っていった方がいいね')
            else:
                res('今日は要らないよ')
        elif talk in 'またね':
            res('うん、またね。')  # TODO: 終了処理
        else:
            res('そうだねえ')


if __name__ == '__main__':
    res('何か用かな？')
    controller()
