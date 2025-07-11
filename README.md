# Phân tích Doanh thu theo Nguồn Giới thiệu

Dự án phân tích dữ liệu doanh thu từ các nguồn giới thiệu khác nhau sử dụng Python và Jupyter Notebook.

## Mô tả

Notebook này phân tích dữ liệu từ file Excel `file xu li du lieu.xlsx` để:
- Khám phá và làm sạch dữ liệu
- Phân tích doanh thu theo nguồn giới thiệu
- Theo dõi xu hướng theo thời gian
- Đánh giá hiệu suất các nguồn
- Tạo các biểu đồ trực quan
- Xuất báo cáo tổng hợp

## Cài đặt

### 1. Cài đặt Python
Đảm bảo bạn đã cài đặt Python 3.8 trở lên.

### 2. Cài đặt các thư viện
```bash
pip install -r requirements.txt
```

### 3. Khởi động Jupyter Notebook
```bash
jupyter notebook
```

## Sử dụng

1. Mở file `phan_tich_doanh_thu.ipynb` trong Jupyter Notebook
2. Đảm bảo file `file xu li du lieu.xlsx` có trong cùng thư mục
3. Chạy từng cell theo thứ tự từ trên xuống dưới
4. Xem các biểu đồ và kết quả phân tích
5. File báo cáo `bao_cao_phan_tich_doanh_thu.xlsx` sẽ được tạo tự động

## Cấu trúc Dữ liệu

Dữ liệu đầu vào từ sheet 'table' bao gồm:
- `noi gioi thieu`: Tên nguồn giới thiệu
- `thang`: Tháng (định dạng YYYY MM)
- `so luong`: Số lượng lượt
- `doanh thu`: Doanh thu (VNĐ)

## Kết quả Phân tích

Notebook sẽ tạo ra:
- Thống kê mô tả dữ liệu
- Top nguồn giới thiệu theo doanh thu
- Xu hướng doanh thu theo thời gian
- Heatmap doanh thu theo nguồn và tháng
- Phân tích hiệu suất (doanh thu trung bình/lượt)
- Báo cáo Excel tổng hợp

## Các Biểu đồ

1. **Biểu đồ cột ngang**: Top 10 nguồn giới thiệu
2. **Biểu đồ tròn**: Phân bố doanh thu top 5 nguồn
3. **Biểu đồ đường**: Xu hướng theo thời gian
4. **Heatmap**: Ma trận doanh thu theo nguồn và tháng
5. **Scatter plot**: Mối quan hệ số lượng vs doanh thu TB

## Lưu ý

- Đảm bảo file Excel có đúng định dạng và tên sheet
- Kiểm tra encoding nếu có ký tự đặc biệt
- Notebook được thiết kế cho dữ liệu từ 2025
- Có thể tùy chỉnh các tham số biểu đồ theo nhu cầu

## Hỗ trợ

Nếu gặp lỗi:
1. Kiểm tra file Excel có tồn tại và đúng định dạng
2. Đảm bảo đã cài đặt đầy đủ thư viện
3. Kiểm tra phiên bản Python và các package
4. Xem log lỗi để debug cụ thể