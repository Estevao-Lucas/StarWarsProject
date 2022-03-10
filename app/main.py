from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

import requests

from sqlalchemy.orm import Session

from datetime import timedelta

from app import crud, models, schemas, security, auth, constantes

from .database import SessionLocal, engine



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
    access_token_expires = timedelta(minutes=constantes.ACCESS_TOKEN_EXPIRE_MINUTES)
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

@app.delete('/users/me/')
def delete_user(current_user: schemas.User = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    """Deleta Usuário"""
    return crud.delete_user(db=db, user_id=current_user.id)

@app.post("/users/me/favorite/", response_model=schemas.FavCharacter)
def add_fav_character(
    char: schemas.FavCharacterCreate, current_user: schemas.User = Depends(auth.get_current_active_user), 
    db: Session = Depends(get_db)
):
    """Adição de um Persnagem favorito para o usuário"""
    return crud.add_fav_character(db=db, char=char, user_id=current_user.id)

@app.put("/users/me/favorite/", response_model=schemas.FavCharacter)
def update_favorite_char(
    char_id: int, char: schemas.FavCharacter, current_user: schemas.User = Depends(auth.get_current_active_user), db: Session = Depends(get_db)
):
    """Atualiza o personagem favorito do usuario"""
    return crud.update_fav_character(db=db, char_id=char_id, char=char, owner_id=current_user.id )

@app.delete("/users/me/favorite/", response_model=schemas.FavCharacter)
def delete_character(char_id: int,
 current_user: schemas.User = Depends(auth.get_current_active_user),
  db: Session = Depends(get_db)):
    """Deleta Personagem Favorito"""
    return crud.delete_fav_character(db=db, char_id=char_id, owner_id= current_user.id)

@app.get("/favorites/", response_model=list[schemas.FavCharacter])
def read_favorite_characters(db: Session = Depends(get_db)):
    """Mostra a Lista de Personagens Favoritos"""
    characters = crud.get_characters(db)
    return characters

@app.get("/characters/")
def get_character(character_id:int):
    """Consome a Swapi, mostrando os dados do persogem desejado"""
    url = f'https://swapi.dev/api/people/{character_id}/'
    r = requests.get(url)
    dados = r.json()
    return {"name" : dados['name'],
            "height" : dados['height'],
            "mass" : dados['mass'],
            "hair_color" : dados['hair_color'],
            "skin_color" : dados['skin_color'],
            "eye_color" : dados['eye_color'],
            "birth_year" : dados["birth_year"],
            "gender" : dados["gender"]
            }