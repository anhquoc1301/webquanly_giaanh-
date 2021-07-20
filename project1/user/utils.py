import pandas as pd
from openpyxl import load_workbook
import xlsxwriter

def load_configure(excel_path):
    return pd.read_excel(excel_path)

def save_excel(df, excel_path):
    df1 = pd.DataFrame(df)
    df1.to_excel(excel_path, index=False, header=True)

# df = load_configure(r'danhsachbienso.xlsx')
# df1 = pd.DataFrame([{"No" : 1, "Name" : "Name1"}, {"No" : 3, "Name" : "Name3"}])
# df1.to_excel("output.xlsx", index=False)  

def save_xlsx(df, excel_path):
    workbook = xlsxwriter.Workbook(excel_path)
    worksheet = workbook.add_worksheet()
    # Widen column A for extra visibility.
    worksheet.set_column('A:A', 30)

    # A number to convert to a date.
    number = 41333.5
    # Write it as a number without formatting.
    worksheet.write('A1', number)                # 41333.5
    format2 = workbook.add_format({'num_format': 'dd/mm/yy'})
    worksheet.write('A2', number, format2)       # 28/02/13

    format3 = workbook.add_format({'num_format': 'mm/dd/yy'})
    worksheet.write('A3', number, format3)       # 02/28/13

    format4 = workbook.add_format({'num_format': 'hh:mm'})
    worksheet.write('A4', number, format4)       # 28-2-2013

    format5 = workbook.add_format({'num_format': 'hh:mm'})
    worksheet.write('A5', number, format5)       # 28/02/13 12:00

    format6 = workbook.add_format({'num_format': 'd mmm yyyy'})
    worksheet.write('A6', number, format6)       # 28 Feb 2013

    format7 = workbook.add_format({'num_format': 'mmm d yyyy hh:mm AM/PM'})
    worksheet.write('A7', number, format7)       # Feb 28 2013 12:00 PM
    workbook.close()
