#__author__ = 'Administrator'
# -*- coding: utf-8 -*-
import pyGPs
import numpy as np
import datetime
from numpy import linspace,array
import matplotlib.pyplot as plt
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter
from matplotlib.backends import backend_wxagg
from matplotlib.figure import Figure
import time
import matplotlib.dates as mdates
from scipy import interpolate
import codecs

plt.rcParams['font.sans-serif'] = ['SimHei'] #指定默认字体

plt.rcParams['axes.unicode_minus'] = False #解决保存图像是负号'-'显示为方块的问题

SHADEDCOLOR = [0.7539, 0.89453125, 0.62890625, 1.0]
MEANCOLOR = [ 0.2109375, 0.63385, 0.1796875, 1.0]
DATACOLOR = [0.12109375, 0.46875, 1., 1.0]
REALDATACOLOR = [0.46875, 0.12109375, 0.62890625, 1.0]
PRETCOLOR = [ 1.0, 0.2, 0.7539, 1.0]


class GPRY(pyGPs.GPR):
    def ploty(self,panel,axes,fg,p_x,p_y,keyWords,axisvals=None):
        '''
        Plot 1d GP regression result.

        :param list axisvals: [min_x, max_x, min_y, max_y] setting the plot range
        '''
        wx_panel = panel
        wx_axes = axes
        wx_fg = fg

        xs = self.xs    # test point
        x = self.x
        y = self.y
        ym = self.ym    # predictive test mean
        pre_x = []
        pre_y = []
        index = x[-1][0]+1
        for i in range(len(xs)):
            # print xs[i][0]
            if int(xs[i][0]+0.1) == index:
                pre_x.append([xs[i][0]])
                pre_y.append([ym[i][0]])
                # print ym[i][0]
                index = index + 1

        print pre_y

        x = list(x.T[0])


        wx_axes.plot_date(xs, ym, color=MEANCOLOR, ls='-', marker='None',ms=12, mew=2, lw=3.)
        wx_axes.plot_date(x, y, color=DATACOLOR, ls='None', marker='+',ms=12, mew=2)
        wx_axes.plot_date(pre_x, pre_y, color=PRETCOLOR, ls='None', marker='+',ms=12, mew=2)
        wx_axes.plot_date(p_x,p_y,color=REALDATACOLOR, ls='None', marker='+',ms=12, mew=2)

        # plt.fill_between(xss,ymm + 2.*np.sqrt(ys22), ymm - 2.*np.sqrt(ys22), facecolor=SHADEDCOLOR,linewidths=0.0)
        # plt.grid()

        # wx_panel.xlabel(u'时间')
        # wx_panel.ylabel(u'热度')
        # wx_panel.title(keyWords)

        wx_fg.autofmt_xdate()
        wx_panel.draw()


class DataPredict():

    def __init__(self,startDate,endDate,date2hot,hotWords):
        self.date , self.hot = self.getDate(startDate,endDate,date2hot)
        self.keyWords = hotWords

    def getDate(self,startDate,endDate,date2hot):
        date = []
        hot = []
        minDate = mdates.datestr2num(startDate)
        maxDate = mdates.datestr2num(endDate)
        for item in date2hot:
            value = item[1]
            dt = mdates.datestr2num(item[0])
            if dt >= minDate and dt <= maxDate:
                date.append(dt)
                hot.append(value)
        return date , hot

    def predict(self,panel,axes,fg):
        print '__date__:',self.date
        print '__hot__:',self.hot


        p_y = self.hot[-1]
        p_x = self.date[-1]
        del self.hot[-1]

        day_min = min(self.date)
        # 预测后面五天的数据
        day_max = max(self.date)+4

        see_len = []
        while day_min <= day_max:
            see_len.append([day_min])
            # 每两天之间切分为10个点
            day_min = day_min + 0.1

        ter_Date = []
        for i in range(0,len(self.date)-1):
            ter_Date.append( [self.date[i]])

        ter_Date = np.array(ter_Date)
        self.hot = np.array(self.hot)
        see_len = np.array(see_len)

        x = ter_Date      # training data
        y = self.hot     # training target
        z = see_len  # test data
    #   print x
    #   print y
    #   print z

    #   model = GPRY()      # specify model (GP regression)
    #   model.getPosterior(x, y) # fit default model (mean zero & rbf kernel) with data
    #   model.optimize(x, y)     # optimize hyperparamters (default optimizer: single run minimize)
    #   model.predict(z)         # predict test cases
    #   model.ploty()             # and plot result

        model = GPRY()      # specify model (GP regression)
        model.getPosterior(x, y) # fit default model (mean zero & rbf kernel) with data
        model.optimize(x, y)     # optimize hyperparamters (default optimizer: single run minimize)

    #   m = pyGPs.mean.Linear( alpha_list=[0.2, 0.4, 0.3] )
    #   k = 0.5*pyGPs.cov.Pre(x, x)
    #   model.setPrior(kernel=k)

    #   model.plotData_1d()
    #   model.setOptimizer("Minimize", num_restarts=20)
    #   model.optimize()
        model.predict(z)
        model.ploty(panel,axes,fg,p_x,p_y,self.keyWords)


