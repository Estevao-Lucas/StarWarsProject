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

def get_characters(db: Session):
    """Lista todos os Personagens"""
    return db.query(models.Character).all()

def add_fav_character(db: Session, char: schemas.FavCharacterCreate, user_id: int):
    """Adiciona um personagem favorito para o Usuário"""
    db_char = models.Character(**char.dict(), owner_id=user_id)
    db.add(db_char)
    db.commit()
    db.refresh(db_char)
    return db_char

def update_fav_character(db: Session, char_id: int,
 char:schemas.FavCharacter, owner_id:int):
    """Atualiza o personagem favorito do Usuário"""
    char_to_update = db.query(models.Character).filter(models.Character.id == char_id).first()
    char_to_update.name = char.name
    char_to_update.height = char.height
    char_to_update.mass = char.mass
    char_to_update.skin_color = char.skin_color
    char_to_update.eye_color = char.eye_color
    char_to_update.gender = char.gender
    db.commit()
    return char_to_update

def delete_fav_character(db: Session, char_id: int, owner_id:int):
    """Deleta um Personagem Favorito"""
    character_to_delete = db.query(models.Character).filter(
        models.Character.id == char_id).first()

    if character_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Character Not Found")

    db.delete(character_to_delete)
    db.commit()

    return character_to_delete
