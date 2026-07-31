"""
Router para las páginas web (interfaz de usuario).
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

# Configurar templates con ruta absoluta
current_dir = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(current_dir, "templates")
templates = Jinja2Templates(directory=templates_dir)

router = APIRouter(prefix="/web", tags=["Web UI"])


@router.get("/test", response_class=HTMLResponse)
async def test():
    """Página de prueba sin template."""
    return HTMLResponse(content="<h1>Test - Si ves esto, el routing funciona!</h1>")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Página principal (dashboard)."""
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"active_page": "home"}
    )


@router.get("/object-types", response_class=HTMLResponse)
async def object_types_page(request: Request):
    """Página de gestión de tipos de objeto."""
    return templates.TemplateResponse(
        request=request,
        name="object_types.html",
        context={"active_page": "object-types"}
    )


@router.get("/objects", response_class=HTMLResponse)
async def objects_page(request: Request):
    """Página de gestión de objetos GeneXus."""
    return templates.TemplateResponse(
        request=request,
        name="objects.html",
        context={"active_page": "objects"}
    )


@router.get("/import", response_class=HTMLResponse)
async def import_page(request: Request):
    """Página de importación CSV."""
    return templates.TemplateResponse(
        request=request,
        name="import.html",
        context={"active_page": "import"}
    )
