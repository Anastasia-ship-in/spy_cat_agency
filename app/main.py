from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .routers import cats, missions
from .database import SessionLocal, initialize_database
from . import schemas

app = FastAPI()
initialize_database()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/spy_cats/")
def create_spy_cat(spy_cat: schemas.SpyCatCreate, db: Session = Depends(get_db)):
    db_cat = cats.create_spy_cat(db, spy_cat.name, spy_cat.experience, spy_cat.breed, spy_cat.salary)
    if db_cat is None:
        raise HTTPException(status_code=400, detail="Invalid breed")
    return db_cat


@app.get("/spy_cats/")
def read_spy_cats(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return cats.get_spy_cats(db, skip=skip, limit=limit)


@app.get("/spy_cats/{cat_id}")
def read_spy_cat(cat_id: int, db: Session = Depends(get_db)):
    db_cat = cats.get_spy_cat(db, cat_id)
    if db_cat is None:
        raise HTTPException(status_code=404, detail="Spy Cat not found")
    return db_cat


@app.put("/spy_cats/{cat_id}")
def update_spy_cat_salary(cat_id: int, salary_update: schemas.SalaryUpdate, db: Session = Depends(get_db)):
    db_cat = cats.update_spy_cat_salary_in_db(db, cat_id, salary_update.salary)
    if db_cat is None:
        raise HTTPException(status_code=404, detail="Spy Cat not found")
    return db_cat


@app.delete("/spy_cats/{cat_id}")
def delete_spy_cat(cat_id: int, db: Session = Depends(get_db)):
    db_cat = cats.remove_spy_cat(db, cat_id)
    if db_cat is None:
        raise HTTPException(status_code=404, detail="Spy Cat not found")
    return {"detail": "Spy Cat deleted"}


@app.post("/missions/")
def create_mission_endpoint(mission: schemas.MissionCreate, db: Session = Depends(get_db)):
    db_mission = missions.create_mission(db, mission)
    if db_mission is None:
        raise HTTPException(status_code=400, detail="Mission creation failed")
    return {
        "message": "Mission created successfully",
        "mission": db_mission
    }, status.HTTP_201_CREATED


@app.delete("/missions/{mission_id}")
def delete_mission(mission_id: int, db: Session = Depends(get_db)):
    db_mission = missions.delete_mission(db, mission_id)
    if db_mission is None:
        raise HTTPException(status_code=404, detail="Mission not found")
    return {"detail": "Mission deleted"}


@app.put("/missions/{mission_id}/targets/{target_id}")
def update_target_endpoint(mission_id: int, target_id: int, target_update: schemas.TargetUpdate,
                           db: Session = Depends(get_db)):
    updated_target = missions.update_target_logic(mission_id, target_id, target_update, db)
    return updated_target


@app.put("/missions/{mission_id}/assign_cat")
def assign_cat_to_mission(mission_id: int, cat_id: int, db: Session = Depends(get_db)):
    db_mission = missions.assign_cat_to_mission(db, mission_id, cat_id)
    if db_mission is None:
        raise HTTPException(status_code=404, detail="Mission or Cat not found or already assigned")
    return db_mission


@app.get("/missions/{mission_id}")
def get_mission(mission_id: int, db: Session = Depends(get_db)):
    db_mission = missions.get_mission(db, mission_id)
    if db_mission is None:
        raise HTTPException(status_code=404, detail="Mission not found")
    return db_mission


@app.get("/missions/")
def list_missions(db: Session = Depends(get_db)):
    missions_list = missions.list_missions(db)
    if not missions_list:
        raise HTTPException(status_code=404, detail="No missions found")
    return missions_list
