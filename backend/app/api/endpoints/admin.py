from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.models import Product, Code
from app.core.config import settings
import csv
from io import StringIO
from decimal import Decimal

router = APIRouter()

async def validate_admin(telegram_user_id: str) -> bool:
    return telegram_user_id == settings.ADMIN_TELEGRAM_ID

@router.post("/upload-pins")
async def upload_pins(
    file: UploadFile = File(...),
    telegram_user_id: str = None,
    db: Session = Depends(get_db)
):
    if not validate_admin(telegram_user_id):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")

    content = await file.read()
    csv_text = content.decode()
    
    # First pass: validate headers
    csv_file = StringIO(csv_text)
    csv_reader = csv.DictReader(csv_file)
    required_columns = {'product_name', 'price', 'pin_code'}
    if not all(col in csv_reader.fieldnames for col in required_columns):
        raise HTTPException(
            status_code=400, 
            detail="CSV must contain columns: product_name, price, pin_code"
        )

    # Second pass: process rows
    csv_file = StringIO(csv_text)  # Reset the StringIO
    csv_reader = csv.DictReader(csv_file)  # Create new reader
    products_created = 0
    pins_created = 0

    for row in csv_reader:
        print(f"Processing row: {row}")  # Debug log
        
        # Get or create product
        product = db.query(Product).filter(Product.name == row['product_name']).first()
        print(f"Found product: {product}")  # Debug log
        
        if not product:
            print(f"Creating new product: {row['product_name']}")  # Debug log
            product = Product(
                name=row['product_name'],
                price=Decimal(row['price']),
                category='default'
            )
            db.add(product)
            db.flush()
            products_created += 1

        # Create code/pin
        code = Code(
            product_id=product.id,
            code=row['pin_code'],
            purchase_cost=Decimal(row['price']),
            sale_price=Decimal(row['price'])
        )
        db.add(code)
        pins_created += 1

    db.commit()
    
    return {
        "message": "Upload successful",
        "products_created": products_created,
        "pins_created": pins_created
    } 