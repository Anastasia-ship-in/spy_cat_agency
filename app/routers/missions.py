from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from .. import models, schemas


def create_mission(db: Session, mission: schemas.MissionCreate):
    if mission.cat_id:
        cat = db.query(models.Cat).filter(models.Cat.id == mission.cat_id).first()
        if not cat:
            raise HTTPException(status_code=400, detail="Cat not found")

    db_mission = models.Mission(name=mission.name, completed=mission.completed, cat_id=mission.cat_id)
    db.add(db_mission)
    db.commit()
    db.refresh(db_mission)

    for target in mission.targets:
        db_target = models.Target(
            name=target.name,
            country=target.country,
            notes=target.notes,
            completed=target.completed,
            mission_id=db_mission.id
        )
        db.add(db_target)

    db.commit()

    return db_mission


def delete_mission(db: Session, mission_id: int):
    db_mission = db.query(models.Mission).filter(models.Mission.id == mission_id).first()
    if db_mission is None:
        raise HTTPException(status_code=404, detail="Mission not found")

    if db_mission.cat_id is not None:
        raise HTTPException(status_code=400, detail="Mission cannot be deleted because it is assigned to a cat")

    db.delete(db_mission)
    db.commit()
    return {"detail": "Mission deleted"}


def update_target_logic(mission_id: int, target_id: int, target_update: schemas.TargetUpdate, db: Session):
    mission = db.query(models.Mission).options(joinedload(models.Mission.targets)).filter(
        models.Mission.id == mission_id).first()
    if mission is None:
        raise HTTPException(status_code=404, detail="Mission not found")

    target = next((t for t in mission.targets if t.id == target_id), None)
    if target is None:
        raise HTTPException(status_code=404, detail="Target not found in this mission")

    if mission.completed or target.completed:
        if target_update.notes is not None:
            raise HTTPException(
                status_code=400,
                detail="Notes cannot be updated if the mission or target is completed"
            )

    if target_update.completed is not None:
        target.completed = target_update.completed

    if target_update.notes is not None:
        target.notes = target_update.notes

    db.commit()
    db.refresh(target)

    return target


def assign_cat_to_mission(db: Session, mission_id: int, cat_id: int):
    db_mission = db.query(models.Mission).filter(models.Mission.id == mission_id).first()
    if db_mission is None:
        raise HTTPException(status_code=404, detail="Mission not found")

    db_cat = db.query(models.Cat).filter(models.Cat.id == cat_id).first()
    if db_cat is None:
        raise HTTPException(status_code=404, detail="Cat not found")

    if db_mission.completed:
        raise HTTPException(status_code=400, detail="Cannot assign cat to mission because mission is completed")

    db_mission.cat_id = cat_id
    db.commit()
    db.refresh(db_mission)
    return db_mission


def get_mission(db: Session, mission_id: int):
    db_mission = db.query(models.Mission).options(joinedload(models.Mission.targets)).filter(
        models.Mission.id == mission_id).first()
    if db_mission is None:
        raise HTTPException(status_code=404, detail="Mission not found")

    return db_mission


def list_missions(db: Session):
    missions = db.query(models.Mission).all()
    return missions
