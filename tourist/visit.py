from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from login.user import approved_users
from places.destination import (Tour, TourBasicInfo, TourInput, TourLoaction,
                                tours, tours_basic_info, tours_locations)

router = APIRouter()


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
