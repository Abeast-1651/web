from flask import Flask,render_template,request
from flask import *
import plotly 
import plotly.graph_objs as go
import pandas as pd
import json
import requests
import lxml.html as lh
import pandas as pd
import csv
import pandas as pd
import time
# from flask_table import Table , Col


app=Flask(__name__)

def show_tables():
    url="https://www.mohfw.gov.in/"
    page = requests.get(url)
    doc = lh.fromstring(page.content)
    tr_elements = doc.xpath('//tr')
    # tr_elements = doc.xpath('//tr')
    col=[]
    big=[]
    i=0
    for t in tr_elements[0]:
        i+=1
        name=t.text_content()
        col.append((name,[]))
    for j in range(1,len(tr_elements)):
        T=tr_elements[j]
        if len(T)!=5:
            continue
        i=0
        for t in T.iterchildren():
            data=t.text_content() 
            if i>0:
                try:
                    data=int(data)
                except:
                    pass
            col[i][1].append(data)
            i+=1
    Dict={title:column for (title,column) in col}
    df=pd.DataFrame(Dict)
    x=list(df['Death'])
    y=list(df['Cured/Discharged/Migrated'])

    data = df
    # data.set_index(['Name'], inplace=True)
    data.set_index(['S. No.'], inplace=True)
    data.index.name=None
    # females = data.loc[data.Gender=='f']
    # males = data.loc[data.Gender=='m']
    return data.to_html(classes='female'),sum(x),sum(y)
    # titles = ['na', 'Female surfers', 'Male surfers'])
def india(df):
    mp=[]
    total_count=[]
    count=0
    number=[]
    for i in range(len(df['Date Announced'])):
        if df['Detected State'][i]!='':
            count+=1
            mp.append(df['Date Announced'][i])
            number.append(count)
    dic=dict()
    for i in mp:
        if i not in dic:
            dic[i]=1
        else:
            dic[i]+=1
    day_count=list(dic.values())
    day=list(dic.keys())
    for i in range(len(day_count)):
        if i==0:
            total_count.append(day_count[i]+0)
        else:
            total_count.append(day_count[i]+total_count[i-1])
    data=[go.Scatter(x=day, y=total_count,
                    mode='lines',
                    name='lineplot')]
    graphJSON=json.dumps(data,cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON,total_count[-1]

def generate_graph(df,state):
    
    # df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')
    mp=[]
    total_count=[]
    count=0
    number=[]
    # state="Madhya Pradesh"
    for i in range(len(df['Detected State'])):
        if df['Detected State'][i]==state:
            count+=1
            mp.append(df['Date Announced'][i])
            number.append(count)
    dic=dict()
    for i in mp:
        if i not in dic:
            dic[i]=1
        else:
            dic[i]+=1
    day_count=list(dic.values())
    day=list(dic.keys())
    for i in range(len(day_count)):
        if i==0:
            total_count.append(day_count[i]+0)
        else:
            total_count.append(day_count[i]+total_count[i-1])
    data=[go.Scatter(x=day, y=total_count,
                    mode='lines',
                    name='lineplot')]
    graphJSON=json.dumps(data,cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


@app.route('/',methods=['POST','GET'])
def index():
    while(True):
        url='https://docs.google.com/spreadsheets/u/1/d/e/2PACX-1vSc_2y5N0I67wDU38DjDh35IZSIS30rQf7_NYZhtYYGU1jJYT6_kDx4YpF-qw0LSlGsBYP8pqM_a1Pd/pubhtml#'
        page = requests.get(url)
        doc = lh.fromstring(page.content)
        tr_elements = doc.xpath('//tr')
        # tr_elements = doc.xpath('//tr')
        col=[]
        i=0
        for t in tr_elements[1]:
            i+=1
            name=t.text_content()
            col.append((name,[]))

        for j in range(3,len(tr_elements)):
            T=tr_elements[j]
            if len(T)!=27:
                continue
            i=0
            for t in T.iterchildren():
                data=t.text_content() 
                if i>0:
                    try:
                        data=int(data)
                    except:
                        pass
                col[i][1].append(data)
                i+=1
        Dict={title:column for (title,column) in col}
        df=pd.DataFrame(Dict)
        temp=india(df)
        total=temp[1]
        temp2=show_tables()
        tab=temp2[0]
        deaths=temp2[1]
        rec=temp2[2]
        line=temp[0]
        line5=generate_graph(df,'Bihar')
        line20=generate_graph(df,'Madhya Pradesh')
        line21=generate_graph(df,'Maharashtra')
        return render_template('index.html',plot=line,plot5=line5,plot20=line20,plot21=line21,totals=total,tables=tab,dead=deaths,recover=rec)
        time.sleep(3600)





if __name__=='__main__':
    app.run(debug=True)