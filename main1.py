from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer , OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from typing import List
from sqlalchemy.orm import Session
import models
import auth
from database import SessionLocal, engine

class UserCreate(BaseModel):
    username : str = Field(min_length = 3)
    password : str = Field(min_length = 6)

class Token(BaseModel):
    access_token : str
    token_type : str

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login")

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class TodoCreate(BaseModel):
    title: str = Field(min_length=1)
    completed: bool

class TodoResponse(BaseModel):
    id: int
    title: str
    completed: bool

    class Config:
        from_attributes = True

class TodoUpdate(BaseModel):
    completed : bool

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token : str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db)):
    username = auth.verify_token(token)
    if username is None:
        raise HTTPException(
            status_code = 401,
            detail = "Invalid or expired token"
        )
    user = db.query(models.User).filter(
        models.User.username == username
    ).first()
    if user is None:
        raise HTTPException(status_code = 401, detail = "User not found")
    return user


@app.get("/todos", response_model=List[TodoResponse])
def get_todos(db: Session = Depends(get_db), current_user : models.User = Depends(get_current_user)):
    return db.query(models.Todo).filter(models.Todo.user_id == current_user.id).all()

@app.post("/todos", response_model=TodoResponse)
def add_todo(todo: TodoCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    new_todo = models.Todo(title=todo.title, completed=todo.completed, user_id = current_user.id)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo 

@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(
        models.User.username == user.username
    ).first()
    if existing_user:
        raise HTTPException(status_code = 400, detail = "Username already exists")
    hashed = auth.hash_password(user.password)
    new_user = models.User(username = user.username, password = hashed)
    db.add(new_user)
    db.commit()
    return {"message" : "User registerd successfully"}

@app.post("/login", response_model = Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.username == form_data.username
    ).first()
    if not user or not auth.verify_password(form_data.password, user.password):
        raise HTTPException(status_code = 401, detail = "Invalid credentials")
    token = auth.create_access_token(data = {"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@app.delete("/todos/{id}")
def del_todo(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    todo = db.query(models.Todo).filter(models.Todo.id == id, models.Todo.user_id == current_user.id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return {"message": f"Todo with id{id} deleted successfully"}

@app.patch("/todos/{id}")
def updt_todo(id: int, update : TodoUpdate , db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    todo = db.query(models.Todo).filter(models.Todo.id == id, models.Todo.user_id == current_user.id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo.completed = update.completed
    db.commit()
    db.refresh(todo)
    return todo