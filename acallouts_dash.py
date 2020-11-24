import sys
import pandas as pd
import numpy as np
import xlwings as xw
import os

#open excel file
bms = (r'D:\git_stuff\Development\ACallouts\sources.csv')
# bms2 = (r'D:\git_stuff\Development\ACallouts\sources.xlsx')
# print(bms)
# bmss = xw.Book(bms)
# combi = bmss.sheets['Sheet1']

# dfxl = pd.read_excel(bms2, sheet_name="Sheet1", engine="openpyxl")
df = pd.read_csv(bms)

df.columns
df.describe()
df.groupby()

# this calculates the csat percentage. it will calculate dataframes and series as well.
def csat_Calc(x,y):
    num = x
    den = y
    res = (num/den)*100
    return round(res, 1)

def ttc_calc(x,y):
    num = x
    den = y
    res = (num/den)
    return round(res, 1)

# this is the way to declare it
# csatp = csat_Calc(df['CSAT_NUM_PRO'], df['CSAT_DENOM_PRO'])

# this assigns the calculated metrics to the dataframe under a new column title
CSAT_Pro = csat_Calc(df['CSAT_NUM_PRO'], df['CSAT_DENOM_PRO'])
CSAT_Basic = csat_Calc(df['CSAT_NUM_BASIC'], df['CSAT_DENOM_BASIC'])
CSAT = csat_Calc(df['CSAT_NUM'], df['CSAT_DENOM'])
DSAT_PRO = csat_Calc(df['DSAT_NUM_PRO'], df['DSAT_DENOM_PRO'])
DSAT_BASIC = csat_Calc(df['DSAT_NUM_BASIC'], df['DSAT_DENOM_BASIC'])
DSAT = csat_Calc(df['DSAT_NUM'], df['DSAT_DENOM'])
OBL = csat_Calc(df['Backlog_NUM'], df['Backlog_DENOM'])
TTC = ttc_calc(df['TTC_NUM'], df['TTC_DENOM'])

df2 = df.assign(CSAT_Pro=CSAT_Pro,CSAT_Basic=CSAT_Basic,CSAT=CSAT,DSAT_PRO=DSAT_PRO,DSAT_BASIC=DSAT_BASIC, DSAT=DSAT, OBL=OBL, TTC=round(TTC, 1), counts=1)
uniqueweeks = df2['Fiscal_Week'].unique()
latestweek = uniqueweeks.max()

df2.to_csv(r'D:\Tutorials_Trainings_Learning\Python_Learning\Python\plotly_dash\test2.csv')

os.getcwd()
