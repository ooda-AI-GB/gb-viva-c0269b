
import os
from datetime import datetime
from typing import List, Optional

import uvicorn
from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# --- Configuration ---
DATABASE_DIR = "data"
DATABASE_URL = f"sqlite:///{DATABASE_DIR}/tasks.db"

# --- Database Setup ---
# Ensure the data directory exists
os.makedirs(DATABASE_DIR, exist_ok=True)

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- SQLAlchemy Model ---
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, index=True)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# --- Seed Data ---
def seed_database():
    db = SessionLocal()
    try:
        if db.query(Task).count() == 0:
            print("Seeding database with initial tasks...")
            db.add(Task(content="Buy groceries"))
            db.add(Task(content="Call mom"))
            db.add(Task(content="Finish report"))
            db.commit()
            print("Database seeded.")
    finally:
        db.close()

# Run seeding on startup
seed_database()

# --- FastAPI App ---
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Routes ---
@app.get("/", response_class=HTMLResponse)
async def read_tasks(request: Request, db: Session = Depends(get_db)):
    pending_tasks = db.query(Task).filter(Task.completed == False).order_by(Task.created_at.desc()).all()
    completed_tasks = db.query(Task).filter(Task.completed == True).order_by(Task.created_at.desc()).all()
    return templates.TemplateResponse(
        "index.html", {"request": request, "pending_tasks": pending_tasks, "completed_tasks": completed_tasks}
    )

@app.post("/add", response_class=RedirectResponse)
async def add_task(request: Request, content: str = Form(...), db: Session = Depends(get_db)):
    if content.strip():
        new_task = Task(content=content.strip())
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
    return RedirectResponse(url="/", status_code=303)

@app.post("/toggle/{task_id}", response_class=RedirectResponse)
async def toggle_task(request: Request, task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        task.completed = not task.completed
        db.commit()
        db.refresh(task)
    return RedirectResponse(url="/", status_code=303)

@app.post("/delete/{task_id}", response_class=RedirectResponse)
async def delete_task(request: Request, task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
    return RedirectResponse(url="/", status_code=303)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

# --- Server Start ---
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
