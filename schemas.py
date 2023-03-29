from typing import Optional

from pydantic import BaseModel


class AddressBase(BaseModel):
    id: Optional[int]
    name: str
    address: str
    latitude: float
    longitude: float


class AddressCreate(AddressBase):
    pass


class AddressInDBBase(AddressBase):
    pass

    class Config:
        orm_mode = True


class AddressUpdate(AddressBase):
    pass


class FilterWithCoordinates(BaseModel):
    latitude: Optional[float]
    longitude: Optional[float]
    distance: Optional[float] = 0

    class Config:
        orm_mode = True
