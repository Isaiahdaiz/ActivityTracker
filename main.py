""" 
Author: Isaiah Daiz
Program: Activity tracker to record run time of processes running on a windows OS

Problem 1: Adding too many programs to check whether they are running slows down the program a lot.
Solution 1: Limit amount of applications allowed to 5

Problem 2: Cannot store tk objects into json file
Solution 2: Load data by pulling json data and convert from int to IntVar (tk object) and vice versa to store
 """

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
import subprocess
import json
import time
import sys


# Function by ewerybody @ Stackoverflow
def process_exists(process_name):
    call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
    # use buildin check_output right away
    output = subprocess.check_output(call).decode()
    # check in last line for process name
    last_line = output.strip().split('\r\n')[-1]
    # because Fail message could be translated
    return last_line.lower().startswith(process_name.lower())


# set root to tk
# Tkinter configuration
root = Tk()
root.title("Activity Tracker")
root.iconbitmap('icon.ico')
# root.geometry('300x300')
root.config(bg='gray')

# variables must be declared after root is set
count = DoubleVar(value=0)
appRunning = BooleanVar(value=FALSE)
appName = "None"
appListIndexRow = 0
message = StringVar()
MAX_APPS_COUNT = 5

def dictionaryToTk(dictionary):
    newDictionary = {}
    for key in dictionary:
        newDictionary[key] = DoubleVar(value=dictionary[key])
    return newDictionary


def tkToDictionary(dictionary):
    newDictionary = {}
    for key in dictionary:
        newDictionary[key] = dictionary[key].get()
    return newDictionary

# functions


def onAppOpen():
    openWinCenter()
    # Welcome the user
    message.set("Welcome!")
    # Open Elapse Time Meter Filename in write mode
    try:
        file = open("ETM.dat", "r")
        # Read count from .dat file
        count.set(file.read())
        # Close file
        file.close
    except:
        print("filename not found")
    appListLoad()


def onAppClose():
    saveAppListData()
    root.destroy()


def saveAppListData():
    global appListData
    appListData = tkToDictionary(appList)
    with open("sample.json", "w") as outfile:
        json.dump(appListData, outfile)


def loadAppListData():
    try:
        with open("sample.json") as infile:
            data = json.load(infile)
        return data
    except:
        print("Load app list error")

def appListLoad():
    global appListIndexRow
    appListIndexRow = 0
    for app in appList:
        appListAdd(app, appList[app])


def appListAdd(text, etm):
    global appListIndexRow
    global appList
    if (len(text) < 1):
        return
    if (appListIndexRow == MAX_APPS_COUNT):
        message.set("Max applications reached")
        return
    # Add to hashtable
    appList[text] = etm
    # Add to app list
    ttk.Label(frmList, text=text, width=30, anchor=CENTER).grid(column=0, row=appListIndexRow)
    ttk.Label(frmList, textvariable=etm, width=14, anchor=CENTER).grid(column=1, row=appListIndexRow)
    appListIndexRow += 1
    # Clear user input
    # global userInput
    userInput.set("")
    updateFrameLabel()


def appListRemove(app):
    if (app in appList):
        appList.pop(app, None)
        saveAppListData()
        restart()
    if (len(app) > 0):
        message.set("Application not found")

def openWinCenter():
    w = root.winfo_width() # width for the Tk root
    h = root.winfo_height() # height for the Tk root

    # get screen width and height
    ws = root.winfo_screenwidth() # width of the screen
    hs = root.winfo_screenheight() # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

    # set the dimensions of the screen 
    # and where it is placed
    root.geometry('+%d+%d' % (x, y))

def restart():
    python = sys.executable
    os.execl(python, python, * sys.argv)


def submitApp(text):
    global appName
    appName = text
    print("New application name: " + appName)

# Increments etm by 1 minute


def incETM(app, amount):
    appList[app].set(appList[app].get() + amount)


def resetETM(app):
    appList[app].set(value=0)


def resetAllETM():
    for app in appList:
        resetETM(app)


# Problem: Adding more applications slows down the program
# Solution: Measure time it takes to update, then add that time to running programs
refreshTime = 0


def refreshElapseTimeMeter():
    global refreshTime
    startRefreshTime = time.time()
    for app in appList:
        if process_exists(app):
            incETM(app, refreshTime)
            incETM(app, 1)
    endRefreshTime = time.time()
    refreshTime = endRefreshTime - startRefreshTime
    print(endRefreshTime - startRefreshTime)


def onClickRefresh():
    incETM()


def browseApp():
    currFile = os.getcwd()
    tempFile = filedialog.askopenfilename(
        parent=root, initialdir=currFile, title='Select an application')
    if len(tempFile) < 1:
        return
    if tempFile.endswith(".exe") == FALSE:
        print("File must be executable (.exe)")
        message.set("File must be executable (.exe)")

    else:
        print("Filepath: " + tempFile)
        newApp = tempFile[tempFile.rfind("/") + 1:]
        # Do not add duplicate apps
        if newApp in appList:
            print("Application already added")
            return
        appListAdd(newApp, DoubleVar(value=0))
        message.set("Application added!")

# Contiunous 1 second loop


def secondLoop(time):
    refreshElapseTimeMeter()
    root.after(time, lambda: secondLoop(time))

def testSecond():
    testSecondVar.set(testSecondVar.get() + 1)
    root.after(1000, testSecond)


def testPrint():
    print("test")


def deleteApp():
    print()


def updateFrameLabel():
    frameLabel.set("Application List (%i/%i)" %
                   (appListIndexRow, MAX_APPS_COUNT))
    
testSecondVar = IntVar(value=0)
frameLabel = StringVar()
# main window

# Top Control Area
frm = ttk.Frame(root, padding=10)
frm.grid()
frm.pack(fill="x", expand="yes")
userInput = StringVar()
ttk.Entry(frm, textvariable=userInput, width=30).grid(column=0, row=1)
ttk.Label(frm, textvariable=message, anchor=CENTER).grid(column=0, row=0, columnspan=2)
ttk.Button(frm, text="Add New", command=lambda: appListAdd(
    userInput.get(), DoubleVar(value=0))).grid(column=1, row=1)
ttk.Button(frm, text="Remove", command=lambda: appListRemove(
    userInput.get())).grid(column=1, row=2)
ttk.Button(frm, text="Browse", width=30, command=browseApp).grid(column=0, row=2)

# Application List
updateFrameLabel()
ttk.Label(root, textvariable=frameLabel, padding=10).pack(
    fill="x", expand="yes", )
separator = ttk.Separator(root, orient='horizontal')
separator.pack(fill='x')
frmList = ttk.Frame(root, padding=5)
frmList.pack(fill="both", expand="yes")
appListData = loadAppListData()
appList = dictionaryToTk(appListData)
onAppOpen()
# allow 1 seconds to pass before looping
testSecond()
timeToLoop = 1000
root.after(timeToLoop, lambda: secondLoop(timeToLoop))
root.protocol("WM_DELETE_WINDOW", onAppClose)
root.resizable(False, False)
root.mainloop()
