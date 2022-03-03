#!/usr/bin/env python
# coding: utf-8

# In[313]:


import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
from pathlib import Path
import arrow
import os, time, sys
import datetime
import schedule
import time
import pymysql
import config
from styleframe import StyleFrame, Styler, utils
import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st  # pip install streamlit
import plotly.figure_factory as ff
from plotly.colors import n_colors
import numpy as np
import plotly.io as pio
import mysql.connector
# In[314]:


sys.path.append('..')
import sys


# In[315]:



# In[316]:


mydb=sqlalchemy.create_engine("mysql+pymysql://Guntur_Sada_Siva:Guntur_Sada_Siva@192.168.45.19")
    


# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/

# In[317]:


st.set_page_config(page_title="Everwell Dashboard", page_icon=":bar_chart:", layout="wide")


# ---- READ Data----

# In[318]:


q1='''select * from 1097_db_iemr.t_everwellapi as api 
inner join 1097_db_iemr.t_everwellfeedback as fb on fb.EAPIID=api.EAPIID
where api.CreatedDate between date_format(subdate( now(),interval 1 week),'%%Y-%%m-%%d 00:00:00') and 
date_format(subdate( now(),interval 1 day),'%%Y-%%m-%%d 23:59:59');'''


# In[319]:


data = pd.read_sql(q1,mydb)


# In[320]:


q9='''select distinct b.ReceivedAgentID, b.CreatedBy from
(select Bencallid from
1097_db_iemr.t_everwellapi
group by Bencallid) as a
inner join 1097_db_iemr.t_bencall as b on a.Bencallid = b.BenCallID
where b.CreatedDate between date_format(subdate( now(),interval 1 week),'%%Y-%%m-%%d 00:00:00') and 
date_format(subdate( now(),interval 1 day),'%%Y-%%m-%%d 23:59:59');'''


# In[321]:


df10 =pd.read_sql(q9,mydb)


# In[322]:


q8='''select Language, count(distinct userid) as 'Agents_Count' from 1097_db_iemr.t_everwellapi
where createddate between date_format(subdate( now(),interval 1 week),'%%Y-%%m-01 00:00:00') and date_format(subdate( now(),interval 1 day),'%%Y-%%m-%%d 23:59:59')
and retryNeeded is true and isAllocated is true and userid is not null
group by Language;'''


# In[323]:


df8 =pd.read_sql(q8,mydb)


# In[324]:


q2='''select api.EverWellID,max(fb.LastModDate) as LastModDate,fb.SubCategory,fb.Comments from 1097_db_iemr.t_everwellapi as api 
inner join 1097_db_iemr.t_everwellfeedback as fb on fb.EAPIID=api.EAPIID
where (api.CreatedDate between date_format(subdate( now(),interval 1 week),'%%Y-%%m-%%d 00:00:00') and date_format(subdate( now(),interval 1 day),'%%Y-%%m-%%d 23:59:59'))
group by EverWellID;'''


# In[325]:


data2 =pd.read_sql(q2,mydb)


# In[326]:


data2.loc[(data2['SubCategory'] == 'Dose not taken'), 'CallType'] = 'Responded'
data2.loc[(data2['SubCategory'] == 'Dose taken but not reported by technology'), 'CallType'] = 'Responded'
data2.loc[(data2['SubCategory'] == 'Called & Counselled'), 'CallType'] = 'Responded'
data2.loc[(data2['SubCategory'] == 'Others'), 'CallType'] = 'Others'
data2.loc[(data2['SubCategory'] == 'Phone switched off'), 'CallType'] = 'Others'
data2.loc[(data2['SubCategory'] == 'Did not receive the call'), 'CallType'] = 'Not Responded'
data2.loc[(data2['SubCategory'] == 'Phone not reachable'), 'CallType'] = 'Others'
data2.loc[(data2['SubCategory'] == 'Wrong Phone number'), 'CallType'] = 'Others'
data2.loc[(data2['SubCategory'] == 'Do not disturb for today'), 'CallType'] = 'Others'


# In[327]:


q4='''select Language, count(*) as cnt from 1097_db_iemr.t_everwellapi
where createddate between date_format(subdate( now(),interval 1 week),'%%Y-%%m-%%d 00:00:00') and date_format(subdate( now(),interval 1 day),'%%Y-%%m-%%d 23:59:59')
and isAllocated is true and userid is not null and bencallid is not null
group by Language;'''


# In[328]:


df4 =pd.read_sql(q4,mydb)


# In[329]:


q5='''select avg(b.CZcallDuration) as avg_call_duration from
(select Bencallid from
1097_db_iemr.t_everwellapi
group by Bencallid) as a
inner join 1097_db_iemr.t_bencall as b on a.Bencallid = b.BenCallID
where b.CreatedDate between date_format(subdate( now(),interval 1 week),'%%Y-%%m-%%d 00:00:00') and 
date_format(subdate( now(),interval 1 day),'%%Y-%%m-%%d 23:59:59');'''


# In[330]:


df5 =pd.read_sql(q5,mydb)


# In[331]:


q6='''select count(distinct userid) from 1097_db_iemr.t_everwellapi
where createddate between date_format(subdate( now(),interval 1 week),'%%Y-%%m-01 00:00:00') and date_format(subdate( now(),interval 1 day),'%%Y-%%m-%%d 23:59:59')
and retryNeeded is true and isAllocated is true and userid is not null;'''


# In[332]:


df6 =pd.read_sql(q6,mydb)


# In[333]:


q7='''select SubCategory as 'Call_Outcome', count(SubCategory) as Count
from 1097_db_iemr.t_everwellfeedback
where CreatedDate between date_format(subdate( now(),interval 1 week),'%%Y-%%m-%%d 00:00:00') and date_format(subdate( now(),interval 1 day),'%%Y-%%m-%%d 23:59:59')
and Category='Support_Action_Call' and SubCategory is not null
group by SubCategory;'''


# In[334]:


df7 =pd.read_sql(q7,mydb)


# In[335]:


q10='''select Language, count(distinct userid) as 'Agents_Count' from 1097_db_iemr.t_everwellapi
where createddate between date_format(subdate( now(),interval 1 week),'%%Y-%%m-01 00:00:00') and date_format(subdate( now(),interval 1 day),'%%Y-%%m-%%d 23:59:59')
and retryNeeded is false and isAllocated is true and userid is not null
group by Language;'''


# In[336]:


df11 =pd.read_sql(q10,mydb)


# In[337]:


q11='''select count(distinct userid) from 1097_db_iemr.t_everwellapi
where createddate between date_format(subdate( now(),interval 1 week),'%%Y-%%m-01 00:00:00') and date_format(subdate( now(),interval 1 day),'%%Y-%%m-%%d 23:59:59')
and retryNeeded is false and isAllocated is true and userid is not null;'''


# In[338]:


df12 =pd.read_sql(q11,mydb)


# In[339]:


df9=data2.SubCategory.value_counts().rename_axis('Action').reset_index(name='counts')


# In[340]:


q3='''call 1097_db_iemr.Pr_EverwellDailyReport(date_format(subdate( now(),interval 1 week),'%%Y-%%m-%%d 00:00:00'),date_format(subdate( now(),interval 1 day),'%%Y-%%m-%%d 23:59:59'));'''


# In[341]:


df2 =pd.read_sql_query(q3,mydb)


# In[342]:


data3=data2.query('CallType=="Responded"')
data4=data2.query('CallType=="Not Responded"')
data7=data2.query('CallType=="Others"')
Language_count=data["Language"].value_counts(normalize=True)*100


# In[343]:


ll=data.Language.unique()


# ---- MAINPAGE ----

# In[344]:


def main():
    st.title(":bar_chart: Everwell Dashboard")
    st.markdown("##")
    a=int(df2.iloc[:,0])
    b=int(df2.iloc[:,1])
    c=int(df2.iloc[:,2])
    d=int(df2.iloc[:,3])
    e=int(df2.iloc[:,4])
    f=int(df2.iloc[:,5])
    g=int(df2.iloc[:,6])
    h=int(df2.iloc[:,7])
    st1, st2, st3, st4, st5 = st.columns(5)
    with st1:
        st.title("Received Calls:")
        st.subheader(f"{a}")
    with st2:
        st.title("Allocated Calls:")
        st.subheader(f"{b}")
    with st3:
        st.title("Calls Made:")
        st.subheader(f"{d}")
    with st4:
        st.title("Calls Responded:")
        st.subheader(f"{e}")
    with st5:
        st.title("Calls Not Made:")
        st.subheader(f"{h}")
    st6, st7, st8, st9 = st.columns(4)
    with st6:
        st.title("Repeat Calls:")
        st.subheader(f"{f}")
    with st7:
        st.title("Repeat Calls Completed:")
        st.subheader(f"{g}")
    with st8:
        st.title("Average Duration of Calls:")
        st.subheader(f"{df5.iloc[0,0]} sec")
    with st9:
        st.title("Agents List:")
        st.subheader(f"{c}")
   
    st10, st11 = st.columns(2)
    with st10:
        st.title("Total No. of Agents who made SVA related re-counselling calls in the month:")
        st.subheader(f"{df6.iloc[0,0]}")
    with st11:
        st.title("Total No. of Agents who made SVA related Counselling calls in the month:")
        st.subheader(f"{df12.iloc[0,0]}")
    
    rowEvenColor = 'rgb(49, 130, 189)'
    rowOddColor = 'rgb(107, 174, 214)'
    fig19 = go.Figure(data=[go.Table(
    header=dict(
    values=['<b>Language</b>', '<b>Count</b>'],
    line_color='blue', fill_color='black',
    align=['center', 'center'],font=dict(color='white', size=12)
       ),
     cells=dict(
    values=[df4.Language, df4.cnt],
    line_color='blue',
    fill_color=[[rowOddColor,rowEvenColor,rowOddColor, rowEvenColor,rowOddColor]*3],
    align=['center', 'center'], font=dict(color='Black', size=10)
    ))
         ])
    fig22 = go.Figure(data=[go.Table(
     header=dict(
    values=['<b>Call Outcome</b>', '<b>Count</b>'],
    line_color='white', fill_color='black',
    align=['center', 'center'],font=dict(color='white', size=12)
                  ),
     cells=dict(
    values=[df7.Call_Outcome, df7.Count],
    line_color='white',
    fill_color=['rgb(255, 200, 200)','rgb(200, 0, 0)'],
    align=['center', 'center'], font=dict(color='black', size=10)
    ))
           ])
    fig23 = go.Figure(data=[go.Table(header=dict(values=['<b>Language</b>', '<b>Agents Count</b>'],
                            line_color='white', fill_color='black',
                                    align=['center', 'center'],font=dict(color='white', size=12)),
           cells=dict(
                   values=[df8.Language, df8.Agents_Count],
                    line_color='white',
                            fill_color=['rgb(30,144,255)','rgb(175,238,238)'],
                          align=['center', 'center'], font=dict(color='black', size=10)))])
    fig24 = go.Figure(data=[go.Table(
     header=dict(
    values=['<b>Support Action</b>', '<b>Count</b>'],
    line_color='white', fill_color='black',
    align=['center', 'center'],font=dict(color='white', size=12)
          ),
    cells=dict(
    values=[df9.Action, df9.counts],
    line_color='white',
    fill_color=['rgb(123,104,238)','rgb(176,196,222)'],
    align=['center', 'center'], font=dict(color='black', size=10)
    ))
             ])
    fig25 = go.Figure(data=[go.Table(
    header=dict(
    values=['<b>Language</b>', '<b>Agents Count</b>'],
    line_color='white', fill_color='black',
    align=['center', 'center'],font=dict(color='white', size=12)
        ),
  cells=dict(
    values=[df11.Language, df11.Agents_Count],
    line_color='white',
    fill_color=['rgb(30,144,255)','rgb(175,238,238)'],
    align=['center', 'center'], font=dict(color='black', size=10)
    ))
        ])
    fig8 =px.pie(data_frame=data2,names="CallType",title='Call Types %')
    fig9 =px.pie(data_frame=data2,names="SubCategory",title='Sub Category %')
    fig10 =px.pie(data_frame=data3,names="SubCategory",title='Responded Calls')
    fig10.update_traces(textinfo='value')
    fig11 =px.pie(data_frame=data4,names="SubCategory",title='Not Responded Calls')
    fig11.update_traces(textinfo='value')
    fig13 =px.bar(data_frame=data2["SubCategory"].value_counts(normalize=True)*100,y="SubCategory",title='Sub Category %').update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
    fig13.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',})
    import datetime as dt
    data5=data2["LastModDate"].dt.date
    data6=data5.value_counts().reset_index()
    data6.columns=["Date","No of calls"]
    fig14 = px.line(data6, x="Date", y="No of calls", text="No of calls",title='Calls Day wise').update_layout(xaxis_showgrid=False, yaxis_showgrid=False,showlegend=True)
    fig14.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',})
    fig12 = px.pie(data_frame=data,names="Language",title='Language %')
          #plt.pie(Language_count,labels=ll) 
    data8=data7["SubCategory"].value_counts().reset_index()
    data8.columns=["Comments","Count"]
    fig15 = px.bar(data8, x="Count", y="Comments", orientation='h',title='Top comments when Others are selected').update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
    fig15.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',})
    fig8.update_layout(autosize=False,width=700, height=390,paper_bgcolor="Black",font = {'color': "White"})
    fig9.update_layout(autosize=False,width=700, height=390,paper_bgcolor="Black",font = {'color': "White"})
   #fig9.update_layout(autosize=False,width=500, height=300,margin=dict(l=0, r=200, t=0, b=20), paper_bgcolor="Black",font = {'color': "White"})
    fig10.update_layout(autosize=True,width=700, height=390,paper_bgcolor="Black",font = {'color': "White"})
    fig12.update_layout(autosize=True,width=700, height=390,paper_bgcolor="Black",font = {'color': "White"})
    fig13.update_layout(autosize=True,width=1400, height=590,paper_bgcolor="Black",font = {'color': "White"})
    fig14.update_layout(autosize=True,width=820, height=390,paper_bgcolor="Black",font = {'color': "White"})
    fig15.update_layout(autosize=True,width=570, height=390,paper_bgcolor="Black",font = {'color': "White"})
    fig19.update_layout(autosize=True,width=700, height=390,paper_bgcolor="Black",font = {'color': "White"},title='Language Break-Up')
    fig22.update_layout(autosize=True,width=700, height=390,paper_bgcolor="Black",font = {'color': "White"},title='Call Outcome Analysis Over Support Actions Marked')
    fig23.update_layout(autosize=True,width=700, height=390,paper_bgcolor="Black",font = {'color': "White"},title='Agents who made SVA related re-counselling calls of month')
    fig24.update_layout(autosize=True,width=700, height=390,paper_bgcolor="Black",font = {'color': "White"},title='Most Number of Support Actions marked by PSMRI')
    fig25.update_layout(autosize=True,width=700, height=390,paper_bgcolor="Black",font = {'color': "White"},title='Agents who made SVA related counselling calls of month')
    left_column, right_column = st.columns(2)
    left_column.plotly_chart(fig23, use_container_width=True)
    right_column.plotly_chart(fig25, use_container_width=True)
    left_column, right_column = st.columns(2)
    left_column.plotly_chart(fig19, use_container_width=True)
    right_column.plotly_chart(fig22, use_container_width=True)
    left_column, right_column = st.columns(2)
    left_column.plotly_chart(fig8, use_container_width=True)
    right_column.plotly_chart(fig9, use_container_width=True)
    left_column, right_column = st.columns(2)
    left_column.plotly_chart(fig10, use_container_width=True)
    right_column.plotly_chart(fig12, use_container_width=True)
    st.plotly_chart(fig13, use_container_width=True)
    left_column, right_column = st.columns(2)
    left_column.plotly_chart(fig14, use_container_width=True)
    right_column.plotly_chart(fig15, use_container_width=True)


# In[345]:


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


# In[346]:


if __name__ == '__main__':
   main()


# In[ ]:




