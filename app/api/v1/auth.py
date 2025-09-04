# app/api/v1/auth.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas.user import UserCreate, UserOut
from app.models.user import User
from app.db.session import get_session
from app.utils.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserOut)
async def register(payload: UserCreate, session: AsyncSession = Depends(get_session)):
    exists = (await session.execute(select(User).where(User.email == payload.email))).scalar_one_or_none()
    if exists:
        raise HTTPException(400, detail="Email already registered")
    user = User(
        email=payload.email, 
        full_name=payload.full_name, 
        username=payload.username, 
        hashed_password=hash_password(payload.password)
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),  # Fixed: Use proper OAuth2 form
    session: AsyncSession = Depends(get_session)
):
    # Try to find user by username or email
    user = (await session.execute(
        select(User).where(
            (User.email == form_data.username) | (User.username == form_data.username)
        )
    )).scalar_one_or_none()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(401, detail="Invalid credentials")
    
    token = create_access_token(sub=user.email)
    return {"access_token": token, "token_type": "bearer"}