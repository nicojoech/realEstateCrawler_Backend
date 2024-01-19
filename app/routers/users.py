from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app import schemas
from app.database import SessionLocal
from app.services.userService import crudUser

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/users/", response_model=schemas.UserSchemaResponse)
def create_user(user: schemas.UserSchema, db: Session = Depends(get_db)):
    db_user = crudUser.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crudUser.create_user(db=db, user=user)


@router.get("/users/", response_model=list[schemas.UserSchemaResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crudUser.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}", response_model=schemas.UserSchemaResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crudUser.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/users/{user_id}/agents", response_model=list[schemas.CrawlerAgentResponse])
def get_agents_from_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crudUser.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    agents = crudUser.get_agents_from_user(db, user_id=user_id)
    return agents


@router.get("/users/{user_id}/count")
def get_agent_count_from_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crudUser.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    agents_created = crudUser.get_agent_count_from_user(db, user_id=user_id)
    return agents_created


@router.delete("/users/{user_id}", response_model=schemas.UserSchemaResponse)
def remove_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crudUser.delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
