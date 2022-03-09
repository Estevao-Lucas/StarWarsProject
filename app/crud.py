from fastapi import status, HTTPException
import models, schemas
from sqlalchemy.orm import Session

def get_user(db: Session, user_id: int):
    """Filtra os dados dos Usuários pelo id"""
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    """Filtra os dados dos Usuários pelo username"""
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session):
    """Lista todos os Usuários"""
    return db.query(models.User).all()


def create_user(db: Session, user: schemas.UserCreate):
    """Cria um Usuário"""
    db_user = models.User(username=user.username, email=user.email, hashed_password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    """Deleta um Usuário"""
    user_to_delete = db.query(models.User).filter(
        models.User.id == user_id).first()

    if user_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")

    db.delete(user_to_delete)
    db.commit()
    return user_to_delete