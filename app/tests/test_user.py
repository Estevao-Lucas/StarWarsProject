from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)

def test_get_todos_os_dados_dos_usuarios():
    response = client.get("/users/", headers={'Content-Type':
     'application/json'})

    assert response.status_code == 200

def test_cria_usuario():
    response = client.post("/users/", headers={'Content-Type':
    'application/json'}, json={
        "username":"testuser",
        "email": "emailtest@test.com",
        "password":"teste"
    })
    assert response.status_code == 200
    
def test_cria_usuario_que_ja_existe():
    response = client.post("/users/", headers={'Content-Type':
    'application/json'}, json={
        "username":"testuser",
        "email": "emailtest@test.com",
        "password":"teste"
    })
    assert response.status_code == 400

def test_geração_de_token_com_login_certo():
    response = client.post("/token/", 
    headers={"Content-Type":"application/x-www-form-urlencoded"}, data={
        "username":"testuser",
        "password":"teste"
    })
    assert response.status_code == 200

def test_geração_de_token_com_senha_errada():
    response = client.post("/token/", 
    headers={"Content-Type":"application/x-www-form-urlencoded"}, data={
        "username":"testuser",
        "password":"testeerror"
    })
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}

def test_geração_de_token_com_username_errado():
    response = client.post("/token/", 
    headers={"Content-Type":"application/x-www-form-urlencoded"}, data={
        "username":"testusererro",
        "password":"teste"
    })
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}

def test_delete_user_sem_token():
    response = client.delete("/users/me/",
     headers={"accept":"application/json"})

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}
     
def test_acessar_dados_do_user_sem_token():
    response = client.get("/users/me/", headers={'Content-Type':
    'application/json'})

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

def test_acessar_dados_do_user_com_token():
    response = client.get("/users/me/", headers={'Content-Type':
    'application/json', "Authorization":"Bearer token"})

    assert response.status_code == 200

