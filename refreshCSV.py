import pandas as pd
import numpy as np
import pyodbc as odd

file = r'D:\git_stuff\Development\ACallouts\sources1.csv'

# loop through all the drivers we have access to
# for driver in odd.drivers():
#     print(driver)

# define the server and the database names
server = 'gronksmash.amer.dell.com'
database = 'SDS_COMMERCIAL_GSA'

# connection string
cnxn = odd.connect('DRIVER={ODBC Driver 17 for SQL Server};\
                    SERVER='+server+'; \
                    DATABASE='+database+'; \
                    Trusted_Connection=yes;')

# create the connection cursor
cursor = cnxn.cursor()

# refresh the file
select_query = '''select * from SDS_COMMERCIAL_GSA.dbo.vw_tj_Task11510_ISG_BMS'''

# '''select * from SDS_COMMERCIAL_GSA.dbo.vw_tj_Task11510_ISG_BMS bems where bems.[Agent Group Name] in ('Commercial Enterprise Services', 'Infrastructure Solutions Group', 'High End Storage')'''
# cursor.execute(select_query)
# cnxn.commit()

# get results
# res = cursor.fetchall()

df_table = pd.read_sql_query(select_query, cnxn)

df_table.to_csv(file, index=False)
