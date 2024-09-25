from .. import schemas, models, utils
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Response
import psycopg2
router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# Create a user
@router.post("/", response_model = schemas.UserOut)
async def create_user(payload: schemas.createUser, db: Session = Depends(get_db)):
    # Hash the password
    hashed_password = utils.hash(payload.password)
    payload.password = hashed_password
    payload_dict = models.User(**payload.dict())
    db.add(payload_dict)
    db.commit()
    db.refresh(payload_dict)
    return payload_dict

# Get only one user
@router.get("/{id}", response_model = schemas.UserOut)
async def read_user(id, response: Response, db: Session = Depends(get_db)):
    try:
        user = db.query(models.User).filter(models.User.id == id).first()
        if user:
            return user
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")