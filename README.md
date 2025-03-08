# Hướng dẫn Sử dụng Flask Blog & To-Do List

## Cài đặt

1. **Clone repository**
   ```sh
   git clone https://github.com/thaibao3214/flask_blog_todo.git
   cd flask_blog_todo
   ```

2. **Tạo và kích hoạt môi trường ảo**
   ```sh
   python -m venv venv
   source venv/bin/activate  # Trên macOS/Linux
   venv\Scripts\activate     # Trên Windows
   ```

3. **Cài đặt các gói cần thiết**
   ```sh
   pip install -r requirements.txt
   ```

## Khởi tạo Database

1. **Tạo database**
   ```sh
   flask db init
   flask db migrate -m "Initial migration."
   flask db upgrade
   ```

2. **Xóa database (nếu cần làm lại từ đầu)**
   ```sh
   flask db downgrade base
   rm -rf migrations/  # Xóa thư mục migrations
   rm app.db  # Xóa file database SQLite (nếu dùng SQLite)
   ```
3. **Reset lại database**
   '''sh
   flask db init
   flask db migrate -m "Reset database"
   flask db upgrade
   '''
## Chạy ứng dụng
```sh
flask run
```
Mở trình duyệt và truy cập: [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Tạo tài khoản Admin
1. **Mở Python shell**
   ```sh
   flask shell
   ```

2. **Tạo tài khoản admin**
   ```python
   from app import db, User
   admin = User(username='admin', is_admin=True)
   admin.set_password('yourpassword')
   db.session.add(admin)
   db.session.commit()
   ```

## Đóng gói với Docker
1. **Xây dựng Docker image**
   ```sh
   docker build -t flask_blog_todo .
   ```

2. **Chạy container**
   ```sh
   docker run -p 5000:5000 flask_blog_todo
   ```

Mở trình duyệt và truy cập: [http://127.0.0.1:5000](http://127.0.0.1:5000)

