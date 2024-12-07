from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.models.user import User
from app.schemas.user import UserCreate, User as UserSchema

router = APIRouter()

@router.post("/", response_model=dict)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists by telegram_user_id
    db_user = db.query(User).filter(User.telegram_user_id == user.telegram_user_id).first()
    if db_user:
        return {"user_id": db_user.id}
    
    db_user = User(
        telegram_user_id=user.telegram_user_id,
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"user_id": db_user.id}

@router.get("/me", response_model=UserSchema)
def read_user_me(db: Session = Depends(get_db)):
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
