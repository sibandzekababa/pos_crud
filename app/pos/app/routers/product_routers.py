import io
from typing import List
from fastapi import APIRouter, Depends, status, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from PIL import Image
import pyrxing

from database import get_db
from app.dependencies import get_current_user, require_roles
from app.models.user import User
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["Products"])


def get_srv(db: Session = Depends(get_db)):
    return ProductService(db)


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    payload: ProductCreate,
    service: ProductService = Depends(get_srv),
    current_user: User = Depends(require_roles("manager", "admin")),
):
    return service.create_product(payload.model_dump())


@router.get("/", response_model=List[ProductResponse])
def read_products(
    service: ProductService = Depends(get_srv),
    current_user: User = Depends(get_current_user),
):
    return service.get_all_products()


@router.post("/scan/camera", response_model=ProductResponse)
def scan_product_via_camera(
    file: UploadFile = File(...),
    service: ProductService = Depends(get_srv),
    current_user: User = Depends(get_current_user),
):
    try:
        image_bytes = file.file.read()
        pil_image = Image.open(io.BytesIO(image_bytes))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid or corrupt image format provided."
        )

    results = pyrxing.read_barcodes(pil_image)
    if not results:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
            detail="No readable barcode detected within camera frame."
        )

    detected_barcode = results[0].text
    return service.scan_product(detected_barcode)


@router.get("/scan/{barcode}", response_model=ProductResponse)
def scan_item(
    barcode: str,
    service: ProductService = Depends(get_srv),
    current_user: User = Depends(get_current_user),
):
    return service.scan_product(barcode)


@router.get("/{id}", response_model=ProductResponse)
def read_product(
    id: int,
    service: ProductService = Depends(get_srv),
    current_user: User = Depends(get_current_user),
):
    return service.get_product(id)


@router.put("/{id}", response_model=ProductResponse)
def update_product(
    id: int,
    payload: ProductUpdate,
    service: ProductService = Depends(get_srv),
    current_user: User = Depends(require_roles("manager", "admin")),
):
    return service.update_product(id, payload.model_dump(exclude_unset=True))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    id: int,
    service: ProductService = Depends(get_srv),
    current_user: User = Depends(require_roles("manager", "admin")),
):
    service.delete_product(id)
