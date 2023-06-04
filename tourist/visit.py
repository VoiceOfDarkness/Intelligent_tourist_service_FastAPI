from datetime import datetime
from uuid import UUID, uuid1
from pydantic import BaseModel
from typing import List

from fastapi import APIRouter, HTTPException, status

from login.user import approved_users
from places.destination import (Tour, TourBasicInfo, TourInput, TourLocation,
                                tours, tours_basic_info, tours_location)

router = APIRouter()


tour_preferences = dict()


class Visit(BaseModel):
    id: UUID
    destination: List[TourBasicInfo]
    last_tour: datetime

class Booking(BaseModel):
    id: UUID
    destination: TourBasicInfo
    booking_date: datetime
    tourist_id: UUID


@router.post('ch02/tourist/tour/booking/add')
def create_booking(tour: TourBasicInfo, touristId: UUID):
    if approved_users.get(touristId) == None:
        raise HTTPException(status_code=500
                            , detail="details are missing")
    booking = Booking(id=uuid1(), destination=tour,
                        booking_date=datetime.now(), tourist_id=touristId)
    approved_users[touristId].tours.append(tour)
    approved_users[touristId].booked += 1
    tours[tour.id].isBooked = True
    tours[tour.id].visits += 1
    return booking


@router.get('/ch02/tourist/tour/booked')
def show_booked_tours(touristId: UUID):
    if approved_users.get(touristId) == None:
        raise HTTPException(
            status_code=status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED,
            detail='details are missing',
            headers={"X-InputError":"missing tourist ID"})
    return approved_users[touristId].tours
