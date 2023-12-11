import numpy as np
import pandas
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd

MONEY = 10000
MAX_SAMPLES = 1000
START = 0
SAMPLES = MAX_SAMPLES - START
MACD1 = 26
MACD2 = 12
SIGNAL1 = 9

column_names = ['Date', 'Close']
data = pandas.read_csv("muchDataMuchWow.csv", header=0)
close = data['Close'].to_numpy()
close = close[START:MAX_SAMPLES]
dates = pd.to_datetime(data['Date'])


def EMA(N, data, start):
    alfa = 2 / N + 1
    upper = data[start]
    lower = 1
    for i in range(1, N):
        upper += pow(alfa,i) * data[start - i]
        lower += pow(alfa,i)
    wynik = upper / lower
    return wynik
def MACD(data, start):
    return EMA(MACD2,data,start) - EMA(MACD1,data,start)
def SIGNAL(macd, start):
    return EMA(SIGNAL1,macd,start)


def buySellPoints(macd, signal, buy, sell):
    mniejsze = macd[SIGNAL1] < signal[0]
    for i in range(SAMPLES-MACD1-SIGNAL1):
        if(mniejsze):
            if signal[i]<macd[SIGNAL1 + i]:
                buy.append(i+MACD1+SIGNAL1)
                mniejsze = False
        else:
            if signal[i] > macd[SIGNAL1 + i]:
                sell.append(i +MACD1+SIGNAL1)
                mniejsze = True

if __name__ == '__main__':
    macd_res = np.zeros(SAMPLES-MACD1)
    signal_res = np.zeros(SAMPLES-MACD1-SIGNAL1)
    for i in range(SAMPLES-MACD1):
        macd_res[i] = MACD(close,i+MACD1)
    for i in range(SAMPLES-MACD1-SIGNAL1):
        signal_res[i] = SIGNAL(macd_res,i+SIGNAL1)
    buyPoints = []
    sellPoints = []
    buySellPoints(macd_res,signal_res,buyPoints,sellPoints)
    plt.plot(dates[MACD1+START:SAMPLES+START],macd_res)
    plt.plot(dates[MACD1+SIGNAL1+START:SAMPLES+START],signal_res)
    plt.legend(["MACD","Signal line"])
    plt.xlabel("date")
    plt.ylabel("MACD value")
    plt.grid()
    x = []
    for p in buyPoints:
        x.append(dates[p+START])
    y = []
    for p in buyPoints:
        y.append(signal_res[p - MACD1 - SIGNAL1])
    plt.scatter(x, y,color = 'blue',zorder= 2)
    x = []
    for p in sellPoints:
        x.append(dates[p+START])
    y = []
    for p in sellPoints:
        y.append(signal_res[p - MACD1 - SIGNAL1])
    plt.scatter(x, y,color = 'blue',zorder= 2)
    plt.show()
    money = MONEY
    dogecoins = 0
    for i in range(len(sellPoints)):
        dogecoins = money/close[buyPoints[i]]
        money = dogecoins*close[sellPoints[i]]
    plt.plot(dates[START:START+SAMPLES],close)
    plt.xlabel("date")
    plt.ylabel("price")
    plt.grid()
    plt.show()
    money = round(money,2)
    print(str(money) + "$")

