# Todo API

A fully authenticated REST API built with FastAPI, PostgreSQL, and JWT authentication.

## Live API
https://todo-api-production-0a0a.up.railway.app/docs

## Features
- Full CRUD operations for todos
- JWT Authentication (register, login, protected routes)
- User-isolated data (each user sees only their own todos)
- Pydantic validation with Field constraints
- PostgreSQL database with SQLAlchemy ORM
- Auto-generated Swagger UI documentation
- Deployed on Railway

## Tech Stack
- Python 3.14
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic v2
- JWT (python-jose)
- bcrypt password hashing

## Local Setup
1. Clone the repository
2. Install dependencies: pip install -r requirements.txt
3. Create a .env file with:
   DATABASE_URL=postgresql://...
   SECRET_KEY=your_secret_key
4. Run: uvicorn main1:app --reload

## API Endpoints

### Auth
POST   /register    - Create a new account
POST   /login       - Login and receive JWT token

### Todos (authentication required)
GET    /todos       - Get all your todos
POST   /todos       - Create a new todo
PATCH  /todos/{id}  - Update todo completion status
DELETE /todos/{id}  - Delete a todo

## Authentication
1. Register a user via POST /register
2. Login via POST /login to receive a token
3. Click Authorize in Swagger UI and enter your token
4. All protected routes are now accessible