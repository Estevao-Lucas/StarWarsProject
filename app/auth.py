from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from jose import jwt, JWTError
from sqlalchemy.orm import Session

import crud, models, schemas, security, constantes
from database import engine, SessionLocal


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    """Autenticação do Usuário"""
    user = crud.get_user_by_username(db, username)
    if not user:
        return False
    if not security.verify_password(password, user.hashed_password):
        return False
    return user

def get_current_user(token: str = Depends(oauth2_scheme), db: Session= Depends(get_db)):
    """Geração do Token para o Usuário"""
    credentials_exception = HTTPException(  status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},)
    try:  
        payload = jwt.decode(token, constantes.SECRET_KEY, algorithms=[constantes.ALGORITHM])
        user: str = payload.get("sub")
        if user is None:  
                raise credentials_exception  

        token_data = schemas.TokenData(username=user)
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_username(db, token_data.username)
    if user is None:
            raise credentials_exception  
    return user 

def get_current_active_user(current_user: schemas.User = Depends(get_current_user)):
    """Retorna o Usuário ativo"""
    return current_user