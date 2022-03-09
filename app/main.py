from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import requests
from sqlalchemy.orm import Session
from datetime import timedelta

import crud, models, schemas, security, auth
from database import SessionLocal, engine

from .constantes import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
models.Base.metadata.create_all(bind=engine)


app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/token/", response_model=schemas.Token)
def token_user(form_data: OAuth2PasswordRequestForm = Depends(),
db: Session = Depends(get_db)):
    """Geração do Token para o user"""
    user = auth.authenticate_user(form_data.username,
     form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Criação de Usuário"""
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=list[schemas.User])
def read_users(db: Session = Depends(get_db)):
    """Lista todos os Usuários"""
    users = crud.get_users(db)
    return users

@app.get("/users/me/", response_model=schemas.User)
def read_user(
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    """Mostra os dados do usuário"""
    return current_user

@app.post("/users/{user_id}/favorite/", response_model=schemas.FavCharacter)
def add_fav_character(
    char: schemas.FavCharacterCreate, current_user: schemas.User = Depends(auth.get_current_active_user), 
    db: Session = Depends(get_db)
):
    """Adição de um Persnagem favorito para o usuário"""
    return crud.add_fav_character(db=db, char=char, user_id=current_user.id)
