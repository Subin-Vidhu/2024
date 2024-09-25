from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, models, utils, oauth2
from ..database import get_db

router = APIRouter(
    tags=["authentications"]
)

@router.post("/login")
async def login_user(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password")
    # create and return the access token
    access_token = oauth2.create_access_token(data={"email": user.email, "id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
    # return {"access_token": "example token"}