# Script để kiểm tra tên cột trong file Excel
import pandas as pd

print("Đang đọc dữ liệu...")
# Đọc dữ liệu từ sheet 'table'
file_path = 'file xu li du lieu.xlsx'
df = pd.read_excel(file_path, sheet_name='table')

print("Tên các cột trong DataFrame:")
print(df.columns.tolist())

print("\nThông tin DataFrame:")
print(df.info())

print("\n5 dòng đầu tiên:")
print(df.head())