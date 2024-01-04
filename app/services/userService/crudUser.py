from sqlalchemy.orm import Session

from app import schemas, models
from app.services.authService.auth import get_password_hash


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_agents_from_user(db: Session, user_id: int):
    return db.query(models.CrawlerAgent).filter(models.CrawlerAgent.user_id == user_id).all()


def create_user(db: Session, user: schemas.UserSchema):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(first_name=user.first_name, last_name=user.last_name, email=user.email,
                          username=user.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    user_to_delete = db.query(models.User).filter(models.User.id == user_id).first()

    if user_to_delete:
        db.delete(user_to_delete)
        db.commit()

    return user_to_delete
