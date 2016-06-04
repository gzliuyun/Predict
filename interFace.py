#!/usr/bin/env python
# -*- coding: utf-8 -*-
import wx
import os
from matplotlib.backends import backend_wxagg
from matplotlib.figure import Figure
import dealFile
import GPs

class InterFace(wx.Frame):
    def __init__(self):
        global filename ,words1 ,words2,contents,dateStart,dateEnd
        wx.Frame.__init__(self,None,-1, title = u"话题热度预测", size = (1100, 600))

        wx.StaticText(self,label=u'语料文件：',pos = (15,13))
        filename = wx.TextCtrl(self, pos = (80,10),size = (210,25))
        openButton = wx.Button(self, label = u'打开',pos = (305,10),size = (80,25))

        wx.StaticText(self,label=u'起止日期：',pos = (470,13))
        dateStart = wx.TextCtrl(self, pos = (550,10),size = (100,25))
        wx.StaticText(self,label=u'至',pos = (665,13))
        dateEnd = wx.TextCtrl(self, pos = (700,10),size = (100,25))
        submitButton = wx.Button(self, label = u'提交',pos = (820,10),size = (80,25))

        wx.StaticText(self,label=u'话题关键字：',pos = (15,55))
        words1 = wx.TextCtrl(self, pos = (90,50),size = (90,25))
        words2 = wx.TextCtrl(self, pos = (200,50),size = (90,25))
        sureButton = wx.Button(self, label = u'确定',pos = (305,50),size = (80,25))

        contents = wx.TextCtrl(self, pos = (15,90),size = (370,450), style = wx.TE_MULTILINE | wx.HSCROLL)

        panel = wx.Panel(self,pos=(420,55),size = (640,480))
        self.fg = Figure()
        self.panel = backend_wxagg.FigureCanvasWxAgg(panel,-1, self.fg)
        self.axes = self.panel.figure.gca()
        self.axes.cla()

        openButton.Bind(wx.EVT_BUTTON,self.openFile)
        sureButton.Bind(wx.EVT_BUTTON,self.sureWords)
        submitButton.Bind(wx.EVT_BUTTON,self.submit)

    def openFile(self, event):
        """
        Create and show the Open FileDialog
        """
        wildcard1 = "All files (*.*)|*.*|Python source (*.py; *.pyc)|*.py;*.pyc"
        dlg = wx.FileDialog(
            self, message=u"选择一个文件",
            defaultFile="",
            wildcard=wildcard1,
            style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
        )
        if dlg.ShowModal() == wx.ID_OK:
            tmp=""
            paths = dlg.GetPaths()
            for path in paths:
                tmp=tmp+path
            filename.SetValue(tmp)
        dlg.Destroy()

    def sureWords(self,event):

        wd1 = words1.GetValue()
        wd2 = words2.GetValue()
        Path = filename.GetValue()

        filePath = Path.replace("\\","/")
        df = dealFile.DealFile(filePath,wd1,wd2)
        self.date2hot = df.date2Hot
        self.keyWords = wd1+" "+ wd2

        file=open(df.dateHot.replace('/','\\'))
        contents.SetValue(file.read())

    def submit(self,event):
        self.axes.cla()
        startDate = dateStart.GetValue()
        endDate = dateEnd.GetValue()
        gps = GPs.DataPredict(startDate,endDate,self.date2hot,self.keyWords)
        gps.predict(self.panel,self.axes,self.fg)

if __name__ == '__main__':
    app = wx.App()
    win = InterFace()
    win.Show()
    app.MainLoop()