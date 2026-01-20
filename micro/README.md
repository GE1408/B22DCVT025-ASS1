# Microservices Django Book Store

Hệ thống bán sách theo mô hình **Microservices Django** với 3 services độc lập.

## Kiến Trúc Hệ Thống

### Version C - Microservices Django
Hệ thống được chia thành 3 services độc lập giao tiếp qua REST APIs:

1. **Customer Service** (Port 8001)
   - Database: `db_micro_customer`
   - Chức năng: Đăng ký, đăng nhập khách hàng

2. **Book Service** (Port 8002)
   - Database: `db_micro_book`
   - Chức năng: Quản lý danh mục sách

3. **Cart Service** (Port 8003)
   - Database: `db_micro_cart`
   - Chức năng: Quản lý giỏ hàng, giao tiếp với Book Service

## Yêu Cầu Hệ Thống

- Python 3.8+
- MySQL Server
- pip (Python package manager)

## Cài Đặt

### Bước 1: Chuẩn Bị Database
Đảm bảo MySQL đang chạy với:
- User: `root`
- Password: `Emailcc123_`

### Bước 2: Cài Đặt Tự Động
Chạy script setup để tạo database, cài đặt dependencies, và chạy migrations:

```bash
setup_all.bat
```

Script sẽ tự động:
- Tạo 3 databases MySQL
- Cài đặt các packages cần thiết
- Chạy migrations cho tất cả services
- Tạo dữ liệu mẫu cho sách

### Bước 3: Chạy Services
Khởi động tất cả 3 services:

```bash
run_all.bat
```

## API Endpoints

### Customer Service (http://localhost:8001)

#### Đăng ký khách hàng
```http
POST /api/register/
Content-Type: application/json

{
  "username": "john",
  "email": "john@example.com",
  "password": "password123",
  "password_confirm": "password123",
  "full_name": "John Doe",
  "phone": "0123456789",
  "address": "123 Main St"
}
```

#### Đăng nhập
```http
POST /api/login/
Content-Type: application/json

{
  "username": "john",
  "password": "password123"
}
```

#### Xem thông tin khách hàng
```http
GET /api/profile/{customer_id}/
```

#### Danh sách khách hàng
```http
GET /api/customers/
```

---

### Book Service (http://localhost:8002)

#### Danh sách sách
```http
GET /api/books/
GET /api/books/?category=Python
GET /api/books/?in_stock=true
```

#### Chi tiết sách
```http
GET /api/books/{book_id}/
```

#### Tạo sách mới
```http
POST /api/books/create/
Content-Type: application/json

{
  "title": "New Book",
  "author": "Author Name",
  "description": "Book description",
  "price": 29.99,
  "isbn": "1234567890123",
  "stock": 100,
  "category": "Programming",
  "image_url": "https://example.com/image.jpg"
}
```

#### Kiểm tra tồn kho
```http
GET /api/books/{book_id}/check-stock/?quantity=5
```

---

### Cart Service (http://localhost:8003)

#### Xem giỏ hàng
```http
GET /api/cart/?customer_id=1
```

#### Thêm sách vào giỏ
```http
POST /api/cart/add/
Content-Type: application/json

{
  "customer_id": 1,
  "book_id": 1,
  "quantity": 2
}
```

#### Cập nhật số lượng
```http
PUT /api/cart/update/{item_id}/
Content-Type: application/json

{
  "quantity": 5
}
```

#### Xóa sách khỏi giỏ
```http
DELETE /api/cart/remove/{item_id}/
```

#### Xóa toàn bộ giỏ hàng
```http
DELETE /api/cart/clear/?customer_id=1
```

## Cấu Trúc Dự Án

```
micro/
├── customer_service/          # Service quản lý khách hàng
│   ├── customers/            # Django app
│   │   ├── models.py        # Customer model
│   │   ├── serializers.py   # DRF serializers
│   │   ├── views.py         # API views
│   │   └── urls.py          # URL routing
│   └── customer_service/
│       └── settings.py       # MySQL config
│
├── book_service/             # Service quản lý sách
│   ├── books/               # Django app
│   │   ├── models.py       # Book model
│   │   ├── serializers.py  # DRF serializers
│   │   ├── views.py        # API views
│   │   ├── urls.py         # URL routing
│   │   └── management/
│   │       └── commands/
│   │           └── seed_books.py  # Tạo dữ liệu mẫu
│   └── book_service/
│       └── settings.py      # MySQL config
│
├── cart_service/            # Service quản lý giỏ hàng
│   ├── carts/              # Django app
│   │   ├── models.py      # Cart, CartItem models
│   │   ├── serializers.py # DRF serializers
│   │   ├── views.py       # API views
│   │   ├── urls.py        # URL routing
│   │   └── services.py    # Book Service client
│   └── cart_service/
│       └── settings.py     # MySQL config
│
├── create_databases.sql    # SQL script tạo databases
├── setup_all.bat          # Script cài đặt tự động
└── run_all.bat            # Script chạy tất cả services
```

## Giao Tiếp Giữa Services

Cart Service giao tiếp với Book Service thông qua HTTP requests:
- Lấy thông tin sách khi xem giỏ hàng
- Kiểm tra tồn kho khi thêm sách vào giỏ
- Xác thực sách tồn tại trước khi thêm

## Dữ Liệu Mẫu

Book Service được tạo sẵn 10 cuốn sách mẫu về lập trình:
- Clean Code
- The Pragmatic Programmer
- Design Patterns
- Introduction to Algorithms
- Python Crash Course
- JavaScript: The Good Parts
- Head First Design Patterns
- Eloquent JavaScript
- You Don't Know JS
- Automate the Boring Stuff with Python

## Testing

### Sử dụng cURL

```bash
# Đăng ký
curl -X POST http://localhost:8001/api/register/ -H "Content-Type: application/json" -d "{\"username\":\"test\",\"email\":\"test@test.com\",\"password\":\"pass123\",\"password_confirm\":\"pass123\",\"full_name\":\"Test User\"}"

# Đăng nhập
curl -X POST http://localhost:8001/api/login/ -H "Content-Type: application/json" -d "{\"username\":\"test\",\"password\":\"pass123\"}"

# Xem danh sách sách
curl http://localhost:8002/api/books/

# Thêm vào giỏ hàng
curl -X POST http://localhost:8003/api/cart/add/ -H "Content-Type: application/json" -d "{\"customer_id\":1,\"book_id\":1,\"quantity\":2}"

# Xem giỏ hàng
curl http://localhost:8003/api/cart/?customer_id=1
```

### Sử dụng Postman hoặc Browser
Truy cập các URL trên bằng Postman hoặc trình duyệt để test APIs.

## Django Admin

Mỗi service có admin panel tại `/admin/`:
- Customer Service: http://localhost:8001/admin/
- Book Service: http://localhost:8002/admin/
- Cart Service: http://localhost:8003/admin/

Tạo superuser cho mỗi service:
```bash
cd customer_service
python manage.py createsuperuser

cd ../book_service
python manage.py createsuperuser

cd ../cart_service
python manage.py createsuperuser
```

## Troubleshooting

### Lỗi kết nối MySQL
- Kiểm tra MySQL đang chạy
- Xác nhận username/password đúng
- Đảm bảo databases đã được tạo

### Lỗi port đã được sử dụng
- Đóng các processes đang dùng ports 8001, 8002, 8003
- Hoặc thay đổi ports trong `run_all.bat`

### Lỗi module not found
- Chạy lại `pip install -r requirements.txt` trong mỗi service
- Kiểm tra đang dùng đúng Python environment

## Tác Giả

Microservices Django Book Store System
