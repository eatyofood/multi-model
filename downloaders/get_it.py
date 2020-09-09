

import pandas as pd
import pandas_datareader as pdr
import os
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

## identify your security


sec = str(input('which security yont?'))
print('looking for price data............')
## this pulls daily price data
def get_dat(sec):
    df = pdr.get_data_yahoo(sec)
    return df
#pull price data from yahoo
df = get_dat(sec)
print('days_collected:',len(df))




import pandas_ta as pta
def sto(df):
    #creates a monthly, weekly, and current stochastic
    #adds, them to the data frame, and returns a list of the
    #names of the columns just added,
    #all in three letters
    df[df.index.name+'_copy'] = df.index
    a = pta.momentum.stoch(df.High,
                      df.Low,
                      df.Close,
                      fast_k=14,
                      slow_k=5,
                      slow_d=3)
    b = pta.momentum.stoch(df.High,
                      df.Low,
                      df.Close,
                      fast_k=14*7,
                      slow_k=5*7,
                      slow_d=3*7)
    c = pta.momentum.stoch(df.High,
                      df.Low,
                      df.Close,
                      fast_k=14*30,
                      slow_k=5*30,
                      slow_d=3*30)
    df = df.join(a)
    df = df.join(b)
    df = df.join(c)
    df
    stoch = []
    for i in df.columns:
        if 'STOCH' in i:
            stoch.append(i)
        hf = []
    for i in df.columns:
        if 'HF' in i:
            hf.append(i)
    hk =[]
    for i in df.columns:
        if 'Hk' in i:
            hk.append(i)
    hd = []
    for i in df.columns:
        if 'Hd' in i:
            hd.append(i)

    df['hd_slowave'] = (df[hd[1]] + df[hd[2]])/2
    df['sto_diff'] = (df['hd_slowave'] - df[hd[0]])
    df['riz'] = pta.momentum.rsi(df.Close,length=2)
    df['riz_sto'] = df['sto_diff'] - df['riz']

    return df,stoch


## mixing price data with the stocastic array
#### (indexed at 0)

df = df.merge(sto(df)[0])

df


## add in fundamentals
### this part is going to have an input option if you say yes then it will add this data...
### but this is the first run through that will do all the things, the other one will have to be called an UP_DATER

def finding_fun(sec):
    from yahoo_earnings_calendar import YahooEarningsCalendar
    yec = YahooEarningsCalendar()
    data = yec.get_earnings_of(sec)
    fdf = pd.DataFrame(data)
    return fdf

## this lets you know the next earnings report...which is nice...
#### if this doesnt transfer over to the other-df you gotta open a info_df or column
print('looking for fundamentals data....')
fdf = finding_fun(sec)
fdf
if len(fdf) > 0:
    print('got_it!')
print('reports_collected:',len(fdf))
import time

len(fdf)
print('mixing_em_together...')
fdf.set_index('startdatetime',inplace=True)

fdf.index.name = 'Date'

fdf

fdf.index = pd.to_datetime(fdf.index)

fdf.index = fdf.index.date
fdf

df['Date'] = df['Date_copy']
df.set_index('Date',inplace=True)
df

mdf = df.join(fdf)

#print(len(mdf))


print('saving_the_data')

mdf = mdf.fillna(method='ffill')



## save it

path = 'data/'
if not os.path.exists(path):
    os.mkdir(path)
shepana = (path+sec+'.csv')
mdf.to_csv(shepana)
print('...............................[[[[[DOWNLOAD COMPLEATE]]].................................]]')
get_dat(sec)
