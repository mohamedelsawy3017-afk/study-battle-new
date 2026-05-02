# routers/auth.py - Authentication endpoints
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import get_db
from schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from services.user_service import get_user_by_email, get_user_by_username, create_user
from core.security import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(data: RegisterRequest, db: AsyncSession = Depends(get_db)):
    """Register a new user account."""
    # Check for existing email/username
    if await get_user_by_email(db, data.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    if await get_user_by_username(db, data.username):
        raise HTTPException(status_code=400, detail="Username already taken")

    if len(data.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")

    user = await create_user(db, data.username, data.email, data.password)
    token = create_access_token({"sub": str(user.id)})

    return TokenResponse(
        access_token=token,
        user_id=user.id,
        username=user.username,
    )


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    """Login with email and password."""
    user = await get_user_by_email(db, data.email)

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    token = create_access_token({"sub": str(user.id)})

    return TokenResponse(
        access_token=token,
        user_id=user.id,
        username=user.username,
    )
