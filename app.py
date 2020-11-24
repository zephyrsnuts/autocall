import sys
import re
import csv
from datetime import datetime
import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objs as go
from dash.dependencies import Input, Output

# define app for graphs
app = dash.Dash(__name__)

#data import section
data = (r'D:\git_stuff\Development\ACallouts\sources.csv')
dforiginal=pd.read_csv(data, keep_default_na=False, float_precision=2)
df = dforiginal.replace({'DPD/UDS': 'DPD_UDS', 'Primary Storage': 'Primary_Storage', 'HCI & Cloud': 'HCI_Cloud'})
outfile = r'D:\git_stuff\Development\ACallouts\output.txt'
with open(outfile, 'r+') as f:
    f.truncate(0)

# for julie to look at this and understand where she needs to point fingers at.

# extract required information like latest week and column names etc
colnames = df.columns
index = df.index
latestweek = df['Fiscal_Week'].max()
prevnbr = int(latestweek[-2:])-1
prevweek = latestweek.replace(latestweek[-2:], str(prevnbr))
pprevnbr = int(latestweek[-2:])-2
pprevweek = latestweek.replace(latestweek[-2:], str(pprevnbr))
latestquarter = df['Fiscal_Quarter'].max()
prevqnbr = int(latestquarter[-1:])-1
prevquarter = latestquarter.replace(latestquarter[-1:], str(prevqnbr))
latestyear = df['Fiscal_Year'].max()
latestyear
prevynbr = int(latestyear[3:4])-1
prevyear = latestyear.replace(latestyear[3:4], str(prevynbr))
uniqueweeks = df['Fiscal_Week'].unique()
ncols = ['EOQ_FLAG', 'China_Flag', 'CSAT_NUM','CSAT_DENOM', 'RDR_NUM', 'RDR_DENOM', 'TTC_NUM', 'TTC_DENOM','Backlog_NUM', 'Backlog_DENOM', 'DSAT_NUM', 'DSAT_DENOM', 'TTR_NUM','TTR_DENOM', 'PI_NUM', 'PI_DENOM', 'OTS_NUM', 'OTS_DENOM', 'SL_NUM','SL_DENOM', 'AHT_NUM', 'AHT_DENOM', 'CSAT_NUM_PRO', 'CSAT_DENOM_PRO','CSAT_NUM_BASIC', 'CSAT_DENOM_BASIC', 'DSAT_NUM_PRO', 'DSAT_DENOM_PRO','DSAT_NUM_BASIC', 'DSAT_DENOM_BASIC', 'PLAN_NUM', 'PLAN_DENOM','SEV1_SLO_NUM', 'SEV1_SLO_DENOM', 'AOP_NUM', 'AOP_DENOM']

# latest week subset
# df_lw = df.loc[df['Fiscal_Week'] == latestweek]
# df_lw.head()
df[ncols] = df[ncols].apply(pd.to_numeric, downcast='unsigned')
df1 = df.loc[df['Fiscal_Week_Lag']>= -13,:]

# df1['Agent Region'].unique()
# df1['Agent Region'] = np.where(df1['Agent Region'] == 'North America', 'Agent Region'] ='NA'
# df1['Agent Region'] = np.where((df1['Agent Region'] == 'Latin America') | (df1['Agent Region'] == 'LATIN AMERICA'), 'LA', df1['Agent Region'])

#test area
# df['BMS_Region'].unique()
# df_int = df.loc[:,ncols]
# dfn = df_int.apply(pd.to_numeric, downcast='unsigned')
#
# df['Product_Group'].unique()

# df['OBL'] = df['Backlog_NUM']/df['Backlog_DENOM']

# title = str(ncols[2]).partition("_")[0]
# #test area

# creating subsets i will most likely use pivots to create the subsets so that i can get the output i want
# table = pd.pivot_table(df1, values = ['Backlog_NUM','Backlog_DENOM'], columns = ['Fiscal_Week'], index = ['BMS_Product','BMS_Region'], aggfunc={'Backlog_NUM':np.sum, 'Backlog_DENOM':np.sum}, margins=True)
#
# tab_tots = table.groupby(level = 'BMS_Product').sum()
# tab_tots.index = [tab_tots.index, ['Total']*len(tab_tots)]
#
# tab_tots
#
# pd.concat(
# [table, tab_tots]
# ).sort_index().append(table.sum().rename(('Grand', 'Total')))
#
# REVIEW: #---------------------------------
# The following concatenates the sum of the multiindex table at level 0 which is product
# rename is basically rename((index level 0, index level 1)) this is a tuple
# rename normally is intex, column which is the same in this case as 'Total' would be the column
# this was originally
# d.append(d.sum().rename((k, 'Total')))
# for k, d in table.groupby(level = 0)
#
# i didnt want it saying 'Total' hence i changed it to reflect the index name at level 0
#
# pd.concat([
# d.append(d.sum().rename((k, k)))
# for k, d in table.groupby(level = 0)
# ])
#
# here k seems to be the index, and d seems to be the columns with the table i dont know how this works.
# for k, d in table.groupby(level = 0):
#     print(d)

# .append(table.sum().rename(('Grand', 'Total'))) # this last append is to just append the grand total row

# newtable = round(table['Backlog_NUM']/table['Backlog_DENOM']*100, 1)
# newtable

def pivoted(x, list, list2, list3):
    agre = list[0]
    agre2 = list[1]
    title = str(list[0]).partition("_")[0]
    print(title)
    table = pd.pivot_table(x, values = list, columns = list2, index = list3, aggfunc={agre:np.sum, agre2:np.sum}, margins=True, margins_name='OVERALL')

    subtable = pd.concat([
    d.append(d.sum().rename((k, k)))
    for k, d in table.groupby(level = 0)
    ])
    #.append(table.sum().rename(('Grand', 'Total')))
    # removed this part since i have the margins=True column included, this just adds the grand total to the table

    newtable = round(subtable[agre]/subtable[agre2]*100, 1)
    newtable = newtable.replace(np.nan, 0.0)
    newtable = newtable.sort_index(ascending = False)
    return newtable

def pivoted_np(x, list, list2, list3):
    agre = list[0]
    agre2 = list[1]
    table = pd.pivot_table(x, values = list, columns = list2, index = list3, aggfunc={agre:np.sum, agre2:np.sum}, margins=True, margins_name='OVERALL')

    subtable = pd.concat([
    d.append(d.sum().rename((k, k)))
    for k, d in table.groupby(level = 0)
    ])
    #.append(table.sum().rename(('Grand', 'Total')))
    # removed this part since i have the margins=True column included, this just adds the grand total to the table

    newtable = round(subtable[agre]/subtable[agre2], 1)
    newtable = newtable.replace(np.nan, 0.0)
    newtable = newtable.sort_index(ascending = False)
    return newtable

# create varibles for list of items so that i dont have to type it in everytime
prod_region = ['BMS_Product','BMS_Region']
weeks = ['Fiscal_Week']
prod = ['BMS_Product']
quarter = ['Fiscal_Quarter']
year = ['Fiscal_Year']
obl = [ncols[8], ncols[9]]
cs = [ncols[2], ncols[3]]
ds = [ncols[10], ncols[11]]
rdr = [ncols[4], ncols[5]]
ttc = [ncols[6], ncols[7]]
ttr = [ncols[12], ncols[13]]
pi = [ncols[14], ncols[15]]
ots = [ncols[16], ncols[17]]
sl = [ncols[18], ncols[19]]
aht = [ncols[20], ncols[21]]
csp = [ncols[22], ncols[23]]
csb = [ncols[24], ncols[25]]
dsp = [ncols[26], ncols[27]]
dsb = [ncols[28], ncols[29]]
pl = [ncols[30], ncols[31]]
slo = [ncols[32], ncols[33]]
aop = [ncols[34], ncols[35]]

# format to enter the data is (dataframe, values, columns, index)
#weeks
cs_table = pivoted(df1, cs, weeks, prod_region)
ds_table = pivoted(df1, ds, weeks, prod_region)
obl_table = pivoted(df1, obl, weeks, prod_region)
rdr_table = pivoted(df1, rdr, weeks, prod_region)
ttc_table = pivoted_np(df1, ttc, weeks, prod_region)
ttr_table = pivoted_np(df1, ttr, weeks, prod_region)
pi_table = pivoted_np(df1, pi, weeks, prod_region)
ots_table = pivoted(df1, ots, weeks, prod_region)
sl_table = pivoted(df1, sl, weeks, prod_region)
aht_table = pivoted_np(df1, aht, weeks, prod_region)
csp_table = pivoted(df1, csp, weeks, prod_region)
csb_table = pivoted(df1, csb, weeks, prod_region)
dsp_table = pivoted(df1, dsp, weeks, prod_region)
dsb_table = pivoted(df1, dsb, weeks, prod_region)
pl_table = pivoted_np(df1, pl, weeks, prod_region)
slo_table = pivoted(df1, slo, weeks, prod_region)
aop_table = pivoted_np(df1, aop, weeks, prod_region)

#quarters
cs_table_q = pivoted(df, cs, quarter, prod_region)
ds_table_q = pivoted(df, ds, quarter, prod_region)
obl_table_q = pivoted(df, obl, quarter, prod_region)
rdr_table_q = pivoted(df, rdr, quarter, prod_region)
ttc_table_q = pivoted_np(df, ttc, quarter, prod_region)
ttr_table_q = pivoted_np(df, ttr, quarter, prod_region)
pi_table_q = pivoted_np(df, pi, quarter, prod_region)
ots_table_q = pivoted(df, ots, quarter, prod_region)
sl_table_q = pivoted(df, sl, quarter, prod_region)
aht_table_q = pivoted_np(df, aht, quarter, prod_region)
csp_table_q = pivoted(df, csp, quarter, prod_region)
csb_table_q = pivoted(df, csb, quarter, prod_region)
dsp_table_q = pivoted(df, dsp, quarter, prod_region)
dsb_table_q = pivoted(df, dsb, quarter, prod_region)
pl_table_q = pivoted_np(df, pl, quarter, prod_region)
slo_table_q = pivoted(df, slo, quarter, prod_region)
aop_table_q = pivoted_np(df, aop, quarter, prod_region)

# year
cs_table_y = pivoted(df, cs, year, prod_region)
ds_table_y = pivoted(df, ds, year, prod_region)
obl_table_y = pivoted(df, obl, year, prod_region)
rdr_table_y = pivoted(df, rdr, year, prod_region)
ttc_table_y = pivoted_np(df, ttc, year, prod_region)
ttr_table_y = pivoted_np(df, ttr, year, prod_region)
pi_table_y = pivoted_np(df, pi, year, prod_region)
ots_table_y = pivoted(df, ots, year, prod_region)
sl_table_y = pivoted(df, sl, year, prod_region)
aht_table_y = pivoted_np(df, aht, year, prod_region)
csp_table_y = pivoted(df, csp, year, prod_region)
csb_table_y = pivoted(df, csb, year, prod_region)
dsp_table_y = pivoted(df, dsp, year, prod_region)
dsb_table_y = pivoted(df, dsb, year, prod_region)
pl_table_y = pivoted_np(df, pl, year, prod_region)
slo_table_y = pivoted(df, slo, year, prod_region)
aop_table_y = pivoted_np(df, aop, year, prod_region)
# FINAL PIVOTED DATA IS AVAILABLE FROM HERE

# original way i did it.
# lwdata = obl_table.iloc[:,12].astype(float)
# pwdata = obl_table.iloc[:,11].astype(float)
# differences = lwdata-pwdata
# obl2 = obl_table.assign(pweek_diff = differences)

# define function to add the additional columns to the data so that it can be used on multiple metrics
# weekly
def add_cols(metric_table):
    diff_table = metric_table
    #ALTERNATE WAY
    diffs = diff_table.diff(axis=1)[latestweek]
    # obl2 = diff_table.index.get_level_values(1)
    obl2 = diff_table[[prevweek,latestweek]]
    updown = np.where((obl2[latestweek].values < obl2[prevweek].values), "Down", 'Up')
    obl22 = obl2.assign(direction = updown)
    obl3 = obl22.assign(pweekdiff = diffs)

    m = diff_table.iloc[:,12]
    m2 = diff_table.iloc[:,11]
    m3 = diff_table.iloc[:,10]
    m4 = diff_table.iloc[:,9]
    m5 = diff_table.iloc[:,8]
    m6 = diff_table.iloc[:,7]

    calc3 = m-m3
    calc4 = m-m4
    calc5 = m-m5
    calc6 = m-m6

    wk3 = np.where(((m<m2)&(m2<m3)), calc3, 0.0)
    wk3u = np.where(((m>m2)&(m2>m3)), calc3, 0.0)
    wk4 = np.where(((m<m2)&(m2<m3)&(m3<m4)), calc4, 0.0)
    wk4u = np.where(((m>m2)&(m2>m3)&(m3>m4)), calc4, 0.0)
    wk5 = np.where(((m<m2)&(m2<m3)&(m3<m4)&(m4<m5)), calc5, 0.0)
    wk5u = np.where(((m>m2)&(m2>m3)&(m3>m4)&(m4>m5)), calc5, 0.0)
    wk6 = np.where(((m<m2)&(m2<m3)&(m3<m4)&(m4<m5)&(m5<m6)), calc6, 0.0)
    wk6u = np.where(((m>m2)&(m2>m3)&(m3>m4)&(m4>m5)&(m5>m6)), calc6, 0.0)

    diff_table1 = obl3.assign(trendd3= wk3, trendu3 = wk3u, trendd4= wk4, trendu4= wk4u, trendd5= wk5, trendu5=wk5u, trendd6= wk6, trendu6= wk6u)
    diff_table2 = diff_table1.assign(latestweekdata = diffs)
    diff_table3 = diff_table2.assign(at = "at")
    diff_table4 = diff_table3.assign(weekname = latestweek[5:8])
    return diff_table4

def add_cols_rdr(metric_table):
    diff_table = metric_table
    #ALTERNATE WAY
    diffs = diff_table.diff(axis=1)[prevweek]
    # obl2 = diff_table.index.get_level_values(1)
    obl2 = diff_table[[pprevweek,prevweek]]
    updown = np.where((obl2[prevweek].values < obl2[pprevweek].values), "Down", 'Up')
    obl22 = obl2.assign(direction = updown)
    obl3 = obl22.assign(pweekdiff = diffs)

    m = diff_table.iloc[:,12]
    m2 = diff_table.iloc[:,11]
    m3 = diff_table.iloc[:,10]
    m4 = diff_table.iloc[:,9]
    m5 = diff_table.iloc[:,8]
    m6 = diff_table.iloc[:,7]

    calc3 = m-m3
    calc4 = m-m4
    calc5 = m-m5
    calc6 = m-m6

    wk3 = np.where(((m<m2)&(m2<m3)), calc3, 0.0)
    wk3u = np.where(((m>m2)&(m2>m3)), calc3, 0.0)
    wk4 = np.where(((m<m2)&(m2<m3)&(m3<m4)), calc4, 0.0)
    wk4u = np.where(((m>m2)&(m2>m3)&(m3>m4)), calc4, 0.0)
    wk5 = np.where(((m<m2)&(m2<m3)&(m3<m4)&(m4<m5)), calc5, 0.0)
    wk5u = np.where(((m>m2)&(m2>m3)&(m3>m4)&(m4>m5)), calc5, 0.0)
    wk6 = np.where(((m<m2)&(m2<m3)&(m3<m4)&(m4<m5)&(m5<m6)), calc6, 0.0)
    wk6u = np.where(((m>m2)&(m2>m3)&(m3>m4)&(m4>m5)&(m5>m6)), calc6, 0.0)

    diff_table1 = obl3.assign(trendd3= wk3, trendu3 = wk3u, trendd4= wk4, trendu4= wk4u, trendd5= wk5, trendu5=wk5u, trendd6= wk6, trendu6= wk6u)
    diff_table2 = diff_table1.assign(latestweekdata = diffs)
    diff_table3 = diff_table2.assign(at = "at")
    diff_table4 = diff_table3.assign(weekname = prevweek[5:8])
    return diff_table4

# quarterly
def add_cols_q(metric_table):
    diff_table = metric_table
    #ALTERNATE WAY
    diffs = diff_table.diff(axis=1)[latestquarter]
    # obl2 = diff_table.index.get_level_values(1)
    obl2 = diff_table[[prevquarter,latestquarter]]
    updown = np.where((obl2[latestquarter].values < obl2[prevquarter].values), "Down", 'Up')
    obl22 = obl2.assign(direction = updown)
    obl3 = obl22.assign(pweekdiff = diffs)

    m = diff_table.iloc[:,5]
    m2 = diff_table.iloc[:,4]
    m3 = diff_table.iloc[:,3]
    m4 = diff_table.iloc[:,2]
    m5 = diff_table.iloc[:,1]
    m6 = diff_table.iloc[:,0]

    calc3 = m-m3
    calc4 = m-m4
    calc5 = m-m5
    calc6 = m-m6

    wk3 = np.where(((m<m2)&(m2<m3)), calc3, 0.0)
    wk3u = np.where(((m>m2)&(m2>m3)), calc3, 0.0)
    wk4 = np.where(((m<m2)&(m2<m3)&(m3<m4)), calc4, 0.0)
    wk4u = np.where(((m>m2)&(m2>m3)&(m3>m4)), calc4, 0.0)
    wk5 = np.where(((m<m2)&(m2<m3)&(m3<m4)&(m4<m5)), calc5, 0.0)
    wk5u = np.where(((m>m2)&(m2>m3)&(m3>m4)&(m4>m5)), calc5, 0.0)
    wk6 = np.where(((m<m2)&(m2<m3)&(m3<m4)&(m4<m5)&(m5<m6)), calc6, 0.0)
    wk6u = np.where(((m>m2)&(m2>m3)&(m3>m4)&(m4>m5)&(m5>m6)), calc6, 0.0)

    diff_table1 = obl3.assign(trendd3= wk3, trendu3 = wk3u, trendd4= wk4, trendu4= wk4u, trendd5= wk5, trendu5=wk5u, trendd6= wk6, trendu6= wk6u)
    diff_table2 = diff_table1.assign(latestweekdata = diffs)
    diff_table3 = diff_table2.assign(at = "at")
    diff_table4 = diff_table3.assign(weekname = latestquarter[5:8])
    return diff_table4

# yearly
def add_cols_y(metric_table):
    diff_table = metric_table
    #ALTERNATE WAY
    diffs = diff_table.diff(axis=1)[latestyear]
    # obl2 = diff_table.index.get_level_values(1)
    obl2 = diff_table[[prevyear,latestyear]]
    updown = np.where((obl2[latestyear].values < obl2[prevyear].values), "Down", 'Up')
    obl22 = obl2.assign(direction = updown)
    obl3 = obl22.assign(pweekdiff = diffs)

    diff_table4 = obl3.assign(weekname = latestyear[0:4])
    return diff_table4

# WEEKLY === ADDING THE COLUMNS
oblz = add_cols(obl_table)
uniqueprods = oblz.index.get_level_values(level = 0).unique()
up2 = list(uniqueprods)

csz = add_cols(cs_table)
dsz = add_cols(ds_table)
rdrz = add_cols_rdr(rdr_table)
ttcz = add_cols(ttc_table)
ttrz = add_cols(ttr_table)
piz = add_cols(pi_table)
otsz = add_cols(ots_table)
slz = add_cols(sl_table)
ahtz = add_cols(aht_table)
cspz = add_cols(csp_table)
csbz = add_cols(csb_table)
dspz = add_cols(dsp_table)
dsbz = add_cols(dsb_table)
plz = add_cols(pl_table)
sloz = add_cols(slo_table)
aopz = add_cols(aop_table)

#QUARTERLY
oblq = add_cols_q(obl_table_q)
csq = add_cols_q(cs_table_q)
dsq = add_cols_q(ds_table_q)
rdrq = add_cols_q(rdr_table_q)
ttcq = add_cols_q(ttc_table_q)
ttrq = add_cols_q(ttr_table_q)
piq = add_cols_q(pi_table_q)
otsq = add_cols_q(ots_table_q)
slq = add_cols_q(sl_table_q)
ahtq = add_cols_q(aht_table_q)
cspq = add_cols_q(csp_table_q)
csbq = add_cols_q(csb_table_q)
dspq = add_cols_q(dsp_table_q)
dsbq = add_cols_q(dsb_table_q)
plq = add_cols_q(pl_table_q)
sloq = add_cols_q(slo_table_q)
aopq = add_cols_q(aop_table_q)

#YEARLY
obly = add_cols_y(obl_table_y)
csy = add_cols_y(cs_table_y)
dsy = add_cols_y(ds_table_y)
rdry = add_cols_y(rdr_table_y)
ttcy = add_cols_y(ttc_table_y)
ttry = add_cols_y(ttr_table_y)
piy = add_cols_y(pi_table_y)
otsy = add_cols_y(ots_table_y)
sly = add_cols_y(sl_table_y)
ahty = add_cols_y(aht_table_y)
cspy = add_cols_y(csp_table_y)
csby = add_cols_y(csb_table_y)
dspy = add_cols_y(dsp_table_y)
dsby = add_cols_y(dsb_table_y)
ply = add_cols_y(pl_table_y)
sloy = add_cols_y(slo_table_y)
aopy = add_cols_y(aop_table_y)

# add a new column to the pivoted data to show highlight
# for a, b in oblz.groupby(level=1):
#     a.append(a)
#     b.append(b.sum().rename((b,b)))
#     b
#
#
# def conditional(metric_table, measure_string):
#     d = "Down"
#     m = ['CSAT', 'OTS']
#
#     np.where((oblz['direction'] == d)& , "Highlight", "Opprtunity")
# if (dir in d) and (meter in m):
#
#
# oblz

trendcsv = (r'D:\git_stuff\Development\ACallouts\year_quarter_trend.csv')
with open(trendcsv, 'w', newline = '') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["YEARLY"])
    writer.writerow([" "])
    writer.writerow(["CSAT"])
    csy.to_csv(csvfile, mode='a')
    writer.writerow([" "])
    writer.writerow(["DSAT"])
    dsy.to_csv(csvfile, mode='a')
    writer.writerow([" "])
    writer.writerow(["RDR"])
    rdry.to_csv(csvfile, mode='a')
    writer.writerow([" "])
    writer.writerow(["TTC"])
    ttcy.to_csv(csvfile, mode='a')
    writer.writerow([" "])
    writer.writerow(["TTR"])
    ttry.to_csv(csvfile, mode='a')
    writer.writerow([" "])
    writer.writerow(["PI"])
    piy.to_csv(csvfile, mode='a')
    writer.writerow([" "])
    writer.writerow(["OTS"])
    otsy.to_csv(csvfile, mode='a')
    writer.writerow([" "])
    writer.writerow(["SL"])
    sly.to_csv(csvfile, mode='a')
    writer.writerow([" "])
    writer.writerow(["AHT"])
    ahty.to_csv(csvfile, mode='a')
    writer.writerow([" "])
    writer.writerow(["CSAT-Pro"])
    cspy.to_csv(csvfile, mode='a')
    writer.writerow([" "])
    writer.writerow(["CSAT-Basic"])
    csby.to_csv(csvfile, mode='a')
    writer.writerow([" "])
    writer.writerow(["DSAT-Pro"])
    dspy.to_csv(csvfile, mode='a')
    writer.writerow([" "])
    writer.writerow(["DSAT-Basic"])
    dsby.to_csv(csvfile, mode='a')
    writer.writerow([" "])
    writer.writerow(["PL"])
    ply.to_csv(csvfile, mode='a')
    writer.writerow([" "])
    writer.writerow(["SLO"])
    sloy.to_csv(csvfile, mode='a')
    writer.writerow([" "])
    writer.writerow(["AOP"])
    aopy.to_csv(csvfile, mode='a')

# product separated data
# can use this to print the callouts separately
def seperate(grouped_table, the_table_to_check):
    for i, j in the_table_to_check.groupby(level=0):
        # had to use regex to find exact string match for the table, otherwise it was not pulling the Primary_Storage section
        # it was always pulling the Storage for it since it just matched the Storage from Primary_Storage and pulled the
        # Storage table again.
        if i in re.findall(r'\b'+grouped_table+r'\b', grouped_table):
            print(i)
            obl66 = j
    return obl66

# OBL
ostorage = seperate('Storage', oblz)
odpd_uds = seperate('DPD_UDS', oblz)
ohci_cloud = seperate('HCI_Cloud', oblz)
omidrange = seperate('Midrange', oblz)
onetworking = seperate('Networking', oblz)
oother = seperate('Other', oblz)
opri_storage = seperate('Primary_Storage', oblz)
oserver = seperate('Server', oblz)
ooverall = seperate('OVERALL', oblz)

ostorageq = seperate('Storage', oblq)
# CSAT
cstorage = seperate('Storage', csz)
cdpd_uds = seperate('DPD_UDS', csz)
chci_cloud = seperate('HCI_Cloud', csz)
cmidrange = seperate('Midrange', csz)
cnetworking = seperate('Networking', csz)
cother = seperate('Other', csz)
cpri_storage = seperate('Primary_Storage', csz)
cserver = seperate('Server', csz)
coverall = seperate('OVERALL', csz)

# DSAT
dstorage = seperate('Storage', dsz)
ddpd_uds = seperate('DPD_UDS', dsz)
dhci_cloud = seperate('HCI_Cloud', dsz)
dmidrange = seperate('Midrange', dsz)
dnetworking = seperate('Networking', dsz)
dother = seperate('Other', dsz)
dpri_storage = seperate('Primary_Storage', dsz)
dserver = seperate('Server', dsz)
doverall = seperate('OVERALL', dsz)

# RDR
rstorage = seperate('Storage', rdrz)
rdpd_uds = seperate('DPD_UDS', rdrz)
rhci_cloud = seperate('HCI_Cloud', rdrz)
rmidrange = seperate('Midrange', rdrz)
rnetworking = seperate('Networking', rdrz)
rother = seperate('Other', rdrz)
rpri_storage = seperate('Primary_Storage', rdrz)
rserver = seperate('Server', rdrz)
roverall = seperate('OVERALL', rdrz)

# TTC
tstorage = seperate('Storage', ttcz)
tdpd_uds = seperate('DPD_UDS', ttcz)
thci_cloud = seperate('HCI_Cloud', ttcz)
tmidrange = seperate('Midrange', ttcz)
tnetworking = seperate('Networking', ttcz)
tother = seperate('Other', ttcz)
tpri_storage = seperate('Primary_Storage', ttcz)
tserver = seperate('Server', ttcz)
toverall = seperate('OVERALL', ttcz)

# TTR
trstorage = seperate('Storage', ttrz)
trdpd_uds = seperate('DPD_UDS', ttrz)
trhci_cloud = seperate('HCI_Cloud', ttrz)
trmidrange = seperate('Midrange', ttrz)
trnetworking = seperate('Networking', ttrz)
trother = seperate('Other', ttrz)
trpri_storage = seperate('Primary_Storage', ttrz)
trserver = seperate('Server', ttrz)
troverall = seperate('OVERALL', ttrz)

# PI
pistorage = seperate('Storage', piz)
pidpd_uds = seperate('DPD_UDS', piz)
pihci_cloud = seperate('HCI_Cloud', piz)
pimidrange = seperate('Midrange', piz)
pinetworking = seperate('Networking', piz)
piother = seperate('Other', piz)
pipri_storage = seperate('Primary_Storage', piz)
piserver = seperate('Server', piz)
pioverall = seperate('OVERALL', piz)

# OTS
otstorage = seperate('Storage', otsz)
otdpd_uds = seperate('DPD_UDS', otsz)
othci_cloud = seperate('HCI_Cloud', otsz)
otmidrange = seperate('Midrange', otsz)
otnetworking = seperate('Networking', otsz)
otother = seperate('Other', otsz)
otpri_storage = seperate('Primary_Storage', otsz)
otserver = seperate('Server', otsz)
otoverall = seperate('OVERALL', otsz)

# SL
slstorage = seperate('Storage', slz)
sldpd_uds = seperate('DPD_UDS', slz)
slhci_cloud = seperate('HCI_Cloud', slz)
slmidrange = seperate('Midrange', slz)
slnetworking = seperate('Networking', slz)
slother = seperate('Other', slz)
slpri_storage = seperate('Primary_Storage', slz)
slserver = seperate('Server', slz)
sloverall = seperate('OVERALL', slz)

# AHT
astorage = seperate('Storage', ahtz)
adpd_uds = seperate('DPD_UDS', ahtz)
ahci_cloud = seperate('HCI_Cloud', ahtz)
amidrange = seperate('Midrange', ahtz)
anetworking = seperate('Networking', ahtz)
aother = seperate('Other', ahtz)
apri_storage = seperate('Primary_Storage', ahtz)
aserver = seperate('Server', ahtz)
aoverall = seperate('OVERALL', ahtz)

#CSATP
cpstorage = seperate('Storage', cspz)
cpdpd_uds = seperate('DPD_UDS', cspz)
cphci_cloud = seperate('HCI_Cloud', cspz)
cpmidrange = seperate('Midrange', cspz)
cpnetworking = seperate('Networking', cspz)
cpother = seperate('Other', cspz)
cppri_storage = seperate('Primary_Storage', cspz)
cpserver = seperate('Server', cspz)
cpoverall = seperate('OVERALL', cspz)

#CSATB
cbstorage = seperate('Storage', csbz)
cbdpd_uds = seperate('DPD_UDS', csbz)
cbhci_cloud = seperate('HCI_Cloud', csbz)
cbmidrange = seperate('Midrange', csbz)
cbnetworking = seperate('Networking', csbz)
cbother = seperate('Other', csbz)
cbpri_storage = seperate('Primary_Storage', csbz)
cbserver = seperate('Server', csbz)
cboverall = seperate('OVERALL', csbz)

#DSATP
dpstorage = seperate('Storage', dspz)
dpdpd_uds = seperate('DPD_UDS', dspz)
dphci_cloud = seperate('HCI_Cloud', dspz)
dpmidrange = seperate('Midrange', dspz)
dpnetworking = seperate('Networking', dspz)
dpother = seperate('Other', dspz)
dppri_storage = seperate('Primary_Storage', dspz)
dpserver = seperate('Server', dspz)
dpoverall = seperate('OVERALL', dspz)

#DSATB
dbstorage = seperate('Storage', dsbz)
dbdpd_uds = seperate('DPD_UDS', dsbz)
dbhci_cloud = seperate('HCI_Cloud', dsbz)
dbmidrange = seperate('Midrange', dsbz)
dbnetworking = seperate('Networking', dsbz)
dbother = seperate('Other', dsbz)
dbpri_storage = seperate('Primary_Storage', dsbz)
dbserver = seperate('Server', dsbz)
dboverall = seperate('OVERALL', dsbz)

# PL
plstorage = seperate('Storage', plz)
pldpd_uds = seperate('DPD_UDS', plz)
plhci_cloud = seperate('HCI_Cloud', plz)
plmidrange = seperate('Midrange', plz)
plnetworking = seperate('Networking', plz)
plother = seperate('Other', plz)
plpri_storage = seperate('Primary_Storage', plz)
plserver = seperate('Server', plz)
ploverall = seperate('OVERALL', plz)

# SLO
sostorage = seperate('Storage', sloz)
sodpd_uds = seperate('DPD_UDS', sloz)
sohci_cloud = seperate('HCI_Cloud', sloz)
somidrange = seperate('Midrange', sloz)
sonetworking = seperate('Networking', sloz)
soother = seperate('Other', sloz)
sopri_storage = seperate('Primary_Storage', sloz)
soserver = seperate('Server', sloz)
sooverall = seperate('OVERALL', sloz)

# AOP
aostorage = seperate('Storage', aopz)
aodpd_uds = seperate('DPD_UDS', aopz)
aohci_cloud = seperate('HCI_Cloud', aopz)
aomidrange = seperate('Midrange', aopz)
aonetworking = seperate('Networking', aopz)
aoother = seperate('Other', aopz)
aopri_storage = seperate('Primary_Storage', aopz)
aoserver = seperate('Server', aopz)
aooverall = seperate('OVERALL', aopz)


# dir = tstorage.loc[(tstorage.index.get_level_values('BMS_Region') == 'Storage')]['direction'].values
# dir = str(dir[0])
# dir
#
# tstorage
#

# the following unpacks everything from the dataframe into strings, so that it is easy to display
# if a a table is required then i can simply use the obl66
# print(name)
# def calls(y):
#     obl66 = y
#     # dir = obl66.iloc[1,2]
#     for index, row in obl66.iterrows():
#         print(index[1], row['direction'], round(row['latestweekdata'],2), row['weekname'], row['at'], row[1])
#         if row['trendd3'] != 0:
#             print(" 3week down trend at ", round(row['trendd3'], 2))
#         elif row['trendu3'] != 0:
#             print("  3week up trend at ", round(row['trendu3'], 2))
#         elif row['trendd4'] != 0:
#             print("  4week down trend at ", round(row['trendd4'], 2))
#         elif row['trendu4'] != 0:
#             print("  4week up trend at ", round(row['trendu4'], 2))
#         elif row['trendd5'] != 0:
#             print("  5week down trend at ", round(row['trendd5'], 2))
#         elif row['trendu5'] != 0:
#             print("  5week up trend at ", round(row['trendu5'], 2))
#         elif row['trendd6'] != 0:
#             print("  6week down trend at ", round(row['trendd6'], 2))
#         elif row['trendu6'] != 0:
#             print("  6week up trend at ", round(row['trendu6'], 2))
#     return str

def calls(y):
    obl66 = y
    # dir = obl66.iloc[1,2]
    i=0
    l = len(obl66)
    judge = []
    # while i < l:
    for index, row in obl66.iterrows():
        judge[f'{index[1]} TREND'] = (f"{index[1]} {row['direction']} {round(row['latestweekdata'],2)} {row['weekname']} {row['at']} {row[1]} ")
        if row['trendu6'] != 0:
            judge.append(f"  6week up trend at {round(row['trendu6'], 2)}")
        elif row['trendd6'] != 0:
            judge.append(f"  6week down trend at {round(row['trendd6'], 2)}")
        elif row['trendu5'] != 0:
            judge.append(f"  5week up trend at {round(row['trendu5'], 2)}")
        elif row['trendd5'] != 0:
            judge.append(f"  5week down trend at {round(row['trendd5'], 2)}")
        elif row['trendu4'] != 0:
            judge.append(f"  4week up trend at {round(row['trendu4'], 2)}")
        elif row['trendd4'] != 0:
            judge.append(f"  4week down trend at {round(row['trendd4'], 2)}")
        elif row['trendu3'] != 0:
            judge.append(f"  3week up trend at {round(row['trendu3'], 2)}")
        elif row['trendd3'] != 0:
            judge.append(f" 3week down trend at {round(row['trendd3'], 2)}")
    # i += 1
    return judge #' '.join(judge)

def calls_dict(y):
    obl66 = y
    # dir = obl66.iloc[1,2]
    i=0
    l = len(obl66)
    judge = {}
    # while i < l:
    for index, row in obl66.iterrows():
        judge[index[1]] = (f"{index[1]} {row['direction']} {round(row['latestweekdata'],2)} {row['weekname']} {row['at']} {row[1]} ")
        if row['trendu6'] != 0:
            judge[f'{index[1]} TREND'] = (f"  6week up trend at {round(row['trendu6'], 2)}")
        elif row['trendd6'] != 0:
            judge[f'{index[1]} TREND'] = (f"  6week down trend at {round(row['trendd6'], 2)}")
        elif row['trendu5'] != 0:
            judge[f'{index[1]} TREND'] = (f"  5week up trend at {round(row['trendu5'], 2)}")
        elif row['trendd5'] != 0:
            judge[f'{index[1]} TREND'] = (f"  5week down trend at {round(row['trendd5'], 2)}")
        elif row['trendu4'] != 0:
            judge[f'{index[1]} TREND'] = (f"  4week up trend at {round(row['trendu4'], 2)}")
        elif row['trendd4'] != 0:
            judge[f'{index[1]} TREND'] = (f"  4week down trend at {round(row['trendd4'], 2)}")
        elif row['trendu3'] != 0:
            judge[f'{index[1]} TREND'] = (f"  3week up trend at {round(row['trendu3'], 2)}")
        elif row['trendd3'] != 0:
            judge[f'{index[1]} TREND'] = (f" 3week down trend at {round(row['trendd3'], 2)}")
        else:
            judge[f'{index[1]} TREND'] = ("----")
    # i += 1
    return judge #' '.join(judge)

# i have to figure out the loops for csat and ttc, currently it is working but it is not seeing the loop if direction is up and the metric is not in the list that loop needs to be checked along with the direction and metring in the variables loop.

def high(product, prod_name, meter):
    d = "Down"
    # dir is so complicated because i need to pick the Up Down
    # direction of only level 0 index from the index level 1
    # eg: storage or server and not regional info.
    dir = product.loc[(product.index.get_level_values('BMS_Region') == prod_name)]['direction'].values
    dir = str(dir[0])
    m = ['CSAT', 'OTS', 'SL']
    new = {}
    if (dir in d) and (meter in m):
        new["condition"] = "Opportunity"
        new["product"] = prod_name
        new["metric"] = meter
        new["callouts"] = calls_dict(product)
        # new.append("Highlight")
        # new.append(f"{prod_name}")
        # new.append(meter)
        # new.append(calls(product))
    elif (dir in d) and (meter not in m):
        new["condition"] = "Highlight"
        new["product"] = prod_name
        new["metric"] = meter
        new["callouts"] = calls_dict(product)
    elif (dir not in d) and (meter in m):
    # else:
        new["condition"] = "Highlight"
        new["product"] = prod_name
        new["metric"] = meter
        new["callouts"] = calls_dict(product)
    #     # new.append(f"Opportunity")
    #     # new.append(f"{prod_name}")
    #     # new.append(meter)
    #     # new.append(calls(product))
    # elif (dir not in d) and (meter not in m):
    else:
        new["condition"] = "Opportunity"
        new["product"] = prod_name
        new["metric"] = meter
        new["callouts"] = calls_dict(product)

    return new

# overall
overall_obl = high(ooverall, 'OVERALL', 'obl')
overall_csat = high(coverall, 'OVERALL', 'CSAT')
overall_dsat = high(doverall, 'OVERALL', 'DSAT')
overall_rdr = high(roverall, 'OVERALL', 'RDR')
overall_ttc = high(toverall, 'OVERALL', 'TTC')
overall_ttr = high(troverall, 'OVERALL', 'TTR')
overall_pi = high(pioverall, 'OVERALL', 'PI')
overall_ots = high(otoverall, 'OVERALL', 'OTS')
overall_sl = high(sloverall, 'OVERALL', 'SL')
overall_aht = high(aoverall, 'OVERALL', 'AHT')
overall_csatp = high(cpoverall, 'OVERALL', 'CSATP')
overall_csatb = high(cboverall, 'OVERALL', 'CSATB')
overall_dsatp = high(dpoverall, 'OVERALL', 'DSATP')
overall_dsatb = high(dboverall, 'OVERALL', 'DSATB')
overall_pl = high(ploverall, 'OVERALL', 'PL')
overall_slo = high(sooverall, 'OVERALL', 'SLO')
overall_aop = high(aooverall, 'OVERALL', 'AOP')

# sorage
storage_obl = high(ostorage, 'Storage', 'obl')
storage_csat = high(cstorage, 'Storage', 'CSAT')
storage_dsat = high(dstorage, 'Storage', 'DSAT')
storage_rdr = high(rstorage, 'Storage', 'RDR')
storage_ttc = high(tstorage, 'Storage', 'TTC')
storage_ttr = high(trstorage, 'Storage', 'TTR')
storage_pi = high(pistorage, 'Storage', 'PI')
storage_ots = high(otstorage, 'Storage', 'OTS')
storage_sl = high(slstorage, 'Storage', 'SL')
storage_aht = high(astorage, 'Storage', 'AHT')
storage_csatp = high(cpstorage, 'Storage', 'CSATP')
storage_csatb = high(cbstorage, 'Storage', 'CSATB')
storage_dsatp = high(dpstorage, 'Storage', 'DSATP')
storage_dsatb = high(dbstorage, 'Storage', 'DSATB')
storage_pl = high(plstorage, 'Storage', 'PL')
storage_slo = high(sostorage, 'Storage', 'SLO')
storage_aop = high(aostorage, 'Storage', 'AOP')

# primary storage
pri_storage_obl = high(opri_storage, 'Primary_Storage', 'obl')
pri_storage_csat = high(cpri_storage, 'Primary_Storage', 'CSAT')
pri_storage_dsat = high(dpri_storage, 'Primary_Storage', 'DSAT')
pri_storage_rdr = high(rpri_storage, 'Primary_Storage', 'RDR')
pri_storage_ttc = high(tpri_storage, 'Primary_Storage', 'TTC')
pri_storage_ttr = high(trpri_storage, 'Primary_Storage', 'TTR')
pri_storage_pi = high(pipri_storage, 'Primary_Storage', 'PI')
pri_storage_ots = high(otpri_storage, 'Primary_Storage', 'OTS')
pri_storage_sl = high(slpri_storage, 'Primary_Storage', 'SL')
pri_storage_aht = high(apri_storage, 'Primary_Storage', 'AHT')
pri_storage_csatp = high(cppri_storage, 'Primary_Storage', 'CSATP')
pri_storage_csatb = high(cbpri_storage, 'Primary_Storage', 'CSATB')
pri_storage_dsatp = high(dppri_storage, 'Primary_Storage', 'DSATP')
pri_storage_dsatb = high(dbpri_storage, 'Primary_Storage', 'DSATB')
pri_storage_pl = high(plpri_storage, 'Primary_Storage', 'PL')
pri_storage_slo = high(sopri_storage, 'Primary_Storage', 'SLO')
pri_storage_aop = high(aopri_storage, 'Primary_Storage', 'AOP')

#server
server_obl = high(oserver, 'Server', 'obl')
server_csat = high(cserver, 'Server', 'CSAT')
server_dsat = high(dserver, 'Server', 'DSAT')
server_rdr = high(rserver, 'Server', 'RDR')
server_ttc = high(tserver, 'Server', 'TTC')
server_ttr = high(trserver, 'Server', 'TTR')
server_pi = high(piserver, 'Server', 'PI')
server_ots = high(otserver, 'Server', 'OTS')
server_sl = high(slserver, 'Server', 'SL')
server_aht = high(aserver, 'Server', 'AHT')
server_csatp = high(cpserver, 'Server', 'CSATP')
server_csatb = high(cbserver, 'Server', 'CSATB')
server_dsatp = high(dpserver, 'Server', 'DSATP')
server_dsatb = high(dbserver, 'Server', 'DSATB')
server_pl = high(plserver, 'Server', 'PL')
server_slo = high(soserver, 'Server', 'SLO')
server_aop = high(aoserver, 'Server', 'AOP')

# Networking
networking_obl = high(onetworking, 'Networking', 'obl')
networking_csat = high(cnetworking, 'Networking', 'CSAT')
networking_dsat = high(dnetworking, 'Networking', 'DSAT')
networking_rdr = high(rnetworking, 'Networking', 'RDR')
networking_ttc = high(tnetworking, 'Networking', 'TTC')
networking_ttr = high(trnetworking, 'Networking', 'TTR')
networking_pi = high(pinetworking, 'Networking', 'PI')
networking_ots = high(otnetworking, 'Networking', 'OTS')
networking_sl = high(slnetworking, 'Networking', 'SL')
networking_aht = high(anetworking, 'Networking', 'AHT')
networking_csatp = high(cpnetworking, 'Networking', 'CSATP')
networking_csatb = high(cbnetworking, 'Networking', 'CSATB')
networking_dsatp = high(dpnetworking, 'Networking', 'DSATP')
networking_dsatb = high(dbnetworking, 'Networking', 'DSATB')
networking_pl = high(plnetworking, 'Networking', 'PL')
networking_slo = high(sonetworking, 'Networking', 'SLO')
networking_aop = high(aonetworking, 'Networking', 'AOP')

# midrange
midrange_obl = high(omidrange, 'Midrange', 'obl')
midrange_csat = high(cmidrange, 'Midrange', 'CSAT')
midrange_dsat = high(dmidrange, 'Midrange', 'DSAT')
midrange_rdr = high(rmidrange, 'Midrange', 'RDR')
midrange_ttc = high(tmidrange, 'Midrange', 'TTC')
midrange_ttr = high(trmidrange, 'Midrange', 'TTR')
midrange_pi = high(pimidrange, 'Midrange', 'PI')
midrange_ots = high(otmidrange, 'Midrange', 'OTS')
midrange_sl = high(slmidrange, 'Midrange', 'SL')
midrange_aht = high(amidrange, 'Midrange', 'AHT')
midrange_csatp = high(cpmidrange, 'Midrange', 'CSATP')
midrange_csatb = high(cbmidrange, 'Midrange', 'CSATB')
midrange_dsatp = high(dpmidrange, 'Midrange', 'DSATP')
midrange_dsatb = high(dbmidrange, 'Midrange', 'DSATB')
midrange_pl = high(plmidrange, 'Midrange', 'PL')
midrange_slo = high(somidrange, 'Midrange', 'SLO')
midrange_aop = high(aomidrange, 'Midrange', 'AOP')

# HCI_CLoud
hci_cloud_obl = high(ohci_cloud, 'HCI_Cloud', 'obl')
hci_cloud_csat = high(chci_cloud, 'HCI_Cloud', 'CSAT')
hci_cloud_dsat = high(dhci_cloud, 'HCI_Cloud', 'DSAT')
hci_cloud_rdr = high(rhci_cloud, 'HCI_Cloud', 'RDR')
hci_cloud_ttc = high(thci_cloud, 'HCI_Cloud', 'TTC')
hci_cloud_ttr = high(trhci_cloud, 'HCI_Cloud', 'TTR')
hci_cloud_pi = high(pihci_cloud, 'HCI_Cloud', 'PI')
hci_cloud_ots = high(othci_cloud, 'HCI_Cloud', 'OTS')
hci_cloud_sl = high(slhci_cloud, 'HCI_Cloud', 'SL')
hci_cloud_aht = high(ahci_cloud, 'HCI_Cloud', 'AHT')
hci_cloud_csatp = high(cphci_cloud, 'HCI_Cloud', 'CSATP')
hci_cloud_csatb = high(cbhci_cloud, 'HCI_Cloud', 'CSATB')
hci_cloud_dsatp = high(dphci_cloud, 'HCI_Cloud', 'DSATP')
hci_cloud_dsatb = high(dbhci_cloud, 'HCI_Cloud', 'DSATB')
hci_cloud_pl = high(plhci_cloud, 'HCI_Cloud', 'PL')
hci_cloud_slo = high(sohci_cloud, 'HCI_Cloud', 'SLO')
hci_cloud_aop = high(aohci_cloud, 'HCI_Cloud', 'AOP')

# DPD_UDS
dpd_uds_obl = high(odpd_uds, 'DPD_UDS', 'obl')
dpd_uds_csat = high(cdpd_uds, 'DPD_UDS', 'CSAT')
dpd_uds_dsat = high(ddpd_uds, 'DPD_UDS', 'DSAT')
dpd_uds_rdr = high(rdpd_uds, 'DPD_UDS', 'RDR')
dpd_uds_ttc = high(tdpd_uds, 'DPD_UDS', 'TTC')
dpd_uds_ttr = high(trdpd_uds, 'DPD_UDS', 'TTR')
dpd_uds_pi = high(pidpd_uds, 'DPD_UDS', 'PI')
dpd_uds_ots = high(otdpd_uds, 'DPD_UDS', 'OTS')
dpd_uds_sl = high(sldpd_uds, 'DPD_UDS', 'SL')
dpd_uds_aht = high(adpd_uds, 'DPD_UDS', 'AHT')
dpd_uds_csatp = high(cpdpd_uds, 'DPD_UDS', 'CSATP')
dpd_uds_csatb = high(cbdpd_uds, 'DPD_UDS', 'CSATB')
dpd_uds_dsatp = high(dpdpd_uds, 'DPD_UDS', 'DSATP')
dpd_uds_dsatb = high(dbdpd_uds, 'DPD_UDS', 'DSATB')
dpd_uds_pl = high(pldpd_uds, 'DPD_UDS', 'PL')
dpd_uds_slo = high(sodpd_uds, 'DPD_UDS', 'SLO')
dpd_uds_aop = high(aodpd_uds, 'DPD_UDS', 'AOP')

#others
other_obl = high(oother, 'Other', 'obl')
other_csat = high(cother, 'Other', 'CSAT')
other_dsat = high(dother, 'Other', 'DSAT')
other_rdr = high(rother, 'Other', 'RDR')
other_ttc = high(tother, 'Other', 'TTC')
other_ttr = high(trother, 'Other', 'TTR')
other_pi = high(piother, 'Other', 'PI')
other_ots = high(otother, 'Other', 'OTS')
other_sl = high(slother, 'Other', 'SL')
other_aht = high(aother, 'Other', 'AHT')
other_csatp = high(cpother, 'Other', 'CSATP')
other_csatb = high(cbother, 'Other', 'CSATB')
other_dsatp = high(dpother, 'Other', 'DSATP')
other_dsatb = high(dbother, 'Other', 'DSATB')
other_pl = high(plother, 'Other', 'PL')
other_slo = high(soother, 'Other', 'SLO')
other_aop = high(aoother, 'Other', 'AOP')

# REVIEW: this is to figure out on how to write to CSV. and also to write the dictionary.
# with open(trendcsv, 'a', newline='') as cf:
#     writer = csv.writer(cf, delimiter = ',')
#     writer.writerow(storage_obl['callouts'][0:])
#     key = storage_obl.keys()
#     writer2 = csv.DictWriter(cf, fieldnames = key)
#     writer2.writerow(storage_obl)


# len(other_obl['callouts'])
# for key, val in other_obl.items():
#     print(key, "=>", val)
#
# for regions in other_obl.values():
#     print(regions)
#     regiondata = other_obl['callouts'][regions]
#     print(regiondata)

# def printline()
#     i = len(other_obl['callouts'])
#     for j in range(i):
#         print(other_obl['callouts'][j])
#
# print(j) for j in other_obl['callouts']
#
# l=0
# while l < i:
#     print(other_obl['callouts'][l])
#     l += 1
#
# other_obl.values()
# print(other_obl.values())
# with open(outfile, 'w') as f1:
def writetext(dictwrite, text):
    print("============ WEEKLY "+text+" {} {} ================".format(dictwrite['metric'], dictwrite['condition']), file=f)
    print(''.join(map(str,dictwrite['product'][:])), file=f)
    print(''.join(map(str,dictwrite['metric'][:])), file=f)
    print(''.join(map(str,dictwrite['condition'][:])), file=f)
    print(''.join(map(str,dictwrite['callouts'][text][:])), file=f)
    print(''.join(map(str,dictwrite['callouts'][text+' TREND'][:])), file=f)
    print(''.join(map(str,dictwrite['callouts']['NA'][:])), file=f)
    print(''.join(map(str,dictwrite['callouts']['NA TREND'][:])), file=f)
    print(''.join(map(str,dictwrite['callouts']['LA'][:])), file=f)
    print(''.join(map(str,dictwrite['callouts']['LA TREND'][:])), file=f)
    print(''.join(map(str,dictwrite['callouts']['EMEA'][:])), file=f)
    print(''.join(map(str,dictwrite['callouts']['EMEA TREND'][:])), file=f)
    print(''.join(map(str,dictwrite['callouts']['APJ'][:])), file=f)
    print(''.join(map(str,dictwrite['callouts']['APJ TREND'][:])), file=f)

with open(outfile, 'a') as f:
    # f.write('\n'.join(map(str, storage_obl[])))
    # f.write(str(storage_csat))
    # f.write(str(storage_dsat))
    # f.write(str(storage_rdr))
    # f.write(str(storage_ttc))
    print(f"output time: {datetime.now()}", file=f)
    # overall
    print("============ OVERALL ================", file=f)
    print("============ WEEKLY ================", file=f)
    print(''.join(map(str,overall_obl['product'][:])), file=f)
    print(''.join(map(str,overall_obl['metric'][:])), file=f)
    print(''.join(map(str,overall_obl['condition'][:])), file=f)
    # print('\n'.join(map(str,overall_obl['callouts']['OVERALL'][:])), file=f)
    print(''.join(map(str,overall_obl['callouts']['OVERALL'][:])), file=f)
    print(''.join(map(str,overall_obl['callouts']['OVERALL TREND'][:])), file=f)
    print('\n', file=f)
    # print(''.join(map(str,overall_rdr['metric'][:])), file=f)
    # print(''.join(map(str,overall_rdr['condition'][:])), file=f)
    # print('\n'.join(map(str,overall_rdr['callouts'][:]))+'\n', file=f)
    print(''.join(map(str,overall_csat['metric'][:])), file=f)
    print(''.join(map(str,overall_csat['condition'][:])), file=f)
    print(''.join(map(str,overall_csat['callouts']['OVERALL'][:])), file=f)
    print(''.join(map(str,overall_csat['callouts']['OVERALL TREND'][:])), file=f)
    print('\n', file=f)
    print(''.join(map(str,overall_dsat['metric'][:])), file=f)
    print(''.join(map(str,overall_dsat['condition'][:])), file=f)
    print(''.join(map(str,overall_dsat['callouts']['OVERALL'][:])), file=f)
    print(''.join(map(str,overall_dsat['callouts']['OVERALL TREND'][:])), file=f)
    print('\n', file=f)
    print(''.join(map(str,overall_ttc['metric'][:])), file=f)
    print(''.join(map(str,overall_ttc['condition'][:])), file=f)
    print(''.join(map(str,overall_ttc['callouts']['OVERALL'][:])), file=f)
    print(''.join(map(str,overall_ttc['callouts']['OVERALL TREND'][:])), file=f)
    print('\n', file=f)
    print(''.join(map(str,overall_ttr['metric'][:])), file=f)
    print(''.join(map(str,overall_ttr['condition'][:])), file=f)
    print(''.join(map(str,overall_ttr['callouts']['OVERALL'][:])), file=f)
    print(''.join(map(str,overall_ttr['callouts']['OVERALL TREND'][:])), file=f)
    print('\n', file=f)
    print(''.join(map(str,overall_pi['metric'][:])), file=f)
    print(''.join(map(str,overall_pi['condition'][:])), file=f)
    print(''.join(map(str,overall_pi['callouts']['OVERALL'][:])), file=f)
    print(''.join(map(str,overall_pi['callouts']['OVERALL TREND'][:])), file=f)
    print('\n', file=f)
    print(''.join(map(str,overall_ots['metric'][:])), file=f)
    print(''.join(map(str,overall_ots['condition'][:])), file=f)
    print(''.join(map(str,overall_ots['callouts']['OVERALL'][:])), file=f)
    print(''.join(map(str,overall_ots['callouts']['OVERALL TREND'][:])), file=f)
    print('\n', file=f)
    print(''.join(map(str,overall_sl['metric'][:])), file=f)
    print(''.join(map(str,overall_sl['condition'][:])), file=f)
    print(''.join(map(str,overall_sl['callouts']['OVERALL'][:])), file=f)
    print(''.join(map(str,overall_sl['callouts']['OVERALL TREND'][:])), file=f)
    print('\n', file=f)
    print(''.join(map(str,overall_aht['metric'][:])), file=f)
    print(''.join(map(str,overall_aht['condition'][:])), file=f)
    print(''.join(map(str,overall_aht['callouts']['OVERALL'][:])), file=f)
    print(''.join(map(str,overall_aht['callouts']['OVERALL TREND'][:])), file=f)
    print('\n', file=f)
    print(''.join(map(str,overall_csatp['metric'][:])), file=f)
    print(''.join(map(str,overall_csatp['condition'][:])), file=f)
    print(''.join(map(str,overall_csatp['callouts']['OVERALL'][:])), file=f)
    print(''.join(map(str,overall_csatp['callouts']['OVERALL TREND'][:])), file=f)
    print('\n', file=f)
    print(''.join(map(str,overall_csatb['metric'][:])), file=f)
    print(''.join(map(str,overall_csatb['condition'][:])), file=f)
    print(''.join(map(str,overall_csatb['callouts']['OVERALL'][:])), file=f)
    print(''.join(map(str,overall_csatb['callouts']['OVERALL TREND'][:])), file=f)
    print('\n', file=f)
    print(''.join(map(str,overall_dsatp['metric'][:])), file=f)
    print(''.join(map(str,overall_dsatp['condition'][:])), file=f)
    print(''.join(map(str,overall_dsatp['callouts']['OVERALL'][:])), file=f)
    print(''.join(map(str,overall_dsatp['callouts']['OVERALL TREND'][:])), file=f)
    print('\n', file=f)
    print(''.join(map(str,overall_dsatb['metric'][:])), file=f)
    print(''.join(map(str,overall_dsatb['condition'][:])), file=f)
    print(''.join(map(str,overall_dsatb['callouts']['OVERALL'][:])), file=f)
    print(''.join(map(str,overall_dsatb['callouts']['OVERALL TREND'][:])), file=f)
    print('\n', file=f)
    print(''.join(map(str,overall_pl['metric'][:])), file=f)
    print(''.join(map(str,overall_pl['condition'][:])), file=f)
    print(''.join(map(str,overall_pl['callouts']['OVERALL'][:])), file=f)
    print(''.join(map(str,overall_pl['callouts']['OVERALL TREND'][:])), file=f)
    print('\n', file=f)
    print(''.join(map(str,overall_slo['metric'][:])), file=f)
    print(''.join(map(str,overall_slo['condition'][:])), file=f)
    print(''.join(map(str,overall_slo['callouts']['OVERALL'][:])), file=f)
    print(''.join(map(str,overall_slo['callouts']['OVERALL TREND'][:])), file=f)
    print('\n', file=f)
    print(''.join(map(str,overall_aop['metric'][:])), file=f)
    print(''.join(map(str,overall_aop['condition'][:])), file=f)
    print(''.join(map(str,overall_aop['callouts']['OVERALL'][:])), file=f)
    print(''.join(map(str,overall_aop['callouts']['OVERALL TREND'][:])), file=f)
    print('\n', file=f)
    # print("============ WEEKLY STORAGE {}================".format(), file=f)
    # STORAGE
    writetext(storage_obl, 'Storage')
    print('\n', file=f)
    writetext(storage_csat, 'Storage')
    print('\n', file=f)
    writetext(storage_dsat, 'Storage')
    print('\n', file=f)
    writetext(storage_rdr, 'Storage')
    print('\n', file=f)
    writetext(storage_ttc, 'Storage')
    print('\n', file=f)
    writetext(storage_ttr, 'Storage')
    print('\n', file=f)
    writetext(storage_pi, 'Storage')
    print('\n', file=f)
    writetext(storage_ots, 'Storage')
    print('\n', file=f)
    writetext(storage_sl, 'Storage')
    print('\n', file=f)
    writetext(storage_aht, 'Storage')
    print('\n', file=f)
    writetext(storage_csatp, 'Storage')
    print('\n', file=f)
    writetext(storage_csatb, 'Storage')
    print('\n', file=f)
    writetext(storage_dsatp, 'Storage')
    print('\n', file=f)
    writetext(storage_dsatb, 'Storage')
    print('\n', file=f)
    writetext(storage_pl, 'Storage')
    print('\n', file=f)
    writetext(storage_slo, 'Storage')
    print('\n', file=f)
    writetext(storage_aop, 'Storage')
    print('\n', file=f)
    # print("============ WEEKLY SERVER ================", file=f)
    # SERVER
    writetext(server_obl, 'Server')
    print('\n', file=f)
    writetext(server_csat, 'Server')
    print('\n', file=f)
    writetext(server_dsat, 'Server')
    print('\n', file=f)
    writetext(server_rdr, 'Server')
    print('\n', file=f)
    writetext(server_ttc, 'Server')
    print('\n', file=f)
    writetext(server_ttr, 'Server')
    print('\n', file=f)
    writetext(server_pi, 'Server')
    print('\n', file=f)
    writetext(server_ots, 'Server')
    print('\n', file=f)
    writetext(server_sl, 'Server')
    print('\n', file=f)
    writetext(server_aht, 'Server')
    print('\n', file=f)
    writetext(server_csatp, 'Server')
    print('\n', file=f)
    writetext(server_csatb, 'Server')
    print('\n', file=f)
    writetext(server_dsatp, 'Server')
    print('\n', file=f)
    writetext(server_dsatb, 'Server')
    print('\n', file=f)
    writetext(server_pl, 'Server')
    print('\n', file=f)
    writetext(server_slo, 'Server')
    print('\n', file=f)
    writetext(server_aop, 'Server')
    print('\n', file=f)
    # NETWORKING
    writetext(networking_obl, 'Networking')
    print('\n', file=f)
    writetext(networking_csat, 'Networking')
    print('\n', file=f)
    writetext(networking_dsat, 'Networking')
    print('\n', file=f)
    writetext(networking_rdr, 'Networking')
    print('\n', file=f)
    writetext(networking_ttc, 'Networking')
    print('\n', file=f)
    writetext(networking_ttr, 'Networking')
    print('\n', file=f)
    writetext(networking_pi, 'Networking')
    print('\n', file=f)
    writetext(networking_ots, 'Networking')
    print('\n', file=f)
    writetext(networking_sl, 'Networking')
    print('\n', file=f)
    writetext(networking_aht, 'Networking')
    print('\n', file=f)
    writetext(networking_csatp, 'Networking')
    print('\n', file=f)
    writetext(networking_csatb, 'Networking')
    print('\n', file=f)
    writetext(networking_dsatp, 'Networking')
    print('\n', file=f)
    writetext(networking_dsatb, 'Networking')
    print('\n', file=f)
    writetext(networking_pl, 'Networking')
    print('\n', file=f)
    writetext(networking_slo, 'Networking')
    print('\n', file=f)
    writetext(networking_aop, 'Networking')
    print('\n', file=f)
    # PRIMARY STORAGE
    writetext(pri_storage_obl, 'Primary_Storage')
    print('\n', file=f)
    writetext(pri_storage_csat, 'Primary_Storage')
    print('\n', file=f)
    writetext(pri_storage_dsat, 'Primary_Storage')
    print('\n', file=f)
    writetext(pri_storage_rdr, 'Primary_Storage')
    print('\n', file=f)
    writetext(pri_storage_ttc, 'Primary_Storage')
    print('\n', file=f)
    writetext(pri_storage_ttr, 'Primary_Storage')
    print('\n', file=f)
    writetext(pri_storage_pi, 'Primary_Storage')
    print('\n', file=f)
    writetext(pri_storage_ots, 'Primary_Storage')
    print('\n', file=f)
    writetext(pri_storage_sl, 'Primary_Storage')
    print('\n', file=f)
    writetext(pri_storage_aht, 'Primary_Storage')
    print('\n', file=f)
    writetext(pri_storage_csatp, 'Primary_Storage')
    print('\n', file=f)
    writetext(pri_storage_csatb, 'Primary_Storage')
    print('\n', file=f)
    writetext(pri_storage_dsatp, 'Primary_Storage')
    print('\n', file=f)
    writetext(pri_storage_dsatb, 'Primary_Storage')
    print('\n', file=f)
    writetext(pri_storage_pl, 'Primary_Storage')
    print('\n', file=f)
    writetext(pri_storage_slo, 'Primary_Storage')
    print('\n', file=f)
    writetext(pri_storage_aop, 'Primary_Storage')
    print('\n', file=f)
    # OTHER
    writetext(other_obl, 'Other')
    print('\n', file=f)
    writetext(other_csat, 'Other')
    print('\n', file=f)
    writetext(other_dsat, 'Other')
    print('\n', file=f)
    writetext(other_rdr, 'Other')
    print('\n', file=f)
    writetext(other_ttc, 'Other')
    print('\n', file=f)
    writetext(other_ttr, 'Other')
    print('\n', file=f)
    writetext(other_pi, 'Other')
    print('\n', file=f)
    writetext(other_ots, 'Other')
    print('\n', file=f)
    writetext(other_sl, 'Other')
    print('\n', file=f)
    writetext(other_aht, 'Other')
    print('\n', file=f)
    writetext(other_csatp, 'Other')
    print('\n', file=f)
    writetext(other_csatb, 'Other')
    print('\n', file=f)
    writetext(other_dsatp, 'Other')
    print('\n', file=f)
    writetext(other_dsatb, 'Other')
    print('\n', file=f)
    writetext(other_pl, 'Other')
    print('\n', file=f)
    writetext(other_slo, 'Other')
    print('\n', file=f)
    writetext(other_aop, 'Other')
    print('\n', file=f)
    # MIDRANGE
    writetext(midrange_obl, 'Midrange')
    print('\n', file=f)
    writetext(midrange_csat, 'Midrange')
    print('\n', file=f)
    writetext(midrange_dsat, 'Midrange')
    print('\n', file=f)
    writetext(midrange_rdr, 'Midrange')
    print('\n', file=f)
    writetext(midrange_ttc, 'Midrange')
    print('\n', file=f)
    writetext(midrange_ttr, 'Midrange')
    print('\n', file=f)
    writetext(midrange_pi, 'Midrange')
    print('\n', file=f)
    writetext(midrange_ots, 'Midrange')
    print('\n', file=f)
    writetext(midrange_sl, 'Midrange')
    print('\n', file=f)
    writetext(midrange_aht, 'Midrange')
    print('\n', file=f)
    writetext(midrange_csatp, 'Midrange')
    print('\n', file=f)
    writetext(midrange_csatb, 'Midrange')
    print('\n', file=f)
    writetext(midrange_dsatp, 'Midrange')
    print('\n', file=f)
    writetext(midrange_dsatb, 'Midrange')
    print('\n', file=f)
    writetext(midrange_pl, 'Midrange')
    print('\n', file=f)
    writetext(midrange_slo, 'Midrange')
    print('\n', file=f)
    writetext(midrange_aop, 'Midrange')
    print('\n', file=f)
    # HCI_CLOUD
    writetext(hci_cloud_obl, 'HCI_Cloud')
    print('\n', file=f)
    writetext(hci_cloud_csat, 'HCI_Cloud')
    print('\n', file=f)
    writetext(hci_cloud_dsat, 'HCI_Cloud')
    print('\n', file=f)
    writetext(hci_cloud_rdr, 'HCI_Cloud')
    print('\n', file=f)
    writetext(hci_cloud_ttc, 'HCI_Cloud')
    print('\n', file=f)
    writetext(hci_cloud_ttr, 'HCI_Cloud')
    print('\n', file=f)
    writetext(hci_cloud_pi, 'HCI_Cloud')
    print('\n', file=f)
    writetext(hci_cloud_ots, 'HCI_Cloud')
    print('\n', file=f)
    writetext(hci_cloud_sl, 'HCI_Cloud')
    print('\n', file=f)
    writetext(hci_cloud_aht, 'HCI_Cloud')
    print('\n', file=f)
    writetext(hci_cloud_csatp, 'HCI_Cloud')
    print('\n', file=f)
    writetext(hci_cloud_csatb, 'HCI_Cloud')
    print('\n', file=f)
    writetext(hci_cloud_dsatp, 'HCI_Cloud')
    print('\n', file=f)
    writetext(hci_cloud_dsatb, 'HCI_Cloud')
    print('\n', file=f)
    writetext(hci_cloud_pl, 'HCI_Cloud')
    print('\n', file=f)
    writetext(hci_cloud_slo, 'HCI_Cloud')
    print('\n', file=f)
    writetext(hci_cloud_aop, 'HCI_Cloud')
    print('\n', file=f)
    # dpd_uds
    writetext(dpd_uds_obl, 'DPD_UDS')
    print('\n', file=f)
    writetext(dpd_uds_csat, 'DPD_UDS')
    print('\n', file=f)
    writetext(dpd_uds_dsat, 'DPD_UDS')
    print('\n', file=f)
    writetext(dpd_uds_rdr, 'DPD_UDS')
    print('\n', file=f)
    writetext(dpd_uds_ttc, 'DPD_UDS')
    print('\n', file=f)
    writetext(dpd_uds_ttr, 'DPD_UDS')
    print('\n', file=f)
    writetext(dpd_uds_pi, 'DPD_UDS')
    print('\n', file=f)
    writetext(dpd_uds_ots, 'DPD_UDS')
    print('\n', file=f)
    writetext(dpd_uds_sl, 'DPD_UDS')
    print('\n', file=f)
    writetext(dpd_uds_aht, 'DPD_UDS')
    print('\n', file=f)
    writetext(dpd_uds_csatp, 'DPD_UDS')
    print('\n', file=f)
    writetext(dpd_uds_csatb, 'DPD_UDS')
    print('\n', file=f)
    writetext(dpd_uds_dsatp, 'DPD_UDS')
    print('\n', file=f)
    writetext(dpd_uds_dsatb, 'DPD_UDS')
    print('\n', file=f)
    writetext(dpd_uds_pl, 'DPD_UDS')
    print('\n', file=f)
    writetext(dpd_uds_slo, 'DPD_UDS')
    print('\n', file=f)
    writetext(dpd_uds_aop, 'DPD_UDS')
    print('\n', file=f)

# TUTORIAL the following illustrates the if conditions for the Highlights and opportunities
# declare variables to test
# d = "Down"
# dir = "Down"
# meter = "CSAT"
# m = ['CSAT', 'OTS']
#
# create an empty dictionary to store data
# new = {}
#
# loop begins here
#
# the for loop that you see is not required, and the if condition automatically iterates through the list.
# i do not need to specify the for loop to iterate through the list. #str(i) for i in m):
#
# if (dir in d) and (meter not in m): #str(i) for i in m):
#     print(dir, meter)
#     print("Highlight")
# elif (dir not in d) and (meter in m): #str(i) for i in m):
#     print(dir, meter)
#     print("opportunity")
# # elif (d not in dir) and (meter in str(i) for i in m):
# else:
#     print(dir, meter)
#     print("Opportunity else")
#
# for i in m:
#     if meter in m:
#         print(meter)
#     else:
#         print("no")

# TUTORIAL this prints the dictionary and the items from the value of the name.
# i can specify the array location of the item that i want to view
# test['Storage'][3]

# called = ' '.join(calls(storage))
#
# called

# called = print(calls(storage))

    # dir = others.loc['Other']['direction'] #'BMS_Region'=='Other','direction')
    # dir
    # dir = pri_storage.loc[(pri_storage.index.get_level_values('BMS_Region') == 'Primary Stoage')]['direction'].values
    #
    # dir = str(dir[0])
    #
    # if test2 == 'Up':
    #     print("works")
    # else:
    #     print("nope")

# def high(product, prod_name, meter):
#     d = "Down"
#     dir = product.loc[(product.index.get_level_values('BMS_Region') == prod_name)]['direction'].values
#     dir = str(dir[0])
#     if d in dir:
#         print("{} callouts".format(prod_name))
#         print('Highlight')
#         print("\n")
#         print(meter)
#         calls(product)
#         print("\n")
#         # print("\n")
#         # print(product[1])
#         # calls(product[1])
#     else:
#         print("{} callouts".format(prod_name))
#         print("Opportunities")
#         print("\n")
#         print(meter)
#         calls(product)
#         print("\n")
#         # print("\n")
#         # print(product[1])
#         # calls(product[1])
#     return None
# file = r'D:\git_stuff\Development\ACallouts\output.txt'
# print('\n'.join(map(str,storage_rdr['callouts'][1:])))

# if i am not able to print it directly then i will have to put it into a text file and then get the input from the text as a list
# and the output it into the HTML output. this is the last resort . if nothing else works.
# i am getting None output from the definions for now. i have to find a way to print them as strings.
# find out if there is a way to put the print output in a variable look at the documentation, there must be a way to redirect it
# like we do for a file.

# text_markdown = "\t"
# with open(file) as this_file:
#     for a in this_file.read():
#         if "\n" in a:
#             text_markdown += "\n \t"
#         else:
#             text_markdown += a

classlight = storage_obl['condition']

htmltext = r'D:\git_stuff\Development\ACallouts\output2.txt'
def htmlwrite(htmldict, text2, filewrite):
    filewrite.write("============ WEEKLY "+text2+" {} {} ================".format(htmldict['metric'], htmldict['condition']))
    filewrite.write('\n {}'.format(htmldict['product'][:]))
    filewrite.write('\n {}'.format(htmldict['metric'][:]))
    filewrite.write('\n {}'.format(htmldict['condition'][:]))
    filewrite.write('\n {}'.format(htmldict['callouts'][text2][:]))
    filewrite.write('\n {}'.format(htmldict['callouts'][text2+' TREND'][:]))
    filewrite.write('\n {}'.format(htmldict['callouts']['NA'][:]))
    filewrite.write('\n {}'.format(htmldict['callouts']['NA TREND'][:]))
    filewrite.write('\n {}'.format(htmldict['callouts']['LA'][:]))
    filewrite.write('\n {}'.format(htmldict['callouts']['LA TREND'][:]))
    filewrite.write('\n {}'.format(htmldict['callouts']['EMEA'][:]))
    filewrite.write('\n {}'.format(htmldict['callouts']['EMEA TREND'][:]))
    filewrite.write('\n {}'.format(htmldict['callouts']['APJ'][:]))
    filewrite.write('\n {}'.format(htmldict['callouts']['APJ TREND'][:]))
    filewrite.write("\n ============================================== \n")

def htmlwrite_o(htmldict, text2, filewrite):
    filewrite.write("============ WEEKLY "+text2+" {} {} ================".format(htmldict['metric'], htmldict['condition']))
    filewrite.write('\n {}'.format(htmldict['product'][:]))
    filewrite.write('\n {}'.format(htmldict['metric'][:]))
    filewrite.write('\n {}'.format(htmldict['condition'][:]))
    filewrite.write('\n {}'.format(htmldict['callouts'][text2][:]))
    filewrite.write('\n {}'.format(htmldict['callouts'][text2+' TREND'][:]))
    filewrite.write("\n ============================================== \n")
    condition = htmldict['condition']
    return condition


# with open(htmltext, 'r+') as ht:
#     htmlwrite_o(overall_obl, 'OVERALL', ht)
#     test = ht.readlines()
#     condition = htmlwrite_o(overall_obl, 'OVERALL', ht)
#
#
#     # test
#     # condition

metric_selection = ['CSAT','DSAT','OBL','SL','AHT','RDR','TTC','TTR','PI','CSAT-PRO','CSAT-BASIC','DSAT-PRO','DSAT-BASIC','SLO','AOP','PL']

app.layout = html.Div([
            html.Div(className = "row", children=[
                        html.Div(className = 'four columns div-user-controls', children = [
                                dcc.Dropdown(id = 'calls_selection',
                                            options = [{'label':i, 'value':i} for i in metric_selection],
                                            value=' '),
                                html.Div(children = [
                                        html.H1(id='test1', style={'whiteSpace': 'pre-wrap'}),
                                        html.H2(id='test2', style={'whiteSpace': 'pre-wrap'}),
                                        html.H2(id='test3', style={'whiteSpace': 'pre-wrap'}),
                                        html.H2(id='test4', style={'whiteSpace': 'pre-wrap'})
                                        ]),
                                html.Div(html.H3(id = 'oregion3', style={'whiteSpace': 'pre-wrap'}))
                        ]),
                        html.Div(className = 'eight columns div-for-charts bg-grey', children=[
                                    dcc.Graph(id='trends'),
                                    dcc.Graph(id='quartertrends'),
                                    dcc.Graph(id='yearesg'),
                                    dcc.Graph(id='yearhes'),
                        ])
            ])
            ])

@app.callback(
    [Output('test1', 'children'),
    Output('test2', 'children'),
    Output('test3', 'children'),
    Output('test4', 'children'),
    Output('oregion3', 'children')],
    [Input('calls_selection', 'value')]
)
def update_callouts(selected_prod):
    line1, line2, line3, line4 = "","","",""
    info = []
    if selected_prod == 'CSAT':
        line1 = overall_csat['condition']
        line2 = overall_csat['metric']
        line3 = overall_csat['callouts']['OVERALL']
        line4 = overall_csat['callouts']['OVERALL TREND']
        with open(htmltext, 'r+') as ht:
            ht.truncate(0)
            # htmlwrite_o(overall_csat, 'OVERALL', ht)
            htmlwrite(storage_csat, 'Storage', ht)
            htmlwrite(server_csat, 'Server', ht)
            htmlwrite(networking_csat, 'Networking', ht)
            htmlwrite(pri_storage_csat, 'Primary_Storage', ht)
            htmlwrite(other_csat, 'Other', ht)
            htmlwrite(midrange_csat, 'Midrange', ht)
            htmlwrite(hci_cloud_csat, 'HCI_Cloud', ht)
            htmlwrite(dpd_uds_csat, 'DPD_UDS', ht)
            ht.close()
        with open(htmltext, 'r') as ht2:
            info = ht2.readlines()
            ht2.close()
    elif selected_prod == 'OBL':
        line1 = overall_obl['condition']
        line2 = overall_obl['metric']
        line3 = overall_obl['callouts']['OVERALL']
        line4 = overall_obl['callouts']['OVERALL TREND']
        with open(htmltext, 'r+') as ht:
            ht.truncate(0)
            # htmlwrite_o(overall_obl, 'OVERALL', ht)
            htmlwrite(storage_obl, 'Storage', ht)
            htmlwrite(server_obl, 'Server', ht)
            htmlwrite(networking_obl, 'Networking', ht)
            htmlwrite(pri_storage_obl, 'Primary_Storage', ht)
            htmlwrite(other_obl, 'Other', ht)
            htmlwrite(midrange_obl, 'Midrange', ht)
            htmlwrite(hci_cloud_obl, 'HCI_Cloud', ht)
            htmlwrite(dpd_uds_obl, 'DPD_UDS', ht)
            ht.close()
        with open(htmltext, 'r') as ht2:
            info = ht2.readlines()
            ht2.close()
    elif selected_prod == 'DSAT':
        line1 = overall_dsat['condition']
        line2 = overall_dsat['metric']
        line3 = overall_dsat['callouts']['OVERALL']
        line4 = overall_dsat['callouts']['OVERALL TREND']
        with open(htmltext, 'r+') as ht:
            ht.truncate(0)
            # htmlwrite_o(overall_dsat, 'OVERALL', ht)
            htmlwrite(storage_dsat, 'Storage', ht)
            htmlwrite(server_dsat, 'Server', ht)
            htmlwrite(networking_dsat, 'Networking', ht)
            htmlwrite(pri_storage_dsat, 'Primary_Storage', ht)
            htmlwrite(other_dsat, 'Other', ht)
            htmlwrite(midrange_dsat, 'Midrange', ht)
            htmlwrite(hci_cloud_dsat, 'HCI_Cloud', ht)
            htmlwrite(dpd_uds_dsat, 'DPD_UDS', ht)
            ht.close()
        with open(htmltext, 'r') as ht2:
            info = ht2.readlines()
            ht2.close()
    elif selected_prod == 'SL':
        line1 = overall_sl['condition']
        line2 = overall_sl['metric']
        line3 = overall_sl['callouts']['OVERALL']
        line4 = overall_sl['callouts']['OVERALL TREND']
        with open(htmltext, 'r+') as ht:
            ht.truncate(0)
            # htmlwrite_o(overall_sl, 'OVERALL', ht)
            htmlwrite(storage_sl, 'Storage', ht)
            htmlwrite(server_sl, 'Server', ht)
            htmlwrite(networking_sl, 'Networking', ht)
            htmlwrite(pri_storage_sl, 'Primary_Storage', ht)
            htmlwrite(other_sl, 'Other', ht)
            htmlwrite(midrange_sl, 'Midrange', ht)
            htmlwrite(hci_cloud_sl, 'HCI_Cloud', ht)
            htmlwrite(dpd_uds_sl, 'DPD_UDS', ht)
            ht.close()
        with open(htmltext, 'r') as ht2:
            info = ht2.readlines()
            ht2.close()
    elif selected_prod == 'AHT':
        line1 = overall_aht['condition']
        line2 = overall_aht['metric']
        line3 = overall_aht['callouts']['OVERALL']
        line4 = overall_aht['callouts']['OVERALL TREND']
        with open(htmltext, 'r+') as ht:
            ht.truncate(0)
            # htmlwrite_o(overall_aht, 'OVERALL', ht)
            htmlwrite(storage_aht, 'Storage', ht)
            htmlwrite(server_aht, 'Server', ht)
            htmlwrite(networking_aht, 'Networking', ht)
            htmlwrite(pri_storage_aht, 'Primary_Storage', ht)
            htmlwrite(other_aht, 'Other', ht)
            htmlwrite(midrange_aht, 'Midrange', ht)
            htmlwrite(hci_cloud_aht, 'HCI_Cloud', ht)
            htmlwrite(dpd_uds_aht, 'DPD_UDS', ht)
            ht.close()
        with open(htmltext, 'r') as ht2:
            info = ht2.readlines()
            ht2.close()
    elif selected_prod == 'TTC':
        line1 = overall_ttc['condition']
        line2 = overall_ttc['metric']
        line3 = overall_ttc['callouts']['OVERALL']
        line4 = overall_ttc['callouts']['OVERALL TREND']
        with open(htmltext, 'r+') as ht:
            ht.truncate(0)
            # htmlwrite_o(overall_ttc, 'OVERALL', ht)
            htmlwrite(storage_ttc, 'Storage', ht)
            htmlwrite(server_ttc, 'Server', ht)
            htmlwrite(networking_ttc, 'Networking', ht)
            htmlwrite(pri_storage_ttc, 'Primary_Storage', ht)
            htmlwrite(other_ttc, 'Other', ht)
            htmlwrite(midrange_ttc, 'Midrange', ht)
            htmlwrite(hci_cloud_ttc, 'HCI_Cloud', ht)
            htmlwrite(dpd_uds_ttc, 'DPD_UDS', ht)
            ht.close()
        with open(htmltext, 'r') as ht2:
            info = ht2.readlines()
            ht2.close()
    elif selected_prod == 'TTR':
        line1 = overall_ttr['condition']
        line2 = overall_ttr['metric']
        line3 = overall_ttr['callouts']['OVERALL']
        line4 = overall_ttr['callouts']['OVERALL TREND']
        with open(htmltext, 'r+') as ht:
            ht.truncate(0)
            # htmlwrite_o(overall_ttr, 'OVERALL', ht)
            htmlwrite(storage_ttr, 'Storage', ht)
            htmlwrite(server_ttr, 'Server', ht)
            htmlwrite(networking_ttr, 'Networking', ht)
            htmlwrite(pri_storage_ttr, 'Primary_Storage', ht)
            htmlwrite(other_ttr, 'Other', ht)
            htmlwrite(midrange_ttr, 'Midrange', ht)
            htmlwrite(hci_cloud_ttr, 'HCI_Cloud', ht)
            htmlwrite(dpd_uds_ttr, 'DPD_UDS', ht)
            ht.close()
        with open(htmltext, 'r') as ht2:
            info = ht2.readlines()
            ht2.close()
    elif selected_prod == 'OTS':
        line1 = overall_ots['condition']
        line2 = overall_ots['metric']
        line3 = overall_ots['callouts']['OVERALL']
        line4 = overall_ots['callouts']['OVERALL TREND']
        with open(htmltext, 'r+') as ht:
            ht.truncate(0)
            # htmlwrite_o(overall_ots, 'OVERALL', ht)
            htmlwrite(storage_ots, 'Storage', ht)
            htmlwrite(server_ots, 'Server', ht)
            htmlwrite(networking_ots, 'Networking', ht)
            htmlwrite(pri_storage_ots, 'Primary_Storage', ht)
            htmlwrite(other_ots, 'Other', ht)
            htmlwrite(midrange_ots, 'Midrange', ht)
            htmlwrite(hci_cloud_ots, 'HCI_Cloud', ht)
            htmlwrite(dpd_uds_ots, 'DPD_UDS', ht)
            ht.close()
        with open(htmltext, 'r') as ht2:
            info = ht2.readlines()
            ht2.close()
    elif selected_prod == 'PI':
        line1 = overall_pi['condition']
        line2 = overall_pi['metric']
        line3 = overall_pi['callouts']['OVERALL']
        line4 = overall_pi['callouts']['OVERALL TREND']
        with open(htmltext, 'r+') as ht:
            ht.truncate(0)
            # htmlwrite_o(overall_pi, 'OVERALL', ht)
            htmlwrite(storage_pi, 'Storage', ht)
            htmlwrite(server_pi, 'Server', ht)
            htmlwrite(networking_pi, 'Networking', ht)
            htmlwrite(pri_storage_pi, 'Primary_Storage', ht)
            htmlwrite(other_pi, 'Other', ht)
            htmlwrite(midrange_pi, 'Midrange', ht)
            htmlwrite(hci_cloud_pi, 'HCI_Cloud', ht)
            htmlwrite(dpd_uds_pi, 'DPD_UDS', ht)
            ht.close()
        with open(htmltext, 'r') as ht2:
            info = ht2.readlines()
            ht2.close()
    elif selected_prod == 'CSAT-PRO':
        line1 = overall_csatp['condition']
        line2 = overall_csatp['metric']
        line3 = overall_csatp['callouts']['OVERALL']
        line4 = overall_csatp['callouts']['OVERALL TREND']
        with open(htmltext, 'r+') as ht:
            ht.truncate(0)
            # htmlwrite_o(overall_csatp, 'OVERALL', ht)
            htmlwrite(storage_csatp, 'Storage', ht)
            htmlwrite(server_csatp, 'Server', ht)
            htmlwrite(networking_csatp, 'Networking', ht)
            htmlwrite(pri_storage_csatp, 'Primary_Storage', ht)
            htmlwrite(other_csatp, 'Other', ht)
            htmlwrite(midrange_csatp, 'Midrange', ht)
            htmlwrite(hci_cloud_csatp, 'HCI_Cloud', ht)
            htmlwrite(dpd_uds_csatp, 'DPD_UDS', ht)
            ht.close()
        with open(htmltext, 'r') as ht2:
            info = ht2.readlines()
            ht2.close()
    elif selected_prod == 'CSAT-BASIC':
        line1 = overall_csatb['condition']
        line2 = overall_csatb['metric']
        line3 = overall_csatb['callouts']['OVERALL']
        line4 = overall_csatb['callouts']['OVERALL TREND']
        with open(htmltext, 'r+') as ht:
            ht.truncate(0)
            # htmlwrite_o(overall_csatb, 'OVERALL', ht)
            htmlwrite(storage_csatb, 'Storage', ht)
            htmlwrite(server_csatb, 'Server', ht)
            htmlwrite(networking_csatb, 'Networking', ht)
            htmlwrite(pri_storage_csatb, 'Primary_Storage', ht)
            htmlwrite(other_csatb, 'Other', ht)
            htmlwrite(midrange_csatb, 'Midrange', ht)
            htmlwrite(hci_cloud_csatb, 'HCI_Cloud', ht)
            htmlwrite(dpd_uds_csatb, 'DPD_UDS', ht)
            ht.close()
        with open(htmltext, 'r') as ht2:
            info = ht2.readlines()
            ht2.close()
    elif selected_prod == 'DSAT-PRO':
        line1 = overall_dsatp['condition']
        line2 = overall_dsatp['metric']
        line3 = overall_dsatp['callouts']['OVERALL']
        line4 = overall_dsatp['callouts']['OVERALL TREND']
        with open(htmltext, 'r+') as ht:
            ht.truncate(0)
            # htmlwrite_o(overall_dsatp, 'OVERALL', ht)
            htmlwrite(storage_dsatp, 'Storage', ht)
            htmlwrite(server_dsatp, 'Server', ht)
            htmlwrite(networking_dsatp, 'Networking', ht)
            htmlwrite(pri_storage_dsatp, 'Primary_Storage', ht)
            htmlwrite(other_dsatp, 'Other', ht)
            htmlwrite(midrange_dsatp, 'Midrange', ht)
            htmlwrite(hci_cloud_dsatp, 'HCI_Cloud', ht)
            htmlwrite(dpd_uds_dsatp, 'DPD_UDS', ht)
            ht.close()
        with open(htmltext, 'r') as ht2:
            info = ht2.readlines()
            ht2.close()
    elif selected_prod == 'DSAT-BASIC':
        line1 = overall_dsatb['condition']
        line2 = overall_dsatb['metric']
        line3 = overall_dsatb['callouts']['OVERALL']
        line4 = overall_dsatb['callouts']['OVERALL TREND']
        with open(htmltext, 'r+') as ht:
            ht.truncate(0)
            # htmlwrite_o(overall_dsatb, 'OVERALL', ht)
            htmlwrite(storage_dsatb, 'Storage', ht)
            htmlwrite(server_dsatb, 'Server', ht)
            htmlwrite(networking_dsatb, 'Networking', ht)
            htmlwrite(pri_storage_dsatb, 'Primary_Storage', ht)
            htmlwrite(other_dsatb, 'Other', ht)
            htmlwrite(midrange_dsatb, 'Midrange', ht)
            htmlwrite(hci_cloud_dsatb, 'HCI_Cloud', ht)
            htmlwrite(dpd_uds_dsatb, 'DPD_UDS', ht)
            ht.close()
        with open(htmltext, 'r') as ht2:
            info = ht2.readlines()
            ht2.close()
    elif selected_prod == 'PL':
        line1 = overall_pl['condition']
        line2 = overall_pl['metric']
        line3 = overall_pl['callouts']['OVERALL']
        line4 = overall_pl['callouts']['OVERALL TREND']
        with open(htmltext, 'r+') as ht:
            ht.truncate(0)
            # htmlwrite_o(overall_pl, 'OVERALL', ht)
            htmlwrite(storage_pl, 'Storage', ht)
            htmlwrite(server_pl, 'Server', ht)
            htmlwrite(networking_pl, 'Networking', ht)
            htmlwrite(pri_storage_pl, 'Primary_Storage', ht)
            htmlwrite(other_pl, 'Other', ht)
            htmlwrite(midrange_pl, 'Midrange', ht)
            htmlwrite(hci_cloud_pl, 'HCI_Cloud', ht)
            htmlwrite(dpd_uds_pl, 'DPD_UDS', ht)
            ht.close()
        with open(htmltext, 'r') as ht2:
            info = ht2.readlines()
            ht2.close()
    elif selected_prod == 'SLO':
        line1 = overall_slo['condition']
        line2 = overall_slo['metric']
        line3 = overall_slo['callouts']['OVERALL']
        line4 = overall_slo['callouts']['OVERALL TREND']
        with open(htmltext, 'r+') as ht:
            ht.truncate(0)
            # htmlwrite_o(overall_slo, 'OVERALL', ht)
            htmlwrite(storage_slo, 'Storage', ht)
            htmlwrite(server_slo, 'Server', ht)
            htmlwrite(networking_slo, 'Networking', ht)
            htmlwrite(pri_storage_slo, 'Primary_Storage', ht)
            htmlwrite(other_slo, 'Other', ht)
            htmlwrite(midrange_slo, 'Midrange', ht)
            htmlwrite(hci_cloud_slo, 'HCI_Cloud', ht)
            htmlwrite(dpd_uds_slo, 'DPD_UDS', ht)
            ht.close()
        with open(htmltext, 'r') as ht2:
            info = ht2.readlines()
            ht2.close()
    elif selected_prod == 'AOP':
        line1 = overall_aop['condition']
        line2 = overall_aop['metric']
        line3 = overall_aop['callouts']['OVERALL']
        line4 = overall_aop['callouts']['OVERALL TREND']
        with open(htmltext, 'r+') as ht:
            ht.truncate(0)
            # htmlwrite_o(overall_aop, 'OVERALL', ht)
            htmlwrite(storage_aop, 'Storage', ht)
            htmlwrite(server_aop, 'Server', ht)
            htmlwrite(networking_aop, 'Networking', ht)
            htmlwrite(pri_storage_aop, 'Primary_Storage', ht)
            htmlwrite(other_aop, 'Other', ht)
            htmlwrite(midrange_aop, 'Midrange', ht)
            htmlwrite(hci_cloud_aop, 'HCI_Cloud', ht)
            htmlwrite(dpd_uds_aop, 'DPD_UDS', ht)
            ht.close()
        with open(htmltext, 'r') as ht2:
            info = ht2.readlines()
            ht2.close()
    elif selected_prod == 'RDR':
        line1 = overall_rdr['condition']
        line2 = overall_rdr['metric']
        line3 = overall_rdr['callouts']['OVERALL']
        line4 = overall_rdr['callouts']['OVERALL TREND']
        with open(htmltext, 'r+') as ht:
            ht.truncate(0)
            # htmlwrite_o(overall_rdr, 'OVERALL', ht)
            htmlwrite(storage_rdr, 'Storage', ht)
            htmlwrite(server_rdr, 'Server', ht)
            htmlwrite(networking_rdr, 'Networking', ht)
            htmlwrite(pri_storage_rdr, 'Primary_Storage', ht)
            htmlwrite(other_rdr, 'Other', ht)
            htmlwrite(midrange_rdr, 'Midrange', ht)
            htmlwrite(hci_cloud_rdr, 'HCI_Cloud', ht)
            htmlwrite(dpd_uds_rdr, 'DPD_UDS', ht)
            ht.close()
        with open(htmltext, 'r') as ht2:
            info = ht2.readlines()
            ht2.close()
    return line1,line2, line3, line4, info

@app.callback(
    [Output('trends', 'figure'),
    Output('quartertrends', 'figure'),
    Output('yearesg', 'figure'),
    Output('yearhes', 'figure')],
    [Input('calls_selection', 'value')]
)
def update_graph(selected_metric):
    fig = px.line()
    fig2 = px.bar()
    num, denom = 'CSAT_NUM','CSAT_DENOM'
    if selected_metric == 'CSAT':
        num = 'CSAT_NUM'
        denom = 'CSAT_DENOM'
    elif selected_metric == 'DSAT':
        num = 'DSAT_NUM'
        denom = 'DSAT_DENOM'
    elif selected_metric == 'OBL':
        num = 'Backlog_NUM'
        denom = 'Backlog_DENOM'
    elif selected_metric == 'SL':
        num = 'SL_NUM'
        denom = 'SL_DENOM'
    elif selected_metric == 'AHT':
        num = 'AHT_NUM'
        denom = 'AHT_DENOM'
    elif selected_metric == 'RDR':
        num = 'RDR_NUM'
        denom = 'RDR_DENOM'
    elif selected_metric == 'TTC':
        num = 'TTC_NUM'
        denom = 'TTC_DENOM'
    elif selected_metric == 'TTR':
        num = 'TTR_NUM'
        denom = 'TTR_DENOM'
    elif selected_metric == 'PI':
        num = 'PI_NUM'
        denom = 'PI_DENOM'
    elif selected_metric == 'CSAT-PRO':
        num = 'CSAT_NUM_PRO'
        denom = 'CSAT_DENOM_PRO'
    elif selected_metric == 'CSAT-BASIC':
        num = 'CSAT_NUM_BASIC'
        denom = 'CSAT_DENOM_BASIC'
    elif selected_metric == 'DSAT-PRO':
        num = 'DSAT_NUM_PRO'
        denom = 'DSAT_DENOM_PRO'
    elif selected_metric == 'DSAT-BASIC':
        num = 'DSAT_NUM_BASIC'
        denom = 'DSAT_DENOM_BASIC'
    elif selected_metric == 'SLO':
        num = 'SEV1_SLO_NUM'
        denom = 'SEV1_SLO_DENOM'
    elif selected_metric == 'AOP':
        num = 'AOP_NUM'
        denom = 'AOP_DENOM'
    elif selected_metric == 'PL':
        num = 'PLAN_NUM'
        denom = 'PLAN_DENOM'
    # primary data source for all weeks, quarters, and years
    # add or remove any columns here to be included in the dataset.
    # NOTE: only numeric columns will be aggregated, if you want non numeric columns to be included, then you will have to
    # include them in the index and then reset_index() will bring the data into the columns.
    # WARNING: DASH DOES NOT SUPPORT MULTI INDEX AS YET.
    # XXX: following is an example to include product_type
    # filtered_df = df.loc[(df['Fiscal_Quarter_Lag'] == 0) | (df['Fiscal_Quarter_Lag'] == -1) | (df['Fiscal_Quarter_Lag'] == -2) | (df['Fiscal_Quarter_Lag'] == -3) ][['Fiscal_Quarter_Lag','Fiscal_Quarter','Fiscal_Week','Product_Type',num, denom]]
    # XXX: end of example
    filtered_df = df.loc[(df['Fiscal_Quarter_Lag'] == 0) | (df['Fiscal_Quarter_Lag'] == -1) | (df['Fiscal_Quarter_Lag'] == -2) | (df['Fiscal_Quarter_Lag'] == -3) ][['Fiscal_Quarter_Lag','Fiscal_Quarter','Fiscal_Week',num, denom]]
    # weekly trend lines
    fdf = filtered_df.groupby(['Fiscal_Quarter_Lag', 'Fiscal_Quarter', 'Fiscal_Week']).agg({num:[sum], denom:[sum]})
    fdf.columns = [num,denom]
    fdf = fdf.reset_index()
    if selected_metric in ['TTC', 'TTR','AHT','PI', 'PL', 'AOP']:
        fdf[selected_metric] = round(fdf[num]/fdf[denom], 2)
    else:
        fdf[selected_metric] = round(fdf[num]/fdf[denom]*100, 2)
    # QUARTERLY DATA
    # can get teh product type in to the mix by using the following line in the comment. can use it in the bar chart
    # for seperating the product with colors.
    # fdf2 = filtered_df.groupby(['Fiscal_Quarter_Lag', 'Fiscal_Quarter', 'Product_Type']).agg({num:[sum], denom:[sum]})
    fdf2 = filtered_df.groupby(['Fiscal_Quarter_Lag', 'Fiscal_Quarter']).agg({num:[sum], denom:[sum]})
    fdf2.columns = [num,denom]
    fdf2 = fdf2.reset_index()
    if selected_metric in ['TTC', 'TTR','AHT','PI', 'PL', 'AOP']:
        fdf2[selected_metric] = round(fdf2[num]/fdf2[denom], 2)
    else:
        fdf2[selected_metric] = round(fdf2[num]/fdf2[denom]*100, 2)
    # YEARLY DATA DIVIDED INTO ESG AND HES
    # ESG
    filtered_df_year_esg = df.loc[df['Product_Type'] == 'ESG'][['Fiscal_Quarter_Lag', 'Fiscal_Year','Fiscal_Quarter','Fiscal_Week',num, denom]]
    filtered_df_year_hes = df.loc[df['Product_Type'] == 'HES'][['Fiscal_Quarter_Lag', 'Fiscal_Year','Fiscal_Quarter','Fiscal_Week',num, denom]]
    fdf3 = filtered_df_year_esg.groupby(['Fiscal_Year']).agg({num:[sum], denom:[sum]})
    fdf3.columns = [num,denom]
    fdf3 = fdf3.reset_index()
    if selected_metric in ['TTC', 'TTR','AHT','PI', 'PL', 'AOP']:
        fdf3[selected_metric] = round(fdf3[num]/fdf3[denom], 2)
    else:
        fdf3[selected_metric] = round(fdf3[num]/fdf3[denom]*100, 2)
    # HES
    fdf4 = filtered_df_year_hes.groupby(['Fiscal_Year']).agg({num:[sum], denom:[sum]})
    fdf4.columns = [num,denom]
    fdf4 = fdf4.reset_index()
    if selected_metric in ['TTC', 'TTR','AHT','PI', 'PL', 'AOP']:
        fdf4[selected_metric] = round(fdf4[num]/fdf4[denom], 2)
    else:
        fdf4[selected_metric] = round(fdf4[num]/fdf4[denom]*100, 2)
    # filtered_df['CSAT'] = round(filtered_df['CSAT_NUM']/filtered_df['CSAT_DENOM']*100, 2)
    # filtered_df2 = filtered_df.loc[:,['Fiscal_Quarter_Lag', 'Fiscal_Week', 'CSAT_NUM', 'CSAT_DENOM', 'Backlog_NUM', 'Backlog_DENOM']]
    # filtered_df2['CSAT'] = round(filtered_df2['CSAT_NUM']/filtered_df2['CSAT_DENOM']*100, 2)
    # filtered_df2['OBL'] = round(filtered_df2['Backlog_NUM']/filtered_df2['Backlog_DENOM']*100, 2)
    fig = px.line(fdf, x = 'Fiscal_Week', y = selected_metric)
    fig.update_layout(transition_duration = 500)
    fig2 = px.bar(fdf2, x='Fiscal_Quarter', y = selected_metric) #, color = 'Product_Type')
    fig2.update_layout(transition_duration = 500)
    fig3 = px.bar(fdf3, x='Fiscal_Year', y = selected_metric)
    fig3.update_layout(transition_duration = 500)
    fig4 = px.bar(fdf4, x='Fiscal_Year', y = selected_metric)
    fig4.update_layout(transition_duration = 500)
    # fig = px.line(csz2, x = 'BMS_Product', y= 'Fiscal_Week')
    return fig, fig2, fig3, fig4


if __name__ == '__main__':
    app.run_server(debug=True)

# print('the data is {} for week {}'.format(obl_table4['latestweekdata'].iterrows(), obl_table4['weekname']))

########### THIS WORKS IN A WEIRD WAY
# for i in obl_table4['latestweekdata']:
#     if i < 0:
#         for j in obl_table4['trendd3']:
#             if j < 0:
#                 print('The data is up for prod {} region {} and has a trend'.format(obl_table4.index.get_level_values(0).values, obl_table4.index.get_level_values(1).values))
#     else:
#         print("The week is down")
###########################################################################

# table2 = pd.pivot_table(df, values = ['Backlog_NUM','Backlog_DENOM','OBL'], columns = ['Fiscal_Week'], index = ['BMS_Product','BMS_Region'], aggfunc={'Backlog_NUM':np.sum, 'Backlog_DENOM':np.sum, 'OBL': })
# table.columns.get_level_values(level=0).names = ['Backlog']
# table.columns.names
#
#
# newcols = pd.MultiIndex.from_product((['Backlog_NUM', 'Backlog_DENOM'], table.columns.get_level_values(level=1)))
# newcols


# region subset
# nafilters = df.loc[:,'BMS_Region'] == 'NA'
# newindex = df.set_index('BMS_Region')
# r_na_bl = df.loc[df['BMS_Region'] == 'NA', ['Fiscal_Year','Fiscal_Quarter','Fiscal_Week','BMS_Region','Backlog_NUM', 'Backlog_DENOM']]
#
# r_na_bl['obl'] = (df['Backlog_NUM']/df['Backlog_DENOM']*100, 2)

# rna_group = r_na_bl.groupby(['Fiscal_Year','Fiscal_Quarter', 'BMS_Region', 'Fiscal_Week']).agg({''})
