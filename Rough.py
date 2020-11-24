import win32com.client as win32

xl = win32.DispatchEx('Excel.Application')
xl.DisplayAlerts = True
xl.Visible = True


file = r'D:\git_stuff\Development\ACallouts\ISG_BMS.xlsx'

wb1 = xl.Workbooks.Open(Filename = file, ReadOnly = False)
for conn in wb1.connections:
    print(conn.OLEDBConnection.CommandText)
