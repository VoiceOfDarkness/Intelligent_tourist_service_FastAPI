from uuid import UUID, uuid1

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from handler_exceptions import PostFeedbackException, PostRatingException
from places.destination import Post, StarRating, tours

router = APIRouter()

feedback_tour = dict()


class Assessment(BaseModel):
    id: UUID
    post: Post
    tour_id: UUID
    tourist_id: UUID
    

@router.post('/feedback/add')
def post_tourist_feedback(touristId: UUID, tid: UUID,
                          post: Post, bg_task: BackgroundTasks):
    if approved_users.get(touristId) == None and tours.get(tid) == None:
        raise PostFeedbackException(
            detail='tourist and tour details invalid', status_code=403)
    assessId = uuid1()
    assessment = Assessment(id=assessId, post=post, tour_id=tid, tourist_id=touristId)
    feedback_tour[assessId] = assessment
    tours[tid].ratings = (tours[tid].ratings + post.rating) / 2
    bg_task.add_task(log_post_transaction, str(touristId), message='post_tourist_feedback')
    assess_json = jsonable_encoder(assessment)
    return JSONResponse(content=assess_json, status_code=200)


@router.post('/feedback/update/rating')
def update_tour_rating(assessId: UUID, new_rating: StarRating):
    if feedback_tour.get(assessId) == None:
        raise PostRatingException(
            detail='tour assessment invalid', status_code=403)
    tid = feedback_tour[assessId].tour_id
    tours[tid].ratings = (tours[tid].ratigs + new_rating) / 2
    tour_json = jsonable_encoder(tours[tid])
    return JSONResponse(content=tour_json, status_code=200)
