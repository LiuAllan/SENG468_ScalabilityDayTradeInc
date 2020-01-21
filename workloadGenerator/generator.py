# To run: change filename to desired 1userWorkLoad
# File needs to be in the same directory as the program
# python3 generator.py
import re
filename = "1userWorkLoad"

def ADD(params):
    print("ADD {}".format(params))
def QUOTE(params):
    print("QUOTE {}".format(params))
def BUY(params):
    print("BUY {}".format(params))
def COMMIT_BUY(params):
    print("COMMIT_BUY {}".format(params))
def CANCEL_BUY(params):
    print("CANCEL_BUY {}".format(params))
def SELL(params):
    print("SELL {}".format(params))
def COMMIT_SELL(params):
    print("COMMIT_SELL {}".format(params))
def CANCEL_SELL(params):
    print("CANCEL_SELL {}".format(params))
def SET_BUY_AMOUNT(params):
    print("SET_BUY_AMOUNT {}".format(params))
def SET_BUY_TRIGGER(params):
    print("SET_BUY_TRIGGER {}".format(params))
def CANCEL_SET_BUY(params):
    print("CANCEL_SET_BUY {}".format(params))
def SET_SELL_AMOUNT(params):
    print("SET_SELL_AMOUNT {}".format(params))
def SET_SELL_TRIGGER(params):
    print("SET_SELL_TRIGGER {}".format(params))
def CANCEL_SET_SELL(params):
    print("CANCEL_SET_SELL {}".format(params))
def DUMPLOG(params):
    print("DUMPLOG {}".format(params))
def DISPLAY_SUMMARY(params):
    print("DISPLAY_SUMMARY {}".format(params))
def PROBLEM(params):
    print("PROBLEM {}".format(params))

switcher = {
    "ADD":ADD,
    "QUOTE":QUOTE,
    "BUY":BUY,
    "COMMIT_BUY":COMMIT_BUY,
    "CANCEL_BUY":CANCEL_BUY,
    "SELL":SELL,
    "COMMIT_SELL":COMMIT_SELL,
    "CANCEL_SELL":CANCEL_SELL,
    "SET_BUY_AMOUNT":SET_BUY_AMOUNT,
    "SET_BUY_TRIGGER":SET_BUY_TRIGGER,
    "CANCEL_SET_BUY":CANCEL_SET_BUY,
    "SET_SELL_AMOUNT":SET_SELL_AMOUNT,
    "SET_SELL_TRIGGER":SET_SELL_TRIGGER,
    "CANCEL_SET_SELL":CANCEL_SET_SELL,
    "DUMPLOG":DUMPLOG,
    "DISPLAY_SUMMARY":DISPLAY_SUMMARY

}
file = open(filename, "r")
#Creates a list of list which each line is broken into parameters
listItems = [re.sub("\[[0-9]+] ","", item.strip()).split(",") for item in file.readlines()]

for item in listItems:
    switcher.get(item[0], PROBLEM)(item[1:])
