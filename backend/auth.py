from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from typing import Optional

from backend import models, schemas
from backend.database import get_db

# tells FastAPI how to retrieve the JWT token from the Authorization header (Bearer <token> format).
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# Secret key for JWT signing (keep this safe and secure!)
SECRET_KEY = "your-secret-key"  # Change this for production!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ---------- Helper Functions ----------

# Hash a password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Verify a hashed password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Create JWT token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Verify JWT token
def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

# ---------- Auth Functions ----------

# Get user from database by username
def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

# Create a new user
def create_user(user: schemas.UserCreate, db: Session):
    # Hash the user's password before saving
    hashed_password = hash_password(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Authenticate user (check password)
def authenticate_user(user: schemas.UserLogin, db: Session):
    db_user = get_user(db, user.username)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": db_user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# Get current user from JWT token
def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# ---------- Task CRUD Functions ----------

# Get tasks for a specific user
def get_tasks_for_user(db: Session, user_id: int):
    return db.query(models.Task).filter(models.Task.owner_id == user_id).all()

# Create a task for a user
def create_task(task: schemas.TaskCreate, db: Session, user_id: int):
    db_task = models.Task(title=task.title, description=task.description, owner_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# Update a task's details
def update_task(task_id: int, task: schemas.TaskUpdate, db: Session, user_id: int):
    db_task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == user_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.title:
        db_task.title = task.title
    if task.description:
        db_task.description = task.description
    if task.is_completed is not None:
        db_task.is_completed = task.is_completed
    db.commit()
    db.refresh(db_task)
    return db_task

# Delete a task
def delete_task(task_id: int, db: Session, user_id: int):
    db_task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == user_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return {"msg": "Task deleted successfully"}
