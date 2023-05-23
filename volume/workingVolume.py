# -*- coding: GB2312 -*- 
import os
import pandas as pd
import numpy as np
import openpyxl
import xlrd
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

###ExcelSecurities=pd.read_csv('C:\\Users\\Administrator\\Desktop\\601066.xls',skiprows=[0,1,3],usecols=[0,1,2,3,4,5],encoding='GB2312',sep='\t')
ExcelSecurities=pd.read_csv('C:\\Users\\Administrator\\Desktop\\512170.txt',skiprows=[0,1,3],skipfooter=1,usecols=[0,1,2,3,4,5],encoding='GB2312',sep='\t')


ExcelSecurities.head()
columns2=['Date','Open','High','Low','Close','Volume']
for i in range(len(ExcelSecurities.columns)):
     ExcelSecurities.rename(columns={ExcelSecurities.columns[i]: columns2[i]},inplace=True) 
###ExcelSecurities.rename(index = ExcelSecurities.loc[:,'Date'])
ExcelSecurities.index=pd.to_datetime(ExcelSecurities.loc[:,'Date'])
close=ExcelSecurities.Close
if float(ExcelSecurities.Close.mean())<1:
     close=ExcelSecurities.Close*100
elif float(ExcelSecurities.Close.mean())<10 and float(ExcelSecurities.Close.mean())>1:
     close=ExcelSecurities.Close*10

BreakClose=np.ceil(close/2)*2
BreakClose.name='BreakClose'
pd.DataFrame({'BreakClose':BreakClose,\
            'Close':close}).head(n=2)
###ExcelSecurities=ExcelSecurities.iloc[0:]
###ExcelSecurities=ExcelSecurities.drop([0,2])
volume=ExcelSecurities.Volume

PrcChange=close.diff()
temp=volume[PrcChange>0]

UpVol=volume.replace(np.array(temp),0)
UpVol[0]=0
temp=volume[PrcChange<=0]
DownVol=volume.replace(np.array(temp),0)
DownVol[0]=0
minbreak=int(BreakClose.min()-2)
maxbreak=int(BreakClose.max()+2)
def VOblock(vol):
    sum={}
    for x in range(minbreak,maxbreak,1):
         print(np.sum(vol[BreakClose==x]))
         sum[x]=np.sum(vol[BreakClose==x])
    return sum

cumUpVol=VOblock(UpVol)
cumDownVol=VOblock(DownVol)

fig,ax=plt.subplots()
ax1=ax.twiny()
ax.plot(close)
ax.set_title('不同价格区间的累积成交量图')
ax.set_ylim(minbreak,maxbreak)
ax.set_xlabel('时间')
plt.setp(ax.get_xticklabels(), rotation=20,horizontalalignment='center')
cumUpVolkeys = list(cumUpVol.keys())
cumUpVolvalues = list(cumUpVol.values())
ax1.barh(y=cumUpVolkeys,width=cumUpVolvalues,\
         height=2,color='g',alpha=0.2)

cumDownVolvalues = list(cumDownVol.values())
ax1.barh(y=cumUpVolkeys,width=cumDownVolvalues,height=2,left=cumUpVolvalues,\
        color='r',alpha=0.2)
plt.show()

volume=ExcelSecurities.Volume
VolSMA5=volume.rolling(5).apply(np.mean).dropna()
VolSMA10=volume.rolling(10).apply(np.mean).dropna()
VolSMA=((VolSMA5+VolSMA10)/2).dropna()
VolSMA.head(n=3)

close=ExcelSecurities.Close
PrcSMA5=close.rolling(5).apply(np.mean).dropna()
PrcSMA20=close.rolling(20).apply(np.mean).dropna()

def upbreak(Line,RefLine):
    signal=np.all([Line>RefLine,Line.shift(1)<RefLine.shift(1)],axis=0)
    return(pd.Series(signal[1:],index=Line.index[1:]))
def downbreak(Line,RefLine):
    signal=np.all([Line<RefLine,Line.shift(1)>RefLine.shift(1)],axis=0)
    return(pd.Series(signal[1:],index=Line.index[1:]))

UpSMA=upbreak(PrcSMA5[-len(PrcSMA20):],PrcSMA20)*1
DownSMA=downbreak(PrcSMA5[-len(PrcSMA20):],PrcSMA20)*1