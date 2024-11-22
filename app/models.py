from sqlalchemy import Column, Integer, Float, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Cat(Base):
    __tablename__ = "cats"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    experience = Column(Integer)
    breed = Column(String)
    salary = Column(Float)

    missions = relationship("Mission", back_populates="cat")


class Mission(Base):
    __tablename__ = "missions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    cat_id = Column(Integer, ForeignKey("cats.id"))
    completed = Column(Boolean, default=False)

    cat = relationship("Cat", back_populates="missions")
    targets = relationship("Target", back_populates="mission", cascade="all, delete-orphan")


class Target(Base):
    __tablename__ = "targets"
    id = Column(Integer, primary_key=True, index=True)
    mission_id = Column(Integer, ForeignKey("missions.id"))
    name = Column(String, index=True)
    country = Column(String)
    notes = Column(String)
    completed = Column(Boolean, default=False)

    mission = relationship("Mission", back_populates="targets")
