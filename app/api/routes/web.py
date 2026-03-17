from fastapi import APIRouter

from app.web import render_homepage


router = APIRouter(tags=["web"])


@router.get("/")
def homepage():
    return render_homepage()
