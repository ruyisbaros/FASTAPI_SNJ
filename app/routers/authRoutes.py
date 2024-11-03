from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.responses import JSONResponse
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..oauth2 import create_access_token
from ..utils import verify_password

router = APIRouter(prefix="/auth", tags=["Auth"])


# response_model=schemas.UserCreate
@router.post("/login")
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    # Check if user exists
    loggedIn = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.username)
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
    access_token = create_access_token(
        data={"user_id": loggedIn.id, "email": loggedIn.email}
    )

    return {
        "token_type": "bearer",
        "access_token": access_token,
    }
