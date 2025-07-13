# Hướng dẫn toàn diện: Phân tích Doanh thu theo Nguồn Giới thiệu

## Mục lục
1. [Tổng quan dự án](#tổng-quan-dự-án)
2. [Yêu cầu hệ thống](#yêu-cầu-hệ-thống)
3. [Cài đặt môi trường](#cài-đặt-môi-trường)
4. [Chuẩn bị dữ liệu](#chuẩn-bị-dữ-liệu)
5. [Chạy ứng dụng](#chạy-ứng-dụng)
6. [Sử dụng ứng dụng](#sử-dụng-ứng-dụng)
7. [Deploy ứng dụng](#deploy-ứng-dụng)
8. [Xử lý lỗi phổ biến](#xử-lý-lỗi-phổ-biến)
9. [Bảo trì và cập nhật](#bảo-trì-và-cập-nhật)

---

## Tổng quan dự án

### Mục đích
Ứng dụng web phân tích doanh thu theo nguồn giới thiệu:
- Theo dõi hiệu quả các kênh giới thiệu bệnh nhân
- Phân tích xu hướng doanh thu theo thời gian
- Đánh giá hiệu suất từng nguồn giới thiệu
- Tạo báo cáo trực quan và tương tác

### Công nghệ sử dụng
- **Frontend**: Streamlit
- **Xử lý dữ liệu**: Pandas, Numpy
- **Visualization**: Plotly
- **Dữ liệu**: Excel files

---

## Yêu cầu hệ thống

### Phần mềm cần thiết
- Python 3.8+
- Git
- Text editor (VS Code khuyến nghị)

### Kiểm tra cài đặt
```bash
python --version
pip --version
```

---

## Cài đặt môi trường

### Bước 1: Tải project
```bash
git clone <repository-url>
cd doanh-thu-theo-nguon-gioi-thieu
```

### Bước 2: Tạo môi trường ảo
```bash
python -m venv venv

# Kích hoạt
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### Bước 3: Cài đặt dependencies
```bash
pip install -r requirements.txt

# Hoặc cài thủ công:
pip install streamlit pandas numpy plotly openpyxl
```

---

## Chuẩn bị dữ liệu

### Cấu trúc file Excel
File `file xu li du lieu.xlsx` cần có:
- **Sheet name**: "table"
- **Các cột bắt buộc**:
  - `noi gioi thieu`: Tên nguồn giới thiệu
  - ` doanh thu `: Số tiền doanh thu (có khoảng trắng)
  - ` so luong `: Số lượng lần giới thiệu (có khoảng trắng)
  - `thang`: Tháng

### Ví dụ dữ liệu
| noi gioi thieu | doanh thu | so luong | thang |
|---------------|-----------|----------|-------|
| Bệnh viện A   | 1500000   | 5        | 1     |
| Phòng khám B  | 2000000   | 8        | 1     |

### Vị trí file
Đặt file Excel trong cùng thư mục với `streamlit_app.py`

---

## Chạy ứng dụng

### Khởi động
```bash
# Kích hoạt môi trường ảo
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Chạy ứng dụng
streamlit run streamlit_app.py
```

### Truy cập
Mở trình duyệt: `http://localhost:8501`

---

## Sử dụng ứng dụng

### Giao diện chính

#### Sidebar - Bộ lọc
- Chọn nguồn giới thiệu
- Chọn khoảng thời gian

#### Dashboard

**Metrics tổng quan:**
- Tổng doanh thu
- Tổng số lượng
- Doanh thu trung bình/lượt
- Số nguồn giới thiệu

**Biểu đồ phân tích:**
1. Top 10 nguồn giới thiệu (cột)
2. Phân bố doanh thu Top 5 (tròn)
3. Xu hướng doanh thu theo tháng (đường)
4. Heatmap doanh thu
5. Scatter plot số lượng vs hiệu suất
6. Xu hướng Top 5 nguồn

#### Bảng dữ liệu
- **Theo Nguồn**: Tổng hợp theo nguồn giới thiệu
- **Theo Tháng**: Tổng hợp theo tháng
- **Hiệu suất**: Phân tích hiệu suất từng nguồn

#### Tóm tắt
- Top 3 nguồn giới thiệu tốt nhất
- Thông tin thời gian phân tích

---

## Deploy ứng dụng

### Streamlit Cloud (Miễn phí)

#### Chuẩn bị GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-repo-url>
git push -u origin main
```

#### Deploy
1. Truy cập: https://share.streamlit.io/
2. Đăng nhập GitHub
3. Tạo app mới
4. Chọn repository và branch
5. Main file: `streamlit_app.py`
6. Deploy

**Lưu ý:** File Excel và requirements.txt phải có trong repository

### Heroku

#### Cài đặt Heroku CLI
Tải từ: https://devcenter.heroku.com/articles/heroku-cli

#### Tạo file cấu hình

**Procfile:**
```
web: streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
```

**setup.sh:**
```bash
mkdir -p ~/.streamlit/
echo "[server]\nheadless = true\nport = $PORT\nenableCORS = false" > ~/.streamlit/config.toml
```

#### Deploy
```bash
heroku login
heroku create your-app-name
git push heroku main
```

### Local Network
```bash
streamlit run streamlit_app.py --server.address=0.0.0.0
```

Truy cập: `http://<your-ip>:8501`

---

## Xử lý lỗi phổ biến

### Lỗi file Excel không tìm thấy
```
FileNotFoundError: Không tìm thấy file 'file xu li du lieu.xlsx'
```
**Giải pháp:**
- Kiểm tra file trong cùng thư mục với `streamlit_app.py`
- Kiểm tra tên file chính xác
- Đảm bảo file không bị lỗi

### Lỗi đọc dữ liệu
```
Error: Lỗi khi đọc dữ liệu
```
**Giải pháp:**
- Kiểm tra sheet name là "table"
- Đảm bảo các cột bắt buộc tồn tại
- Kiểm tra tên cột có khoảng trắng

### Module không tồn tại
```
ModuleNotFoundError: No module named 'streamlit'
```
**Giải pháp:**
```bash
pip install -r requirements.txt
```

### Port đã sử dụng
```
OSError: Address already in use
```
**Giải pháp:**
```bash
# Chạy port khác
streamlit run streamlit_app.py --server.port=8502

# Kill process (Windows)
netstat -ano | findstr :8501
taskkill /PID <PID> /F
```

---

## Bảo trì và cập nhật

### Cập nhật dữ liệu
1. Thay thế file Excel mới
2. Đảm bảo cấu trúc dữ liệu không đổi
3. Refresh trang web (Ctrl + F5)

### Backup dữ liệu
```bash
mkdir backup
cp "file xu li du lieu.xlsx" backup/backup_$(date +%Y%m%d).xlsx
```

### Cập nhật code
```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

### Monitoring
- Theo dõi logs trên Streamlit Cloud
- Kiểm tra performance định kỳ
- Cập nhật dependencies

---

## Hỗ trợ

### Debug
```bash
streamlit run streamlit_app.py --logger.level=debug
```

### Health check
```bash
curl http://localhost:8501/_stcore/health
```

---

## Checklist triển khai

### Trước deploy
- [ ] Kiểm tra dữ liệu Excel
- [ ] Test local thành công
- [ ] Tạo requirements.txt
- [ ] Commit code
- [ ] Kiểm tra bảo mật

### Sau deploy
- [ ] Test production
- [ ] Kiểm tra performance
- [ ] Test responsive
- [ ] Backup dữ liệu
- [ ] Setup monitoring

---

## Kết luận

Ứng dụng phân tích doanh thu theo nguồn giới thiệu đã sẵn sàng sử dụng.

**Hỗ trợ**: Tham khảo documentation Streamlit tại https://docs.streamlit.io/
