from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

'''
https://medium.com/@guilhermedatt/calling-the-idealista-api-using-python-a39a843cf5cc
'''

class OperationFilter(str, Enum):
    rent = 'rent'
    sale = 'sale'

class OrderFilter(str, Enum):
    distance = 'distance'
    price = 'price'
    street = 'street'
    publicationDate = 'publicationDate'
    modificationDate = 'modificationDate'
    size = 'size'
    floor = 'floor'
    pricedown = 'pricedown'

class SortFilter(str, Enum):
    asc = 'asc'
    desc = 'desc'

class PreservationFilter(str, Enum):
    good = 'good'
    renew = 'renew'

class FurnishedFilter(str, Enum):
    furnished = 'furnished'

class SubTypologyChaletFilter(str, Enum):
    independantHouse = 'independantHouse'
    semidetachedHouse = 'semidetachedHouse'
    terracedHouse = 'terracedHouse'

class HomeFilters(BaseModel):
    minSize: float = None
    maxSize: float = None

    flat: bool = None
    penthouse: bool = None
    duplex: bool = None
    studio: bool = None
    chalet: bool = None
    countryHouse: bool = None

    bedrooms: str = '' # if multiple options, separate by commas: "1,4", "0,2,4". "4" means >= 4
    bathrooms: str = '' # similar to bedrooms

    preservation: PreservationFilter = None
    newDevelopment: bool = None

    furnished: FurnishedFilter = None

    bankOffer: bool = None
    garage: bool = None
    terrace: bool = None
    exterior: bool = None
    elevator: bool = None
    swimmingPool: bool = None
    airConditioning: bool = None
    storeRoom: bool = None

    subTypology: SubTypologyChaletFilter = None

class IDEALISTA(BaseModel):
    baseUrl: str = 'https://api.idealista.com/3.5/'
    country: str = 'es'
    language: str = 'es'
    maxItems: str = 50
    propertyType: str = 'homes'
    
    operation: OperationFilter

    distance: float = None # distance to center -> in meters
    center: str = '' # e.g., '41.3851,2.1734'
    locationId: str = ''

    numPage: int = 0
    maxPrice: float = None
    minPrice: float = None

    order: OrderFilter = OrderFilter.pricedown
    sort: SortFilter = SortFilter.asc

    hasMultimedia: bool = True

    adIds: list[int] = Field(default_factory=list)