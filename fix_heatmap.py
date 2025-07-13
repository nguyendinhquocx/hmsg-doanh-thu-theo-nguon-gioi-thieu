# Script để sửa lỗi heatmap trong notebook
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Cấu hình hiển thị
plt.style.use('default')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10
sns.set_palette('husl')

print("Đang đọc dữ liệu...")
# Đọc dữ liệu từ sheet 'table'
file_path = 'file xu li du lieu.xlsx'
df = pd.read_excel(file_path, sheet_name='table')

print("Đang tính toán doanh thu theo nguồn...")
print("Tên các cột:", df.columns.tolist())

# Tính doanh thu theo nguồn
doanh_thu_theo_nguon = df.groupby('noi gioi thieu').agg({
    'so luong ': 'sum',  # Có dấu cách ở cuối
    'doanh thu': 'sum'
}).sort_values('doanh thu', ascending=False)

print("Đang tạo pivot table cho heatmap...")
# Tạo pivot table cho heatmap (KHÔNG FORMAT)
pivot_for_heatmap = df.pivot_table(
    values='doanh thu', 
    index='noi gioi thieu', 
    columns='thang', 
    aggfunc='sum', 
    fill_value=0
)

# Chỉ lấy top 10 nguồn giới thiệu
top_10_names = doanh_thu_theo_nguon.head(10).index
pivot_heatmap_top10 = pivot_for_heatmap.loc[top_10_names]

print("Đang tạo heatmap...")
# Tạo heatmap
plt.figure(figsize=(12, 10))
short_names = [name[:40] + '...' if len(name) > 40 else name for name in pivot_heatmap_top10.index]
pivot_display = pivot_heatmap_top10.copy()
pivot_display.index = short_names

# Sử dụng dữ liệu số thực cho heatmap
sns.heatmap(pivot_display, annot=True, fmt='.0f', cmap='YlOrRd', 
            cbar_kws={'label': 'Doanh thu (VNĐ)'})
plt.title('Heatmap Doanh thu theo Nguồn Giới thiệu và Tháng (Top 10)', 
          fontsize=14, fontweight='bold')
plt.xlabel('Tháng')
plt.ylabel('Nguồn Giới thiệu')
plt.xticks(rotation=45)
plt.yticks(rotation=0)
plt.tight_layout()

print("Đang lưu heatmap...")
plt.savefig('.image/heatmap_doanh_thu.png', dpi=300, bbox_inches='tight')
plt.close()

print("Đã sửa lỗi và tạo heatmap thành công!")
print("File đã được lưu: .image/heatmap_doanh_thu.png")