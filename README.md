# TechMarket Backend

A Django-based e-commerce backend system that provides a robust foundation for managing an online store.

## 🚀 Features Implemented

### Data Models
- **Categories**: Product categorization system
- **Customers**: User management with authentication
- **Products**: Complete product management with:
  - Name, price, and description
  - Category association
  - Stock status
  - Image upload support
- **Orders**: Order management system with:
  - Product and customer associations
  - Quantity tracking
  - Delivery information
  - Order status
  - Date tracking

### Project Structure
```
techmarket-backend/
├── ecom/              # Main Django project directory
├── store/             # Main application directory
│   ├── models.py      # Data models
│   ├── views.py       # View logic
│   ├── urls.py        # URL routing
│   ├── admin.py       # Admin interface
│   └── templates/     # HTML templates
├── static/            # Static files
├── media/             # User-uploaded files
└── manage.py          # Django management script
```

## 🛠️ Technical Stack
- Django (Python web framework)
- SQLite Database
- Django Admin Interface
- Image handling support

## 📋 Prerequisites
- Python 3.x
- Django
- Pillow (for image handling)

## 🔧 Setup Instructions
1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
6. Run the development server:
   ```bash
   python manage.py runserver
   ```

## 🔐 Admin Access
Access the admin interface at `/admin` to manage:
- Products
- Categories
- Customers
- Orders

## 📝 License
This project is licensed under the terms included in the LICENSE file.
