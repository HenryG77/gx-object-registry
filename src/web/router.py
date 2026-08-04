"""
Router para las páginas web (interfaz de usuario).
"""
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import os

from src.auth.domain.user import User
from src.auth.presentation.dependencies import get_current_user

# Configurar templates con ruta absoluta
current_dir = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(current_dir, "templates")
templates = Jinja2Templates(directory=templates_dir)

router = APIRouter(prefix="/web", tags=["Web UI"])


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Página de login."""
    return templates.TemplateResponse(
        request=request,
        name="login.html"
    )


@router.get("/change-password", response_class=HTMLResponse)
async def change_password_page(request: Request):
    """Página de cambio de contraseña obligatorio."""
    return templates.TemplateResponse(
        request=request,
        name="change_password.html"
    )


@router.get("/test", response_class=HTMLResponse)
async def test():
    """Página de prueba sin template."""
    return HTMLResponse(content="<h1>Test - Si ves esto, el routing funciona!</h1>")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request, current_user: User = Depends(get_current_user)):
    """Página principal (dashboard)."""
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "active_page": "home",
            "current_user": current_user
        }
    )


@router.get("/object-types", response_class=HTMLResponse)
async def object_types_page(request: Request, current_user: User = Depends(get_current_user)):
    """Página de gestión de tipos de objeto."""
    return templates.TemplateResponse(
        request=request,
        name="object_types.html",
        context={
            "active_page": "object-types",
            "current_user": current_user
        }
    )


@router.get("/objects", response_class=HTMLResponse)
async def objects_page(request: Request, current_user: User = Depends(get_current_user)):
    """Página de gestión de objetos GeneXus."""
    return templates.TemplateResponse(
        request=request,
        name="objects.html",
        context={
            "active_page": "objects",
            "current_user": current_user
        }
    )


@router.get("/import", response_class=HTMLResponse)
async def import_page(request: Request, current_user: User = Depends(get_current_user)):
    """Página de importación CSV."""
    return templates.TemplateResponse(
        request=request,
        name="import.html",
        context={
            "active_page": "import",
            "current_user": current_user
        }
    )


@router.get("/users", response_class=HTMLResponse)
async def users_page(request: Request, current_user: User = Depends(get_current_user)):
    """Página de gestión de usuarios."""
    return templates.TemplateResponse(
        request=request,
        name="users.html",
        context={
            "active_page": "users",
            "current_user": current_user
        }
    )
