# Script tổng hợp để sửa tất cả lỗi và tạo lại tất cả biểu đồ nha
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
import os
warnings.filterwarnings('ignore')

# Tạo thư mục image nếu chưa có
if not os.path.exists('image'):
    os.makedirs('image')
    print("Đã tạo thư mục image")

# Cấu hình hiển thị
plt.style.use('default')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10
sns.set_palette('husl')

print("Đang đọc dữ liệu...")
# Đọc dữ liệu từ sheet 'table'
file_path = 'file xu li du lieu.xlsx'
df = pd.read_excel(file_path, sheet_name='table')

print("Tên các cột:", df.columns.tolist())
print("Số dòng dữ liệu:", len(df))

# ===== 1. TÍNH TOÁN CÁC DATAFRAME CẦN THIẾT =====
print("\n1. Đang tính toán doanh thu theo nguồn...")
# Tính doanh thu theo nguồn (sửa tên cột)
doanh_thu_theo_nguon = df.groupby('noi gioi thieu').agg({
    'so luong': 'sum',  # Có dấu cách ở cuối
    'doanh thu': 'sum'
}).sort_values('doanh thu', ascending=False)

# Đổi tên cột để dễ sử dụng
doanh_thu_theo_nguon.columns = ['so luong', 'doanh thu']

print("\n2. Đang tính toán hiệu suất nguồn...")
# Tính hiệu suất nguồn
hieu_suat_nguon = df.groupby('noi gioi thieu').agg({
    'so luong': 'sum',
    'doanh thu': 'sum'
}).reset_index()
hieu_suat_nguon.columns = ['noi gioi thieu', 'so luong', 'doanh thu']
hieu_suat_nguon['trung binh'] = hieu_suat_nguon['doanh thu'] / hieu_suat_nguon['so luong']

print("\n3. Đang tính toán doanh thu theo tháng...")
# Tính doanh thu theo tháng
doanh_thu_theo_thang = df.groupby('thang').agg({
    'so luong': 'sum',
    'doanh thu': 'sum'
}).reset_index()
doanh_thu_theo_thang.columns = ['thang', 'so luong', 'doanh thu']

# ===== 2. TẠO CÁC PIVOT TABLE =====
print("\n4. Đang tạo pivot tables...")
# Pivot table cho heatmap (KHÔNG FORMAT)
pivot_for_heatmap = df.pivot_table(
    values='doanh thu', 
    index='noi gioi thieu', 
    columns='thang', 
    aggfunc='sum', 
    fill_value=0
)

# Pivot table cho hiển thị (CÓ FORMAT)
pivot_doanh_thu = df.pivot_table(
    values='doanh thu', 
    index='noi gioi thieu', 
    columns='thang', 
    aggfunc='sum', 
    fill_value=0
)

# Format pivot table cho hiển thị
for col in pivot_doanh_thu.columns:
    pivot_doanh_thu[col] = pivot_doanh_thu[col].apply(lambda x: f'{x:,.0f}' if x > 0 else '0')

# Lấy top 10 cho cả hai pivot table
top_10_names = doanh_thu_theo_nguon.head(10).index
pivot_heatmap_top10 = pivot_for_heatmap.loc[top_10_names]
pivot_top_10 = pivot_doanh_thu.loc[top_10_names]

# ===== 3. TẠO TẤT CẢ CÁC BIỂU ĐỒ =====
print("\n5. Đang tạo biểu đồ Top 10 nguồn giới thiệu...")
# Biểu đồ Top 10 nguồn giới thiệu
plt.figure(figsize=(14, 8))
top_10 = doanh_thu_theo_nguon.head(10)
bars = plt.bar(range(len(top_10)), top_10['doanh thu'], color='skyblue', edgecolor='navy', alpha=0.7)
plt.title('Top 10 Nguồn Giới thiệu theo Doanh thu', fontsize=16, fontweight='bold')
plt.xlabel('Nguồn Giới thiệu', fontsize=12)
plt.ylabel('Doanh thu (VNĐ)', fontsize=12)

# Tạo nhãn ngắn cho trục x
short_labels = [name[:30] + '...' if len(name) > 30 else name for name in top_10.index]
plt.xticks(range(len(top_10)), short_labels, rotation=45, ha='right')

# Thêm giá trị lên đầu cột
for i, bar in enumerate(bars):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
             f'{height:,.0f}', ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.savefig('image/top_10_nguon_gioi_thieu.png', dpi=300, bbox_inches='tight')
plt.close()

print("\n6. Đang tạo biểu đồ tròn Top 5...")
# Biểu đồ tròn Top 5
plt.figure(figsize=(10, 8))
top_5 = doanh_thu_theo_nguon.head(5)
short_names = [name[:25] + '...' if len(name) > 25 else name for name in top_5.index]
colors = plt.cm.Set3(np.linspace(0, 1, len(top_5)))
wedges, texts, autotexts = plt.pie(top_5['doanh thu'], labels=short_names, autopct='%1.1f%%', 
                                   startangle=90, colors=colors)
plt.title('Top 5 Nguồn Giới thiệu theo Doanh thu', fontsize=14, fontweight='bold')
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
plt.axis('equal')
plt.tight_layout()
plt.savefig('image/top_5_pie_chart.png', dpi=300, bbox_inches='tight')
plt.close()

print("\n7. Đang tạo xu hướng doanh thu và số lượng theo tháng...")
# Xu hướng doanh thu và số lượng theo tháng
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

# Doanh thu theo tháng
ax1.plot(doanh_thu_theo_thang['thang'], doanh_thu_theo_thang['doanh thu'], 
         marker='o', linewidth=2, markersize=6, color='blue')
ax1.set_title('Xu hướng Doanh thu theo Tháng', fontsize=14, fontweight='bold')
ax1.set_ylabel('Doanh thu (VNĐ)')
ax1.grid(True, alpha=0.3)
ax1.tick_params(axis='x', rotation=45)

# Số lượng theo tháng
ax2.plot(doanh_thu_theo_thang['thang'], doanh_thu_theo_thang['so luong'], 
         marker='s', linewidth=2, markersize=6, color='green')
ax2.set_title('Xu hướng Số lượng theo Tháng', fontsize=14, fontweight='bold')
ax2.set_xlabel('Tháng')
ax2.set_ylabel('Số lượng')
ax2.grid(True, alpha=0.3)
ax2.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('image/xu_huong_thang.png', dpi=300, bbox_inches='tight')
plt.close()

print("\n8. Đang tạo heatmap...")
# Heatmap
plt.figure(figsize=(12, 10))
short_names = [name[:40] + '...' if len(name) > 40 else name for name in pivot_heatmap_top10.index]
pivot_display = pivot_heatmap_top10.copy()
pivot_display.index = short_names

sns.heatmap(pivot_display, annot=True, fmt='.0f', cmap='YlOrRd', 
            cbar_kws={'label': 'Doanh thu (VNĐ)'})
plt.title('Heatmap Doanh thu theo Nguồn Giới thiệu và Tháng (Top 10)', 
          fontsize=14, fontweight='bold')
plt.xlabel('Tháng')
plt.ylabel('Nguồn Giới thiệu')
plt.xticks(rotation=45)
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig('image/heatmap_doanh_thu.png', dpi=300, bbox_inches='tight')
plt.close()

print("\n9. Đang tạo scatter plot hiệu suất...")
# Scatter plot hiệu suất
plt.figure(figsize=(12, 8))
plt.scatter(hieu_suat_nguon['so luong'], hieu_suat_nguon['doanh thu'], 
           s=100, alpha=0.6, c='coral', edgecolors='black')
plt.title('Hiệu suất các Nguồn Giới thiệu', fontsize=14, fontweight='bold')
plt.xlabel('Số lượng')
plt.ylabel('Doanh thu (VNĐ)')
plt.grid(True, alpha=0.3)

# Thêm nhãn cho các điểm có doanh thu cao
top_sources = hieu_suat_nguon.nlargest(5, 'doanh thu')
for idx, row in top_sources.iterrows():
    name = row['noi gioi thieu'][:20] + '...' if len(row['noi gioi thieu']) > 20 else row['noi gioi thieu']
    plt.annotate(name, (row['so luong'], row['doanh thu']), 
                xytext=(5, 5), textcoords='offset points', fontsize=8)

plt.tight_layout()
plt.savefig('image/scatter_hieu_suat.png', dpi=300, bbox_inches='tight')
plt.close()

print("\n10. Đang tạo xu hướng doanh thu top 5 nguồn theo tháng...")
# Xu hướng doanh thu top 5 nguồn theo tháng
plt.figure(figsize=(14, 8))
top_5_sources = doanh_thu_theo_nguon.head(5).index

for source in top_5_sources:
    source_data = df[df['noi gioi thieu'] == source]
    monthly_data = source_data.groupby('thang')['doanh thu'].sum()
    short_name = source[:25] + '...' if len(source) > 25 else source
    plt.plot(monthly_data.index, monthly_data.values, marker='o', linewidth=2, label=short_name)

plt.title('Xu hướng Doanh thu Top 5 Nguồn theo Tháng', fontsize=14, fontweight='bold')
plt.xlabel('Tháng')
plt.ylabel('Doanh thu (VNĐ)')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('image/xu_huong_top5_thang.png', dpi=300, bbox_inches='tight')
plt.close()

print("\n11. Đang tạo xu hướng tất cả nguồn...")
# Xu hướng tất cả nguồn
plt.figure(figsize=(16, 10))
all_sources = df['noi gioi thieu'].unique()

for i, source in enumerate(all_sources):
    source_data = df[df['noi gioi thieu'] == source]
    monthly_data = source_data.groupby('thang')['doanh thu'].sum()
    plt.plot(monthly_data.index, monthly_data.values, marker='o', linewidth=1, alpha=0.7)

plt.title('Xu hướng Doanh thu Tất cả Nguồn theo Tháng', fontsize=14, fontweight='bold')
plt.xlabel('Tháng')
plt.ylabel('Doanh thu (VNĐ)')
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('image/xu_huong_tat_ca_nguon.png', dpi=300, bbox_inches='tight')
plt.close()

print("\n" + "="*50)
print("ĐÃ HOÀN THÀNH TẤT CẢ BIỂU ĐỒ!")
print("="*50)
print("Các file đã được lưu trong thư mục image/:")
print("1. top_10_nguon_gioi_thieu.png")
print("2. top_5_pie_chart.png")
print("3. xu_huong_thang.png")
print("4. heatmap_doanh_thu.png")
print("5. scatter_hieu_suat.png")
print("6. xu_huong_top5_thang.png")
print("7. xu_huong_tat_ca_nguon.png")
print("\nTất cả lỗi đã được sửa và biểu đồ đã được tạo thành công!")
