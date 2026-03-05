from fastapi import APIRouter, HTTPException
from app.database import SessionLocal
from app.models import User
from app.utils.security import hash_password, verify_password
from app.utils.jwt_handler import create_access_token

router = APIRouter()


# -----------------------------
# Register User
# -----------------------------
@router.post("/register")
def register_user(email: str, password: str):

    db = SessionLocal()

    existing_user = db.query(User).filter(User.email == email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = hash_password(password)

    new_user = User(
        email=email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()

    return {"message": "User registered successfully"}


# -----------------------------
# Login User
# -----------------------------
@router.post("/login")
def login_user(email: str, password: str):

    db = SessionLocal()

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid password")

    token = create_access_token({"sub": user.email})

    return {
        "access_token": token,
        "token_type": "bearer"
    }