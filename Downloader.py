import os
import sys
import time
import datetime
from idm import IDMan
from selenium import webdriver
from urllib.error import HTTPError
import urllib.request as urllib


class internet:
    def buy():
        print(" > Buying Internet...")
        #   width=1440   &   height=2960
        command="cmd /c "+sys.path[0][0:2].lower()+" & cd "+sys.path[0]+"\\ADB"
        #command+=" & adb shell wm size"
        command+=" && adb shell input keyevent 3 && timeout /T 5"      # Go Home
        command+=" && adb shell am force-stop com.mtni.myirancell && timeout /T 5"      # Close All Apps
        command+=" && adb shell monkey -p com.mtni.myirancell -v 1 && timeout /T 10"      # Open MyIrancell
        command+=" && adb shell input tap 720 2760 && timeout /T 5"      # Open Menu
        command+=" && adb shell input tap 1050 1480 && timeout /T 5"      # Go To Internet Section
        command+=" && adb shell input tap 720 1200 && timeout /T 5"      # Click On Package
        command+=" && adb shell input tap 720 1520 && timeout /T 5"      # Click On Activate
        command+=" && adb shell input tap 720 1580 && timeout /T 10"      # Buy Using Account Currency
        command+=" && adb shell input keyevent 3 && timeout /T 5"      # Go Home

        os.system(command)

        print("   > Bought Internet For 3 Hours.")

    def turnOn():
        command="cmd /c "+sys.path[0][0:2].lower()+" & cd "+sys.path[0]+"\\ADB"
        command+=" && adb shell svc data enable"
        os.system(command)
        print("   > Mobile Data Turned On.")

    def turnOff():
        command="cmd /c "+sys.path[0][0:2].lower()+" & cd "+sys.path[0]+"\\ADB"
        command+=" && adb shell svc data disable"
        os.system(command)
        print("   > Mobile Data Turned Off.")

def selectLinks():
    print("   > Selecting Download Links.")
    maxSize=60000000000
    links=[]
    data=open(sys.path[0]+"\\Links.txt","r").read().splitlines()
    file=open(sys.path[0]+"\\Links.txt","w")
    size=0

    for i in data:
        if i=='' or i=='\n': continue

        try:
            size+=int(urllib.urlopen(i).info()["Content-Length"])
            if size>maxSize :
                file.write(i+"\n")
            else:
                links.append(i)
        except HTTPError:
            print("     > This Link Is Curropted: "+i)
            file.write(i+"\n")

    file.close()
    print("   > Total Of "+str(len(links))+" Links Have Been Selected.")
    return links

def startDownload():
    while True:
        h=datetime.datetime.now().hour
        m=datetime.datetime.now().minute
        if h==4:
            break
        else:
            print("   > Waiting Until 4 To Start Downloading.(Checked At "+str(h)+":"+str(m)+")")
            time.sleep(600)

    downloader=IDMan()
    links=selectLinks()
    downloadSpeed=8000000
    internet.buy()
    time.sleep(15)
    internet.turnOn()

    print("   > Downloading Started.")

    for link in links:
        size=int(urllib.urlopen(link).info()["Content-Length"])
        t=int(size/downloadSpeed)
        downloader.download(link, sys.path[0]+"\\Downloads", output=None, referrer=None, cookie=None, postData=None, user=None, password=None, confirm = False, lflag = None, clip=False)
        print("     > Waiting for "+str(t)+" Seconds To Download From "+link+".")
        time.sleep(t)

    print("   > Downloading Finished.")
    internet.turnOff()


try:
    os.mkdir(sys.path[0]+"\\Downloads")
    print(' > Created "Downloads" Folder.')
except OSError:
    print(' > "Downloads" Folder Already Exists.')

while True:
    ans=input(" > Do You Want Me To Download Or What?\n   > ")
    if ans.lower() in ["yes","downloaad","yep"]:
        startDownload()
    elif ans.lower() in ["no","dont"]:
        print("   > OK. I'll Ask You Again In 12 Hours.")
        time.sleep(43200)
    elif ans.lower() in ["add","link"]:
        link=input("   > Paste Your Link: ")
        file=open(sys.path[0]+"\\Links.txt","a")
        file.write(link)
        file.close()
        print("   > New Link Has Been Added.")
    elif ans.lower() in ["test","tester"]:
        print("   > List Of Available Functions:\n     > internet.turnOn()\n     > internet.turnOff()\n     > internet.buy()\n     > selectLinks()\n     > startDownload()\n     > Exit")
        while True:
            a=input("   > Whitch Function Do You Want To Test?\n     > ")
            if a.lower() in "internet.turnon()": internet.turnOn()
            elif a.lower() in "internet.turnoff()": internet.turnOff()
            elif a.lower() in "internet.buy()": internet.buy()
            elif a.lower() in "selectlinks()": selectLinks()
            elif a.lower() in "startdownload()": startDownload()
            elif a.lower() in ["exit","break","quit","close"]: break
    elif ans.lower() in ["exit","quit","close"]:
        print("   > Closing The Program.")
        sys.exit(0)
    else:
        print("   > I Dont Get It.")
        continue
