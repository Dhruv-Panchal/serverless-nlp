import streamlit as st 
import requests
import time
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from google.cloud import bigquery
import matplotlib.pyplot as plt


    
def custom_day(event, start, end):
    start_date = str(start)
    end_date = str(end)
    syear = int(start_date[0:4])
    smonth = int(start_date[5:7])
    sdate = (start_date[8:10])
    if sdate[0] == 0:
        sdate = int(sdate[1])
    else:
        sdate = int(sdate)
    eyear = int(end_date[0:4])
    emonth = int(end_date[5:7])
    edate = (end_date[8:10])
    if (edate[0]) == 0:
        edate = int(edate[1])
    else:
        edate = int(edate)     
    url = 'https://us-central1-nlp-big-data.cloudfunctions.net/guardian-data'
    myobj = {"keyword":event,
            	"sdy":syear,
	            "sdm":smonth,
	            "sdd": sdate,
	            "edy": eyear,
	            "edm": emonth,
	            "edd": edate
            }
    response = requests.post(url,json=myobj)
    return response
def seq1(query,sdate,edate):
    start_date = str(sdate)
    end_date = str(edate)
    syear = (start_date[0:4])
    smonth = (start_date[5:7])
    sdate = (start_date[8:10])
    
    eyear = (end_date[0:4])
    emonth = (end_date[5:7])
    edate = (end_date[8:10])

    
    x = syear+'-'+smonth+'-'+sdate
    y = eyear+'-'+emonth+'-'+edate
    client = bigquery.Client()
    sql = '''
    SELECT DATE, AVG(SENTIMENT)* AVG(MAGNITUDE)AVERAGEMS FROM `nlp-big-data.pubsub.table1` WHERE query = @query and date BETWEEN @sdate AND @edate  GROUP BY DATE ORDER BY DATE ASC LIMIT 1000
    ''' 
    job_config =bigquery.QueryJobConfig(query_parameters=[bigquery.ScalarQueryParameter("query", "STRING",query),bigquery.ScalarQueryParameter("sdate", "STRING",x),
    bigquery.ScalarQueryParameter("edate", "STRING",y)    ])    

    df = client.query(sql,location="US",job_config=job_config).to_dataframe()
    return df

def seq2(query):
    client = bigquery.Client()
    sql = '''
    SELECT DISTINCT CATEGORY, AVG(SENTIMENT)* AVG(MAGNITUDE)AVERAGEMS FROM `nlp-big-data.pubsub.table1` WHERE query = @query GROUP BY CATEGORY
    
    ''' 
    
    job_config = bigquery.QueryJobConfig(query_parameters=[bigquery.ScalarQueryParameter("query", "STRING",query)])
    
    
    
    #query_job = client.query(sql,location="US",job_config=job_config)


    df = client.query(sql,location="US",job_config=job_config).to_dataframe()
    return df

def seq3(query):
    client = bigquery.Client()
    sql = '''

    SELECT DISTINCT CATEGORY, COUNT(*)COUNT FROM `nlp-big-data.pubsub.table1`  WHERE query = @query GROUP BY CATEGORY
    
    ''' 
    
    job_config = bigquery.QueryJobConfig(query_parameters=[bigquery.ScalarQueryParameter("query", "STRING",query)])
    
    
    
    #query_job = client.query(sql,location="US",job_config=job_config)


    df = client.query(sql,location="US",job_config=job_config).to_dataframe()
    return df

def seq4(query,sdate,edate,cross=None):
    start_date = str(sdate)
    end_date = str(edate)
    syear = (start_date[0:4])
    smonth = (start_date[5:7])
    sdate = (start_date[8:10])
    
    eyear = (end_date[0:4])
    emonth = (end_date[5:7])
    edate = (end_date[8:10])

    
    x = syear+'-'+smonth+'-'+sdate
    y = eyear+'-'+emonth+'-'+edate




    cross = "%"+cross+"%"
    client = bigquery.Client()
    if cross==None:
         sql = '''

    SELECT DISTINCT CATEGORY, AVG(SENTIMENT)* AVG(MAGNITUDE)COUNT FROM `nlp-big-data.pubsub.table1` where TEXT LIKE "%China%" and query = @query and date BETWEEN @sdate AND @edate GROUP BY CATEGORY
    
    ''' 
    else:
        sql = '''

    SELECT DISTINCT CATEGORY,AVG(SENTIMENT)* AVG(MAGNITUDE)COUNT FROM `nlp-big-data.pubsub.table1` where TEXT LIKE @cross and query = @query and date BETWEEN @sdate AND @edate  GROUP BY CATEGORY
    
    ''' 
    
    job_config = bigquery.QueryJobConfig(query_parameters=[
        
        bigquery.ScalarQueryParameter("query", "STRING",query),
        bigquery.ScalarQueryParameter("cross", "STRING",cross),
        bigquery.ScalarQueryParameter("sdate", "STRING",x),
        bigquery.ScalarQueryParameter("edate", "STRING",y)  
    
    ])
    df = client.query(sql,location="US",job_config=job_config).to_dataframe()
    return df



def prog(query,today,days5):
        progress_bar = st.progress(0)
        progress_bar.progress(10)
        status = st.info("Running Cloud Functions")
        d = custom_day(query,today,days5)
        time.sleep(1)
        progress_bar.progress(20)
        status.info("Running Pubsub Functions")
        time.sleep(1)
        progress_bar.progress(40)
        status.info("Cleaning Data")
        time.sleep(1)
        progress_bar.progress(50)
        status.info("Detecting Sentiments and Entities")
        time.sleep(0.8)
        progress_bar.progress(60)
        status.info("Running Transformations")
        time.sleep(0.8)
        progress_bar.progress(70)
        status.info("Queueing Data For Big Query")
        time.sleep(1)
        progress_bar.progress(90)
        status.info("Analyzing Data")
        time.sleep(1)
        progress_bar.progress(100)
        st.success("Building Charts")

st.title('Serverless X News Sentiment Analysis!')
query = st.sidebar.text_input('Enter Search Query')
today =  datetime.datetime.today().date()
duration = st.sidebar.radio("How many days of data you want to analyze?",("5 days","10 days","30 days","Custom"))
if duration == "Custom":
    start_date = st.sidebar.date_input("Enter Query start date")
    end_date = st.sidebar.date_input("Enter Query end date")

    

run_query = st.sidebar.button('Run Query')
cross_check = st.sidebar.checkbox("Find a Cross Relation")
if query == '':
    st.warning("Enter a Value")
else:
    if run_query:
        if duration == "5 days":
            today =  datetime.datetime.today().date()
            days5 =today-datetime.timedelta(days=5)
            prog(query,days5,today)
            df = seq1(query,days5,today)
        elif duration == "10 days":
            today =  datetime.datetime.today().date()
            days10 =today-datetime.timedelta(days=10)
            prog(query,days10,today)
            df = seq1(query,days10,today)
        elif duration == "30 days":
            today =  datetime.datetime.today().date()
            days30 =today-datetime.timedelta(days=30)
            prog(query,days30,today)
            df = seq1(query,days30,today)
        elif duration == "Custom":
            if start_date > today  or end_date > today:
                st.warning("This app cannot predict the future......yet")
            else:
                prog(query,start_date,end_date)
                df = seq1(query,start_date,end_date)
        try:
            plt.figure(figsize = (12,12))
            plt.subplot(221)
            plt.plot(df['DATE'], df['AVERAGEMS'], color = 'g')
            plt.xticks(df['DATE'],rotation=90)
            plt.xlabel("Date")
            plt.ylabel("SENTIMENT")
            plt.legend(['SENTIMENT'])
            df1 = seq2(query)
            plt.subplot(222)
            plt.bar(df1['CATEGORY'], df1['AVERAGEMS'])
            plt.xticks(df1['CATEGORY'],rotation=90)
            plt.xlabel("CATEGORY")
            plt.ylabel("Average")
            df2 = seq3(query)
            plt.subplot(223)
            plt.bar(df2['CATEGORY'], df2['COUNT'])
            plt.xticks(df2['CATEGORY'],rotation=90)
            plt.xlabel("CATEGORY")
            plt.ylabel("COUNT")
            st.pyplot()
        except:
            print("Restart")
if cross_check:
    cross = st.sidebar.text_input("Enter a Query To Correlate")
    cross_bt = st.sidebar.button("Run Cross Query")
    if cross_bt:
        if cross == "":
            st.warning("Enter a cross query")
        else:
            print("button")
            if duration == "5 days":
                print("5days")
                today =  datetime.datetime.today().date()
                days5 =today-datetime.timedelta(days=5)  
                df3 = seq4(query,days5,today,cross)
            elif duration == "10 days":
                today =  datetime.datetime.today().date()
                days10 =today-datetime.timedelta(days=10)   
                df3 = seq4(query,days10,today,cross)
            elif duration == "30 days":
                today =  datetime.datetime.today().date()
                days30 =today-datetime.timedelta(days=30)
                df3 = seq4(query,days30,today,cross)
            elif duration == "Custom":
                df3 = seq4(query,start_date,end_date,cross)
            plt.bar(df3['CATEGORY'], df3['COUNT'])
            plt.xticks(df3['CATEGORY'],rotation=90)
            plt.xlabel("CATEGORY")
            plt.ylabel("SENTIMENT")
            st.pyplot()
        

