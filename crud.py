from sqlalchemy.orm import Session
import models, schemas

def get_task(db: Session, task_id: int, user_id: str):
    return db.query(models.Task).filter(models.Task.id == task_id, models.Task.user_id == user_id).first()

def get_task_by_id(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def get_tasks(db: Session, user_id: str, skip: int = 0, limit: int = 100):
    return db.query(models.Task).filter(models.Task.user_id == user_id).offset(skip).limit(limit).all()

def create_task(db: Session, user_id: str, task: schemas.TaskCreate):
    db_task = models.Task(**task.dict(), user_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: int, user_id: str, task: schemas.TaskCreate):
    db_task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.user_id == user_id).first()
    if db_task:
        for key, value in task.dict().items():
            setattr(db_task, key, value)
        db.commit()
        db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int, user_id: str):
    db_task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.user_id == user_id).first()
    if db_task:
        db.delete(db_task)
        db.commit()
    return db_task

def get_tasks_count(db: Session, user_id: str):
    return db.query(models.Task).filter(models.Task.user_id == user_id).count()
