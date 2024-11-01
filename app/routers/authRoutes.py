from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..utils import get_password_hash, verify_password

router = APIRouter(prefix="/auth", tags=["Auth"])


# response_model=schemas.UserCreate
@router.post("/login", response_model=schemas.UserOut)
async def login(
    user_credentials: schemas.UserLogin,
    db: Session = Depends(get_db),
):
    # Check if user exists
    loggedIn = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.email)
        .first()
    )

    if not loggedIn:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    # Check if password is correct
    password_match = verify_password(user_credentials.password, loggedIn.password)

    if not password_match:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    # Create access token

    return loggedIn
