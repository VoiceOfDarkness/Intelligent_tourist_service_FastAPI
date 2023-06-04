from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, PlainTextResponse
from starlette.exceptions import HTTPException as GlobalStarletteHTTPException

from admin import manager
from feedback import post
from handler_exceptions import PostFeedbackException, PostRatingException
from login import user
from places import destination
from tourist import visit

app = FastAPI()

app.include_router(manager.router)
app.include_router(user.router)
app.include_router(destination.router)
app.include_router(visit.router)
app.include_router(
    post.router,
    prefix="/ch02/post",
)


@app.exception_handler(GlobalStarletteHTTPException)
def global_exception_handler(req: Request, ex: str):
    return PlainTextResponse(f'Error message: {ex}', status_code=400)


@app.exception_handler(RequestValidationError)
def validationerror_exception_handler(req: Request, ex: str):
    return PlainTextResponse(f'Error message: {ex}', status_code=400)


@app.exception_handler(PostFeedbackException)
def feedback_exception_handler(req: Request, ex: PostFeedbackException):
    return JSONResponse(
        status_code=ex.status_code,
        content={'message': f'error: {ex.detail}'}
    )


@app.exception_handler(PostRatingException)
def rating_exception_handler(req: Request, ex: PostRatingException):
    return JSONResponse(
        status_code=ex.status_code, 
        content={'message': f'error: {ex.detail}'}
    )
