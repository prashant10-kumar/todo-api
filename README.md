# Todo API

A REST API built with FastAPI and PostgreSQL.

## Features
- Full CRUD operations
- Pydantic validation
- PostgreSQL database

## Setup
1. Install dependencies: pip install -r requirements.txt
2. Configure database URL in database.py
3. Run: uvicorn main1:app --reload

## Endpoints
GET    /todos       - Get all todos
POST   /todos       - Create a todo
PATCH  /todos/{id}  - Update a todo
DELETE /todos/{id}  - Delete a todo