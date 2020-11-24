import sys
import pandas as pd
import numpy as np

#data import section
data = (r'D:\git_stuff\Development\ACallouts\sources.csv')
df=pd.read_csv(data, keep_default_na=False, float_precision=2)

# for julie to look at this and understand where she needs to point fingers at.

# extract required information like latest week and column names etc
colnames = df.columns
index = df.index
latestweek = df['Fiscal_Week'].max()
prevnbr = int(latestweek[-2:])-1
prevweek = latestweek.replace(latestweek[-2:], str(prevnbr))
uniqueweeks = df['Fiscal_Week'].unique()
ncols = ['EOQ_FLAG', 'China_Flag', 'CSAT_NUM','CSAT_DENOM', 'RDR_NUM', 'RDR_DENOM', 'TTC_NUM', 'TTC_DENOM','Backlog_NUM', 'Backlog_DENOM', 'DSAT_NUM', 'DSAT_DENOM', 'TTR_NUM','TTR_DENOM', 'PI_NUM', 'PI_DENOM', 'OTS_NUM', 'OTS_DENOM', 'SL_NUM','SL_DENOM', 'AHT_NUM', 'AHT_DENOM', 'CSAT_NUM_PRO', 'CSAT_DENOM_PRO','CSAT_NUM_BASIC', 'CSAT_DENOM_BASIC', 'DSAT_NUM_PRO', 'DSAT_DENOM_PRO','DSAT_NUM_BASIC', 'DSAT_DENOM_BASIC', 'PLAN_NUM', 'PLAN_DENOM','SEV1_SLO_NUM', 'SEV1_SLO_DENOM', 'AOP_NUM', 'AOP_DENOM']

# latest week subset
# df_lw = df.loc[df['Fiscal_Week'] == latestweek]
# df_lw.head()
df[ncols] = df[ncols].apply(pd.to_numeric, downcast='unsigned')
df1 = df.loc[df['Fiscal_Week_Lag']>= -13,:]

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
#---------------------------------
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
    table = pd.pivot_table(x, values = list, columns = list2, index = list3, aggfunc={agre:np.sum, agre2:np.sum}, margins=True, margins_name='Grand_Total')

    subtable = pd.concat([
    d.append(d.sum().rename((k, k)))
    for k, d in table.groupby(level = 0)
    ])
    #.append(table.sum().rename(('Grand', 'Total')))
    # removed this part since i have the margins=True column included, this just adds the grand total to the table

    newtable = round(subtable[agre]/subtable[agre2]*100, 1)
    newtable = newtable.sort_index(ascending = False)
    return newtable

def pivoted_np(x, list, list2, list3):
    agre = list[0]
    agre2 = list[1]
    table = pd.pivot_table(x, values = list, columns = list2, index = list3, aggfunc={agre:np.sum, agre2:np.sum}, margins=True, margins_name='Grand_Total')

    subtable = pd.concat([
    d.append(d.sum().rename((k, k)))
    for k, d in table.groupby(level = 0)
    ])
    #.append(table.sum().rename(('Grand', 'Total')))
    # removed this part since i have the margins=True column included, this just adds the grand total to the table

    newtable = round(subtable[agre]/subtable[agre2], 1)
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

# format to enter the data is (dataframe, values, columns, index)
obl_table = pivoted(df1, obl, weeks, prod_region)
cs_table = pivoted(df1, cs, weeks, prod_region)
ttc_table = pivoted_np(df1, ttc, weeks, prod_region)


# FINAL PIVOTED DATA IS AVAILABLE FROM HERE

# original way i did it.
# lwdata = obl_table.iloc[:,12].astype(float)
# pwdata = obl_table.iloc[:,11].astype(float)
# differences = lwdata-pwdata
# obl2 = obl_table.assign(pweek_diff = differences)

# define function to add the additional columns to the data so that it can be used on multiple metrics
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

oblz = add_cols(obl_table)
csz = add_cols(cs_table)
ttcz = add_cols(ttc_table)

# product separated data
# can use this to print the callouts separately
def seperate(grouped_table, the_table_to_check):
    for i, j in the_table_to_check.groupby(level=0):
        if i in grouped_table:
            print(i)
            obl66 = j
    return obl66

# OBL
ostorage = seperate('Storage', oblz)
oDPD_UDS = seperate('DPD/UDS', oblz)
ohci_cloud = seperate('HCI & Cloud', oblz)
omidrange = seperate('Midrange', oblz)
onetoworking = seperate('Networking', oblz)
oothers = seperate('Other', oblz)
opri_storage = seperate('Primary Storage', oblz)
oserver = seperate('Server', oblz)
ooverall = seperate('Grand_Total', oblz)

# CSAT
cstorage = seperate('Storage', csz)
cDPD_UDS = seperate('DPD/UDS', csz)
chci_cloud = seperate('HCI & Cloud', csz)
cmidrange = seperate('Midrange', csz)
cnetoworking = seperate('Networking', csz)
cothers = seperate('Other', csz)
cpri_storage = seperate('Primary Storage', csz)
cserver = seperate('Server', csz)
coverall = seperate('Grand_Total', csz)

# TTC
tstorage = seperate('Storage', ttcz)
tDPD_UDS = seperate('DPD/UDS', ttcz)
thci_cloud = seperate('HCI & Cloud', ttcz)
tmidrange = seperate('Midrange', ttcz)
tnetoworking = seperate('Networking', ttcz)
tothers = seperate('Other', ttcz)
tpri_storage = seperate('Primary Storage', ttcz)
tserver = seperate('Server', ttcz)
toverall = seperate('Grand_Total', ttcz)


# the following unpacks everything from the dataframe into strings, so that it is easy to display
# if a a table is required then i can simply use the obl66
# print(name)
def calls(y):
    obl66 = y
    # dir = obl66.iloc[1,2]
    for index, row in obl66.iterrows():
        print(index[1], row['direction'], round(row['latestweekdata'],2), row['weekname'], row['at'], row[1])
        if row['trendd3'] != 0:
            print(" 3week down trend at ", round(row['trendd3'], 2))
        elif row['trendu3'] != 0:
            print("  3week up trend at ", round(row['trendu3'], 2))
        elif row['trendd4'] != 0:
            print("  4week down trend at ", round(row['trendd4'], 2))
        elif row['trendu4'] != 0:
            print("  4week up trend at ", round(row['trendu4'], 2))
        elif row['trendd5'] != 0:
            print("  5week down trend at ", round(row['trendd5'], 2))
        elif row['trendu5'] != 0:
            print("  5week up trend at ", round(row['trendu5'], 2))
        elif row['trendd6'] != 0:
            print("  6week down trend at ", round(row['trendd6'], 2))
        elif row['trendu6'] != 0:
            print("  6week up trend at ", round(row['trendu6'], 2))
    return str

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

def high(product, prod_name, meter):
    d = "Down"
    dir = product.loc[(product.index.get_level_values('BMS_Region') == prod_name)]['direction'].values
    dir = str(dir[0])
    if d in dir:
        print("{} callouts".format(prod_name))
        print('Highlight')
        print("\n")
        print(meter)
        calls(product)
        print("\n")
        # print("\n")
        # print(product[1])
        # calls(product[1])
    else:
        print("{} callouts".format(prod_name))
        print("Opportunities")
        print("\n")
        print(meter)
        calls(product)
        print("\n")
        # print("\n")
        # print(product[1])
        # calls(product[1])
    return None

high(ostorage, 'Storage', 'obl')
high(cstorage, 'Storage', 'CSAT')
high(tstorage, 'Storage', 'TTC')
high(oserver, 'Server', 'obl')
high(cserver, 'Server', 'CSAT')
high(tserver, 'Server', 'TTC')
high(oothers, 'Other', 'obl')
high(cothers, 'Other', 'CSAT')
high(tothers, 'Other', 'TTC')





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
