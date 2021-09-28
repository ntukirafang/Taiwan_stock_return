from IPython.display import display, clear_output
from urllib.request import urlopen
import pandas as pd
import datetime
import requests
import sched
import time
import json

s = sched.scheduler(time.time, time.sleep)
def tableColor(val):
    if val > 0:
        color = 'red'
    elif val < 0:
        color = 'green'
    else:
        color = 'white'
    return 'color: %s' % color
def stock_crawler(targets):
    
    clear_output(wait=True)
    
    # Forming stock_list
    stock_list = '|'.join('tse_{}.tw'.format(target) for target in targets) 
    
    #　query data
    query_url = "http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch="+ stock_list
    data = json.loads(urlopen(query_url).read())

    # Filter out using value
    columns = ['c','n','z','tv','v','o','h','l','y']
    df = pd.DataFrame(data['msgArray'], columns=columns)
    df.columns = ['Stock code','Coperation company','Present price','Present mount','Comsumption mount','Start price','Higer price','Lower price','Yesterday price']
    df.insert(9, "Percentage of increse and decrease", 0.0) 
    
    # Add Percentage of increse and decrease column
    for x in range(len(df.index)):
        if df['當Present price'].iloc[x] != '-':
            df.iloc[x, [2,3,4,5,6,7,8]] = df.iloc[x, [2,3,4,5,6,7,8]].astype(float)
            df['Percentage of increse and decrease'].iloc[x] = (df['Present price'].iloc[x] - df['Yesterday price'].iloc[x])/df['Yesterday price'].iloc[x] * 100
    
    # Record present time
    time = datetime.datetime.now()  
    print("Update time:" + str(time.hour)+":"+str(time.minute))
    
    # show table
    df = df.style.applymap(tableColor, subset=['Percentage of increse and decrease column'])
    display(df)
    
    start_time = datetime.datetime.strptime(str(time.date())+'9:00', '%Y-%m-%d%H:%M')
    end_time =  datetime.datetime.strptime(str(time.date())+'13:30', '%Y-%m-%d%H:%M')
    
    # Recognize to stop python code
    if time >= start_time and time <= end_time:
        s.enter(1, 0, stock_crawler, argument=(targets,))
	# Prepratory Stock list 
stock_list = ['2022','2330']

# Pre second count down clock
s.enter(1, 0, stock_crawler, argument=(stock_list,))
s.run()
