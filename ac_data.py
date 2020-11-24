import pandas as pd
import numpy as np
import sys
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

# os.getcwd()

#data import section
data = (r'D:\git_stuff\Development\ACallouts\sources.csv')
df=pd.read_csv(data)

# extract required information like latest week and column names etc
colnames = df.columns
index = df.index
latestweek = df['Fiscal_Week'].max()
prevnbr = int(latestweek[-2:])-1
prevweek = latestweek.replace(latestweek[-2:], str(prevnbr))
uniqueweeks = df['Fiscal_Week'].unique()
# add more unique columns here if required
# only numeric columns
ncols = ['EOQ_FLAG', 'China_Flag', 'CSAT_NUM','CSAT_DENOM', 'RDR_NUM', 'RDR_DENOM', 'TTC_NUM', 'TTC_DENOM','Backlog_NUM', 'Backlog_DENOM', 'DSAT_NUM', 'DSAT_DENOM', 'TTR_NUM','TTR_DENOM', 'PI_NUM', 'PI_DENOM', 'OTS_NUM', 'OTS_DENOM', 'SL_NUM','SL_DENOM', 'AHT_NUM', 'AHT_DENOM', 'CSAT_NUM_PRO', 'CSAT_DENOM_PRO','CSAT_NUM_BASIC', 'CSAT_DENOM_BASIC', 'DSAT_NUM_PRO', 'DSAT_DENOM_PRO','DSAT_NUM_BASIC', 'DSAT_DENOM_BASIC', 'PLAN_NUM', 'PLAN_DENOM','SEV1_SLO_NUM', 'SEV1_SLO_DENOM', 'AOP_NUM', 'AOP_DENOM']
colnames

# latest week subset
# use this df to create graphs which are related only to the latest week
# like region compare product compare etc, they can be substets of this.
# a sequence of boolean series
criteria = df['Fiscal_Week'] == latestweek
df_lw = df.loc[df['Fiscal_Week'] == latestweek, ncols]
df_lw.head()


# make a subset for only Fiscal week column and the CSAT columns to display in a visual
ce_week = df.groupby('Fiscal_Week')[['CSAT_NUM', 'CSAT_DENOM']].sum()
ce_week['CSAT'] = round(ce_week['CSAT_NUM']/ce_week['CSAT_DENOM']*100, 2)
