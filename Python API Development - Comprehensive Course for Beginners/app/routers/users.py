from .. import schemas, models, utils
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Response
import psycopg2
from sqlalchemy.exc import IntegrityError
router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# Create a user

@router.post("/", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(payload: schemas.createUser, db: Session = Depends(get_db)):
    try:
        # Hash the password
        hashed_password = utils.hash(payload.password)
        payload.password = hashed_password
        payload_dict = models.User(**payload.dict())
        db.add(payload_dict)
        db.commit()
        db.refresh(payload_dict)
        return payload_dict
    except IntegrityError as e:
        db.rollback()
        if "unique constraint" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this username or email already exists.",
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An internal server error occurred.",
            )
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