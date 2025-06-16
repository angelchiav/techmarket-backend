# TechMarket Backend API

A robust Django REST Framework-based e-commerce backend API system designed to provide a scalable and secure foundation for modern e-commerce applications.

## 🚀 Current Features

### Authentication & User Management
- **User Registration & Authentication**
  - Secure user registration with email verification
  - JWT (JSON Web Token) based authentication
  - Password reset functionality
  - Email verification system
  - User profile management
  - Role-based access control (RBAC)
  - Address management system
  - Customer groups for discounts and benefits

### API Features
- RESTful API architecture
- Comprehensive API documentation using Swagger/OpenAPI
- Rate limiting and request throttling
- CORS (Cross-Origin Resource Sharing) support
- Secure password hashing and token management
- Input validation and sanitization
- Nested serializers for complex data structures
- Custom permission classes

### Testing & Quality
- Comprehensive test suite with 31 tests
- Test coverage for models, serializers, views, and API endpoints
- Authentication and permission testing
- Data validation testing
- API endpoint testing
- Test database management

### Planned Features
- **Product Management**
  - CRUD operations for products
  - Category management
  - Inventory tracking
  - Image handling
  - Product search and filtering

- **Order Management**
  - Order creation and tracking
  - Payment processing integration
  - Order status management
  - Delivery tracking

- **Customer Management**
  - Customer profiles
  - Order history
  - Address management
  - Wishlist functionality

## 🛠️ Technical Stack
- **Backend Framework**: Django & Django REST Framework
- **Database**: PostgreSQL (planned migration from SQLite)
- **Authentication**: JWT (JSON Web Tokens)
- **API Documentation**: Swagger/OpenAPI
- **Testing**: Django Test Framework
- **Task Queue**: Celery (planned)
- **Caching**: Redis (planned)

## 📋 Project Structure
```
techmarket-backend/
├── config/                 # Main Django project directory
│   ├── settings.py        # Project settings
│   ├── urls.py           # Main URL configuration
│   └── wsgi.py           # WSGI configuration
├── apps/                  # Applications directory
│   └── users/            # Users application
│       ├── models.py     # User models
│       ├── serializers.py # API serializers
│       ├── views.py      # API views
│       ├── urls.py       # URL routing
│       └── tests/        # Test suite
│           ├── test_models.py
│           ├── test_serializers.py
│           ├── test_views.py
│           ├── test_api.py
│           └── test_auth.py
├── media/                # User-uploaded files
└── manage.py            # Django management script
```

## 🔧 Setup Instructions

### Prerequisites
- Python 3.8+
- PostgreSQL (for production)
- Virtual environment tool (venv, conda, etc.)

### Development Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/angelchiav/techmarket-backend.git
   cd techmarket-backend
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```

### API Documentation
Access the API documentation at:
- Swagger UI: `/api/docs/`
- ReDoc: `/api/redoc/`

## 🔐 API Endpoints

### Authentication
- `POST /api/token/` - Obtain JWT token
- `POST /api/token/refresh/` - Refresh JWT token
- `POST /api/users/register/` - Register new user
- `POST /api/users/change-password/` - Change user password

### User Management
- `GET /api/users/me/` - Get current user profile
- `PUT /api/users/me/` - Update user profile
- `GET /api/users/` - List all users (admin only)
- `GET /api/users/{id}/` - Get user details (admin only)

### Address Management
- `GET /api/users/addresses/` - List user addresses
- `POST /api/users/addresses/` - Create new address
- `GET /api/users/addresses/{id}/` - Get address details
- `PUT /api/users/addresses/{id}/` - Update address
- `DELETE /api/users/addresses/{id}/` - Delete address
- `PUT /api/users/addresses/{id}/set-default/` - Set default address

## 🧪 Testing
Run the test suite:
```bash
python manage.py test apps.users.tests
```

Current test coverage:
- Total tests: 31
- Test categories:
  - Model tests
  - Serializer tests
  - View tests
  - API endpoint tests
  - Authentication tests
  - Permission tests

## 📝 Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔮 Roadmap
- [x] Implement user authentication system
- [x] Add address management
- [x] Implement customer groups
- [ ] Implement product management system
- [ ] Add order processing functionality
- [ ] Integrate payment gateway
- [ ] Implement caching system
- [ ] Add real-time notifications
- [ ] Set up CI/CD pipeline
- [ ] Implement analytics dashboard
- [ ] Add multi-language support
