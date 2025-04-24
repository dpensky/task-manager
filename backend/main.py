from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from backend import models, schemas, auth
from backend.database import engine, get_db
from backend.auth import get_current_user
from typing import List

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Allow frontend to connect (adjust as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend URL for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def read_root():
    return FileResponse(os.path.join("static", "index.html"))


# ---------- Auth Routes ----------

@app.post("/register", response_model=schemas.Token)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return auth.register_user(user, db)

@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    return auth.authenticate_user(user, db)

# ---------- Task Routes ----------

@app.get("/tasks/", response_model=List[schemas.TaskOut])
def get_tasks(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return auth.get_tasks_for_user(db, current_user.id)

@app.post("/tasks/", response_model=schemas.TaskOut)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return auth.create_task(task, db, current_user.id)

@app.put("/tasks/{task_id}", response_model=schemas.TaskOut)
def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return auth.update_task(task_id, task, db, current_user.id)

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return auth.delete_task(task_id, db, current_user.id)
