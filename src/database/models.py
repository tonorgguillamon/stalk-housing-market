from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Boolean, Float, Integer, Date


Base = declarative_base()

class Coordinates(BaseModel):
    latitude: float
    longitude: float

class Accommodation(Base):
    __tablename__ = "accommodations"

    id = Column(Integer, primary_key=True)

    country = Column(String, nullable=True)
    province = Column(String, nullable=True)
    munipality = Column(String, nullable=True)
    district = Column(String, nullable=True)
    neighborhood = Column(String, nullable=True)

    propertyType = Column(String, nullable=True)

    terrace = Column(Boolean, nullable=True)
    garage = Column(Boolean, nullable=True)
    hasLift = Column(Boolean, nullable=True)
    newDevelopment = Column(Boolean, nullable=True)

    price = Column(Float, nullable=True)
    pricePerM2 = Column(Float, nullable=True)

    rooms = Column(Integer, nullable=True)
    bathrooms = Column(Integer, nullable=True)
    size = Column(Integer, nullable=True)

    datePublication = Column(Date, nullable=True)

class SearchFilters(BaseModel):
    country: Optional[str]
    province: Optional[str]
    munipality: Optional[str]
    district: Optional[str]
    neighborhood: Optional[str]

    propertyType: Optional[str]

    terrace: Optional[bool]
    garage: Optional[bool]
    hasLift: Optional[bool]
    newDevelopment: Optional[bool]

    min_price: Optional[float] = Field(None, ge=0)
    max_price: Optional[float] = Field(None, ge=0)

    min_rooms: Optional[int] = Field(None, ge=0)
    max_rooms: Optional[int] = Field(None, ge=0)

    published_after: Optional[date]

    limit: int = Field(20, ge=1, le=50)
