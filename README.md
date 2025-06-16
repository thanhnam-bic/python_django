## Sửa lỗi database file db.sqlite3 bị lỗi không hiển thị
Bước 1: xóa file db.sqlite3  
Bước 2: Mở terminal (\python_django\mysite)  
Bước 3: Chạy lệnh py manage.py migrate  
Bước 4: Chạy lệnh python manage.py shell  
Bước 5: Copy code trong file insert_data.py và paste vô trong terminal  
Bước 6: Bấm Enter ( để insert dữ liệu vô file db.sqlite3)  
Bước 7: Chạy lệnh exit()  
## Insert thư viện djangorestframework và thư viện JWT (JSON Web Token)
Bước 1: Mở terminal (\python_django\mysite)  
Bước 2: chạy lệnh pip install djangorestframework djangorestframework-simplejwt
# Đồ án: Quản lý tài sản
Django - Python

1. Cài đặt django: pip install django
2. Tạo app: python manage.py startapp <tenapp>
3. Run server: python manage-py runserver
4. Chấp nhận thay đổi DB: py manage.py migrate

Admin page: http://127.0.0.1:8000/admin/

## Lệnh migrate data cho các models

```bash
python manage.py shell | insert_data.py 
```
