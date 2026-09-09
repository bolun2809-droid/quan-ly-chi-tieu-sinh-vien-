# Ứng dụng Quản lý & Phân tích Chi tiêu Sinh viên

Module giao diện (UI) — Thành viên 5.

## 1. Cài đặt

Yêu cầu: Python 3.9+

```bash
# (Khuyến khích) tạo môi trường ảo
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# Cài thư viện
pip install -r requirements.txt
```

## 2. Chạy chương trình

```bash
streamlit run app.py
```

Sau khi chạy, trình duyệt sẽ tự mở tại `http://localhost:8501`.

## 3. Cách sử dụng

1. Ở thanh bên trái, bấm **"Tải lên file CSV dữ liệu sinh viên"** và chọn file dữ liệu
   (ví dụ bộ dữ liệu *Student Spending Habits* từ Kaggle).
2. Chương trình sẽ tự động:
   - Kiểm tra lỗi định dạng cơ bản.
   - Làm sạch dữ liệu (điền giá trị thiếu, xóa dòng trùng).
   - Tính toán thống kê.
3. Dùng bộ lọc (giới tính / năm học / chuyên ngành) ở thanh bên để xem theo nhóm.
4. Xem kết quả ở 4 tab:
   - **Tổng quan**: bảng dữ liệu sau khi làm sạch.
   - **Thống kê**: các chỉ số tổng hợp (thu nhập TB, chi tiêu TB...).
   - **Biểu đồ**: biểu đồ tròn tỷ trọng chi tiêu, phân bố thu nhập, so sánh theo nhóm.
   - **Xuất dữ liệu**: tải file CSV đã làm sạch về máy.

## 4. Cột dữ liệu đầu vào mong đợi

```
age, gender, year_in_school, major, monthly_income, financial_aid,
tuition, housing, food, transportation, books_supplies, entertainment,
personal_care, technology, health_wellness, miscellaneous,
preferred_payment_method
```

Nếu file thiếu cột, chương trình vẫn chạy nhưng sẽ cảnh báo và ẩn bớt
chức năng liên quan đến cột bị thiếu.

## 5. Ghi chú cho nhóm phát triển

Các hàm `clean_data()`, `analyze_data()`, `plot_*()` trong `app.py` hiện
là bản demo đơn giản để giao diện chạy được ngay. Khi các module chính
thức của Thành viên 2 (làm sạch dữ liệu), Thành viên 3 (phân tích),
Thành viên 4 (trực quan hóa) hoàn thành, chỉ cần:

1. Đặt file của các bạn vào thư mục `modules/`.
2. Import hàm tương ứng vào đầu `app.py`.
3. Thay lời gọi hàm demo bằng hàm chính thức.

Phần giao diện (bố cục trang, tab, sidebar, upload, filter) không cần
chỉnh sửa gì thêm.
