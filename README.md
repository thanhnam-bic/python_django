### Admin page: http://127.0.0.1:8000/admin/
## I/ Insert thư viện djangorestframework và thư viện JWT (JSON Web Token)
Bước 1: Mở terminal (\python_django\mysite)  
Bước 2: chạy lệnh
```bash
pip install djangorestframework djangorestframework-simplejwt
```
--------------------------------------------
## II/ Đồ án: Quản lý tài sản
Django - Python
1. Cài đặt django:
```bash
pip install django
```
2. Tạo app:
```bash 
python manage.py startapp <tenapp>
```
3. Run server(chú ý phải ở trong mysite)
```bash
python manage-py runserver
```

--------------------------------------------
## III/ Sửa lỗi database file db.sqlite3 bị lỗi không hiển thị (áp dụng cho hệ điều hành Windows)
Bước 1: Xóa file db.sqlite3  
Bước 2: Mở terminal (\python_django\mysite)  
Bước 3: Chạy lệnh
```bash
py manage.py migrate
``` 
Bước 4: Chạy lệnh
```bash
python manage.py shell
```
Bước 5: Copy code trong file insert_data.py và paste vô trong terminal  
Bước 6: Bấm Enter ( để insert dữ liệu vô file db.sqlite3)  
Bước 7: Chạy lệnh
```bash
exit()
```

--------------------------------------------
## IV/ Lệnh khởi tạo các bảng (table) cho các models trong file sqlite3.db
```bash
py manage.py migrate 
```

--------------------------------------------
## V/ Lệnh khởi tạo dữ liệu mẫu cho các bảng (table)
Bước 1: Mở terminal (\python_django\mysite)
Bước 2: Chạy lệnh
```bash
python manage.py shell
```
Bước 3: Copy code trong file insert_data.py và paste vô trong terminal  
Bước 4: Bấm Enter ( để insert dữ liệu vô file db.sqlite3)  
Bước 5: Chạy lệnh

-------------------------------------------

Github repository: https://github.com/thanhnam-bic/python_django
