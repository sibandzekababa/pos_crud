from fastapi import FastAPI, WebSocket, WebSocketDisconnect, status
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine

from app.models.user import User
from app.models.customer import Customer
from app.models.category import Category
from app.models.supplier import Supplier
from app.models.product import Product
from app.models.sale import Sale
from app.models.sale_item import SaleItem
from app.models.payment import Payment
from app.models.receipt import Receipt

from app.routers.auth_routers import router as auth_router
from app.routers.product_routers import router as product_router
from app.routers.user_routers import router as user_router
from app.routers.customer_routers import router as customer_router
from app.routers.category_routers import router as category_router
from app.routers.supplier_routers import router as supplier_router
from app.routers.sale_routers import router as sale_router
from app.routers.sale_item_routers import router as sale_item_router
from app.routers.payment_routers import router as payment_router
from app.routers.receipt_routers import router as receipt_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SME Supermarket POS API",
    version="2.0.0",
    description="Authenticated supermarket sales, inventory, customers and payments API.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

active_connections: list[WebSocket] = []

@app.websocket("/ws/checkout")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            await websocket.receive_text()  
    except WebSocketDisconnect:
        active_connections.remove(websocket)

@app.post("/api/iot-scan/{barcode}", tags=["System"], status_code=status.HTTP_200_OK)
async def receive_iot_scan(barcode: str):
    for connection in active_connections:
        await connection.send_text(barcode)
    return {"status": "broadcasted", "barcode": barcode}

app.include_router(auth_router)
app.include_router(product_router)
app.include_router(user_router)
app.include_router(customer_router)
app.include_router(category_router)
app.include_router(supplier_router)
app.include_router(sale_router)
app.include_router(sale_item_router)
app.include_router(payment_router)
app.include_router(receipt_router)


@app.get("/", tags=["System"])
def read_root():
    return {"status": "success", "message": "Supermarket POS API is active"}
