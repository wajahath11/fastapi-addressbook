from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models
from database import *
from models import Address
from schemas import AddressCreate, AddressInDBBase, AddressUpdate, \
    FilterWithCoordinates

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/addresses/", response_model=AddressInDBBase)
def create_address(address: AddressCreate,
                   db: Session = Depends(get_db)) -> List[Address]:
    """
    Create a new address

    :param address: example:
        {"name": "test", "address": "test", "latitude": 0.0, "longitude": 0.0}
    :param db:
    :return: Address
    """
    db_address = Address(**address.dict())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address


@app.get("/addresses/{address_id}", response_model=AddressInDBBase)
def read_address(address_id: int,
                 db: Session = Depends(get_db)) -> List[Address]:
    """
    Get address by id
    :param address_id:
    :param db:
    :return: Address
    """
    db_address = db.query(Address).filter(Address.id == address_id).first()
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address


@app.put("/addresses/{address_id}", response_model=AddressInDBBase)
def update_address(address_id: int, address: AddressUpdate,
                   db: Session = Depends(get_db)) -> List[Address]:
    """
    Update address by id
    :param address_id: id of the address
    :param address:
    :param db:
    :return:
    """
    db_address = db.query(Address).filter(Address.id == address_id).first()
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    for var, value in vars(address).items():
        setattr(db_address, var, value) if value else None
    db.commit()
    db.refresh(db_address)
    return db_address


@app.delete("/addresses/{address_id}")
def delete_address(address_id: int,
                   db: Session = Depends(get_db)) -> dict[str, str]:
    """
    Delete address by id
    :param address_id:
    :param db:
    :return: dict/json
    """
    db_address = db.query(Address).filter(Address.id == address_id).first()
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    db.delete(db_address)
    db.commit()
    return {"message": "Address deleted successfully"}


@app.post("/addresses-filter/", response_model=List[AddressInDBBase])
def read_addresses(filterCoordinates: FilterWithCoordinates,
                   db: Session = Depends(get_db)) -> List[Address]:
    """
    Filter addresses by coordinates
    :param filterCoordinates: query parameters
    :param db:
    :return:
    """
    db_addresses = db.query(Address).filter(
        Address.latitude >= filterCoordinates.latitude - filterCoordinates.distance,
        Address.longitude >= filterCoordinates.longitude - filterCoordinates.distance,
    ).all()
    return db_addresses
