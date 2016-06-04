#__author__ = 'Administrator'
# -*- coding: utf-8 -*-

import time
import codecs
import os
import matplotlib.dates as mdates
class DealFile():
    def __init__(self,filename,words1,words2):
        self.filename = filename
        self.words1 = words1
        self.words2 = words2
        path  = os.path.realpath(__file__)
        path = path[0:path.rfind('\\')].replace('\\','/')
        self.keyWordFile = path+ '/file/keyWordsFile.txt'
        self.dateHot = path + '/file/dateHot.txt'
        self.date2Hot = {}
        self.readFile()


    def readFile(self):
        fr = codecs.open(self.filename,'r','utf8')
        fw = codecs.open(self.keyWordFile,'w','utf8')
        while True:
            line = fr.readline()
            if line:
                if len(self.words1) != 0 :
                    if line.find(self.words1) == -1:
                        continue

                if len(self.words2) != 0:
                    if line.find(self.words2) == -1:
                        continue
            else:
                break
            fw.write(line)
            self.date2hot(line)


        fr.close()
        fw.close()
        self.sortDate()

    def date2hot(self,line):
        list = line.split('	')
        try:
            date = list[-2].replace('"','').replace('/','-')
            hot = int(list[-1].replace('"',''))
            if  date in self.date2Hot.keys():
                self.date2Hot[date] += hot
            else :
                self.date2Hot[date] = hot
        except:
            return

    def sortDate(self):
        fw = codecs.open(self.dateHot,'w','utf8')
        self.date2Hot = sorted(self.date2Hot.items(), key=lambda dict:dict[0])
        for item in self.date2Hot:
            fw.write(''+item[0].encode('utf-8')+'	'+str(item[1])+'\n')
        fw.close()

