from fastapi import APIRouter

from app.admin_web import render_admin_page
from app.web import render_homepage


router = APIRouter(tags=["web"])


@router.get("/")
def homepage():
    return render_homepage()


@router.get("/admin")
def admin_console():
    return render_admin_page()
