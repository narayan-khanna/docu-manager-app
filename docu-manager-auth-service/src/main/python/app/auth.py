import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import User
from app.schema import RegisterRequest, LoginRequest, TokenResponse
from app.security import hash_password, verify_password
from app.jwt_utils import create_access_token
from app.logger import get_logger

# Set up logging
logger = get_logger("auth-api")
router = APIRouter()

@router.post("/register", response_model=TokenResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    logger.info(f"Attempting to register user with email: {payload.email}")
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        logger.warning(f"Registration failed - email already exists: {payload.email}")
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=payload.email,
        hashed_password=hash_password(payload.password),
        role=payload.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    logger.info(f"User registered successfully: {user.email} with role: {user.role}")

    token = create_access_token({"user_id": user.id, "email": user.email, "role": user.role})
    logger.debug(f"Access token generated for user: {user.email}")
    return {"token": token}

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    logger.info(f"Login attempt for email: {payload.email}")
    user = db.query(User).filter(User.email == payload.email).first()

    if not user:
        logger.warning(f"Login failed - user not found: {payload.email}")
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not verify_password(payload.password, user.hashed_password):
        logger.warning(f"Login failed - invalid password for user: {payload.email}")
        raise HTTPException(status_code=401, detail="Invalid email or password")

    logger.info(f"User logged in successfully: {user.email}")
    token = create_access_token({"user_id": user.id, "email": user.email, "role": user.role})
    logger.debug(f"Access token generated for user: {user.email}")
    return {"token": token}
