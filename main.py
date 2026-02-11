from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from fastapi.responses import JSONResponse

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content=schemas.ResponseModel[None](
            status="error",
            message=exc.detail,
            data=None
        ).model_dump(),
    )

@app.post("/tasks/", response_model=schemas.ResponseModel[schemas.Task])
def create_task(user_id: str, task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = crud.create_task(db=db, user_id=user_id, task=task)
    return schemas.ResponseModel(status="success", message="Task created successfully", data=db_task)

@app.get("/tasks/", response_model=schemas.ResponseModel[List[schemas.Task]])
def read_tasks(user_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tasks = crud.get_tasks(db, user_id=user_id, skip=skip, limit=limit)
    total = crud.get_tasks_count(db, user_id=user_id)
    return schemas.ResponseModel(status="success", message="Tasks retrieved successfully", data=tasks, total=total)

@app.get("/tasks/{task_id}", response_model=schemas.ResponseModel[schemas.Task])
def read_task(task_id: int, user_id: str, db: Session = Depends(get_db)):
    # First check if task exists at all
    db_task_check = crud.get_task_by_id(db, task_id=task_id)
    if db_task_check is None:
        raise HTTPException(status_code=404, detail="Task not found")
        
    # Then check if user owns it
    if db_task_check.user_id != user_id:
        raise HTTPException(status_code=404, detail="user id is not found")
        
    return schemas.ResponseModel(status="success", message="Task retrieved successfully", data=db_task_check)

@app.put("/tasks/{task_id}", response_model=schemas.ResponseModel[schemas.Task])
def update_task(task_id: int, user_id: str, task: schemas.TaskCreate, db: Session = Depends(get_db)):
    # First check if task exists at all
    db_task_check = crud.get_task_by_id(db, task_id=task_id)
    if db_task_check is None:
        raise HTTPException(status_code=404, detail="Task not found")
        
    # Then check if user owns it
    if db_task_check.user_id != user_id:
        raise HTTPException(status_code=404, detail="user id is not found")
        
    db_task = crud.update_task(db, task_id=task_id, user_id=user_id, task=task)
    return schemas.ResponseModel(status="success", message="Task updated successfully", data=db_task)

@app.delete("/tasks/{task_id}", response_model=schemas.ResponseModel[schemas.Task])
def delete_task(task_id: int, user_id: str, db: Session = Depends(get_db)):
    # First check if task exists at all
    db_task_check = crud.get_task_by_id(db, task_id=task_id)
    if db_task_check is None:
        raise HTTPException(status_code=404, detail="Task not found")
        
    # Then check if user owns it
    if db_task_check.user_id != user_id:
        raise HTTPException(status_code=404, detail="user id is not found")
        
    db_task = crud.delete_task(db, task_id=task_id, user_id=user_id)
    return schemas.ResponseModel(status="success", message="Task deleted successfully", data=db_task)
