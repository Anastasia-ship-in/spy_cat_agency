from sqlalchemy.orm import Session
from .. import models, validators
from fastapi import HTTPException


def create_spy_cat(db: Session, name: str, experience: int, breed: str, salary: float):
    if not validators.validate_breed(breed):
        raise ValueError("Invalid breed")
    db_cat = models.Cat(name=name, experience=experience, breed=breed, salary=salary)
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat


def get_spy_cats(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Cat).offset(skip).limit(limit).all()


def get_spy_cat(db: Session, cat_id: int):
    return db.query(models.Cat).filter(models.Cat.id == cat_id).first()


def update_spy_cat_salary_in_db(db: Session, cat_id: int, salary: float):
    cat = db.query(models.Cat).filter(models.Cat.id == cat_id).first()
    if cat is None:
        raise HTTPException(status_code=404, detail="Cat not found")
    cat.salary = salary
    db.commit()
    db.refresh(cat)
    return cat


def remove_spy_cat(db: Session, cat_id: int):
    cat = db.query(models.Cat).filter(models.Cat.id == cat_id).first()
    if cat is None:
        raise HTTPException(status_code=404, detail="Cat not found")
    db.delete(cat)
    db.commit()
    return cat
