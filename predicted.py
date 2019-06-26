# import requests
# import re
import json
import sys
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import regression
from numpy import *

def drawResult():
    results = []
    event1 = []
    event2 = []
    with open('./data.json', 'r') as f:
        results = json.load(f)
    for result in results:
        event1.append(float(result[0]))
        event2.append(float(result[1]))
    print(event1)
    print(event2)
    plt.scatter(event1, event2)
    plt.show()

def writeJsontoTxt():
    results = []
    with open('./data.json', 'r') as f:
        results = json.load(f)
    str = ''
    for result in results:
        str = str + '1.00\t{}\t{}\n'.format(result[0],result[1])
    with open('./results.txt', 'w') as f:
        f.write(str)


# 标准线性回归
def lineResult(fileName):
    xArr,yArr=regression.loadDataSet(fileName)
    ws = regression.standRegres(xArr, yArr)     #取得回归系数矩阵
    # 画出回归曲线
    xMat = mat(xArr)
    yHat = xMat*ws
    fig = plt.figure()
    ax = fig.add_subplot(111)
    xCopy = xMat.copy()
    xCopy.sort(0)
    yHat=xCopy*ws
    ax.plot(xCopy[:,1], yHat)
    ax.scatter(xMat[:, 1].flatten().A[0], mat(yArr).T.flatten().A[0], s=2, c='red')
    plt.show()


# 局部加权线性回归
def lwlrResult(fileName, weight):
    xArr,yArr=regression.loadDataSet(fileName)
    yHat = regression.lwlrTest(xArr, xArr, yArr, weight)    #取得各点的回归系数矩阵
    # 画出回归曲线
    xMat=mat(xArr)
    srtInd = xMat[:,1].argsort(0)
    xSort=xMat[srtInd][:,0,:]
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(xSort[:,1],yHat[srtInd])
    ax.scatter(xMat[:,1].flatten().A[0], mat(yArr).T.flatten().A[0], s = 2, c ='red')
    plt.show()



if __name__ == '__main__':
    try:
        method = sys.argv[1]
        data = sys.argv[2]
        if method == 'line':
            lineResult(data)
        if method == 'lwlr':
            weight = 1
            if len(sys.argv) == 4:
                weight = float(sys.argv[3])
            lwlrResult(data, weight)
    except:
        print('parameter error!')