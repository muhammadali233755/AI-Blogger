# BloggerAi - FastAPI Blog Application

A modern, full-featured blog application built with FastAPI, SQLAlchemy, and SQLite.

## Features

- ✅ **User Authentication** - JWT-based authentication with bcrypt password hashing
- ✅ **Admin Panel** - Complete admin functionality with user and content management
- ✅ **Blog Management** - Create, read, update, and delete blog posts
- ✅ **Comment System** - Users can comment on blog posts
- ✅ **Like System** - Users can like/unlike blog posts
- ✅ **User Management** - Admin can manage users and privileges
- ✅ **RESTful API** - Clean, well-documented API endpoints

## Tech Stack

- **Backend**: FastAPI
- **Database**: SQLAlchemy with SQLite
- **Authentication**: JWT tokens
- **Password Hashing**: bcrypt
- **Validation**: Pydantic
- **Async Support**: Full async/await support

## Project Structure

```
BloggerAi/
├── auth/           # Authentication utilities
├── crud/           # Database operations
├── models/         # SQLAlchemy models
├── routes/         # API endpoints
├── schemas/        # Pydantic schemas
├── database.py     # Database configuration
├── main.py         # FastAPI application
└── requirements.txt # Dependencies
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd BloggerAi
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

## API Documentation

Once the server is running, visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

## Admin Setup

1. **Set environment variable**
   ```bash
   $env:ALLOW_ADMIN_CREATION="true"  # Windows PowerShell
   ```

2. **Create first admin**
   ```bash
   curl -X POST "http://localhost:8000/create-first-admin" \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "email": "admin@example.com", "password": "admin123"}'
   ```

3. **Login as admin**
   ```bash
   curl -X POST "http://localhost:8000/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=admin&password=admin123"
   ```

## API Endpoints

### Authentication
- `POST /register` - User registration
- `POST /login` - User login

### Admin (Requires JWT Token)
- `POST /create-first-admin` - Create first admin
- `GET /admin/users/` - Get all users
- `PATCH /admin/users/{user_id}` - Update user
- `DELETE /admin/users/{user_id}` - Delete user
- `GET /admin/blogs/` - Get all blogs
- `POST /admin/blogs/` - Create blog as admin
- `DELETE /admin/blogs/{blog_id}` - Delete blog

### Blogs
- `GET /blogs/` - Get all blogs
- `POST /blogs/` - Create blog (authenticated)
- `GET /blogs/{blog_id}` - Get specific blog
- `PATCH /blogs/{blog_id}` - Update blog
- `DELETE /blogs/{blog_id}` - Delete blog

### Comments
- `GET /blogs/{blog_id}/comments/` - Get blog comments
- `POST /blogs/{blog_id}/comments/` - Create comment
- `DELETE /comments/{comment_id}` - Delete comment

### Likes
- `POST /blogs/{blog_id}/likes/` - Like a blog
- `DELETE /blogs/{blog_id}/likes/` - Unlike a blog

## Development

This project follows a clean architecture pattern with:
- **Models**: SQLAlchemy ORM models
- **Schemas**: Pydantic validation schemas
- **CRUD**: Database operation functions
- **Routes**: API endpoint handlers
- **Auth**: JWT authentication and authorization

## License

This project is open source and available under the MIT License. 