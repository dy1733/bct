import sys
import datetime
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import random
from scipy.signal import argrelextrema
from PyQt5.QtWidgets import QApplication, QFileDialog, QGridLayout, QPushButton, QLabel, QLineEdit, QWidget

class chatting_graph():
    def __init__(self):
        self.endindex = 0

    def initGraph(self, logpath, cps, noise):
        with open(logpath, 'rt', encoding='UTF8') as f:
            lines = f.readlines()
            endstr = lines[-1][1:9]
            
            if endstr[7] == ']':
                endstr = endstr[0:7]
            endarray = list(map(int, endstr.split(':')))

            endindex = int((endarray[0] * 3600 + endarray[1] * 60 + endarray[2]) / cps)
            timerange = range(0, endindex + 1)
            

            numchat = np.zeros(endindex + 1)
            for line in lines:
                    logstr = line[1:9]
                    if logstr[7] == ']':
                        logstr = logstr[0:7]
                    logarray = list(map(int, logstr.split(':')))
                    logindex = int((logarray[0] * 3600 + logarray[1] * 60 + logarray[2]) / cps)
                    numchat[logindex] += 1

            avgchat = np.copy(numchat)
            for i in timerange:
                if i < noise:
                    cl = avgchat[0: i + noise]
                elif i < endindex - noise - 1:
                    cl = avgchat[i - noise:i + noise]
                else:
                    cl = avgchat[endindex - noise - i - 1:endindex + 1]
                avg = round(np.mean(cl), 1)
                if avg == avgchat[i-1]:
                    avg += round(random.random() / 10, 2)
                avgchat[i] = avg
            
            self.endindex = endindex
            self.timerange = timerange
            self.numchat = numchat
            self.avgchat = avgchat
            self.maxchat = np.max(numchat)

    def detectHighlight(self, sensitivity, offset):
        highlights = [0]
        candidate = np.flipud(argrelextrema(self.avgchat, np.greater)[0])

        for c in candidate:
            flag = self.selectCandidate(c, sensitivity, offset, highlights[-1])
            if flag == 0:
                highlights.append(c)
            elif flag > 0:
                highlights.append(c + flag)
        self.highlights = np.flipud(highlights)

    def selectCandidate(self, c, sensitivity, offset, pre):
        result = -1
        if c < 6 or c > self.endindex - 6:
            return result
        if pre != 0 and pre - c < offset:
            return result
        
        numlist = self.numchat[c:c+offset]
        if np.min(numlist[0:1]) < sensitivity and numlist[2] < sensitivity - 1:
            return result

        result = np.argmax(numlist)

        if pre != 0 and pre - c - result < offset:
            result = -1
        
        return result

    def printGraph(self, cps, width, height, sen):
        path = 'NanumBarunGothic.ttf'
        fontprop = fm.FontProperties(fname=path, size=18)

        endindex = self.endindex
        timerange = self.timerange
        numchat = self.numchat
        avgchat = self.avgchat
        maxchat = self.maxchat
        highlights = self.highlights

        timefield = int(endindex / 60) + 1
        chatfield = int(maxchat / 5) + 1

        plt.figure(figsize=(timefield * width, chatfield * height))
        plt.grid(True, linestyle='-', color='0.75')
        plt.autoscale(tight=True)
        plt.title('채팅 트래픽', fontproperties=fontprop, fontsize=80)
        plt.xlabel('Time (In 10 minutes)', fontsize=52)
        plt.ylabel('Chat (Chatting per ' + str(cps) + ' seconds)', fontsize=52)

        plt.plot(timerange, numchat)
        plt.plot(timerange, avgchat, linewidth=3, color='green')

        f = open('./IO/result/highlight_' + str(sen) + '.txt', 'w')
        for i in range(0, len(highlights)):
            highlightpoint = highlights[i]
            if highlightpoint > 10 and highlightpoint < endindex - 10:
                plt.axvspan(highlightpoint - 1, highlightpoint, facecolor='red', edgecolor='gold', alpha=0.5)
                hl_string = str(datetime.timedelta(seconds=int(highlightpoint*cps)))
                f.write(hl_string+'\n')
        f.close()

        xr = np.arange(0, timefield)
        xl1 = list(xr * 60)
        xl2 = []
        
        for i in xr:
            dt = datetime.datetime.fromtimestamp(i * 600 + 54000)
            xl2.insert(i, dt.strftime("%H:%M:%S"))
        yr = np.arange(0, chatfield)
        yl1 = list(yr * 5)
        yl2 = yr * 5

        plt.xticks(xl1, xl2, fontsize=28)
        plt.yticks(yl1, yl2, fontsize=28)
        
        filename = './IO/result/chattingtraffic_' + str(sen) + '.png'

        plt.savefig(filename, bbox_inches='tight', pad_inches=0)
        # plt.show()

        
    def onebuttonrun(self):
        self.detectHighlight(25, 5)
        self.printGraph(10, 4, 2, 25)

        self.detectHighlight(15, 5)
        self.printGraph(10, 4, 2, 15)

        self.detectHighlight(10, 5)
        self.printGraph(10, 4, 2, 10)

        self.detectHighlight(5, 5)
        self.printGraph(10, 4, 2, 5)
        print("end")
