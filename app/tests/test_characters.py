from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)


def test_personagens_favoritos_registrados():
    response = client.get("/favorites/", headers={'Content-Type':
    'application/json'})

    assert response.status_code == 200

def test_adicionar_personagem_fav_sem_token():
    response = client.post("/users/me/favorite/", headers={'Content-Type':
    'application/json'})

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

def test_adcionar_personagem_favorito_do_user_com_token():
    response = client.post("/users/me/favorite/", headers={'Content-Type':
    'application/json', "Authorization":"Bearer token"},
    json={
        "name": "Greedo",
        "height": "173",
        "mass": "74",
        "skin_color": "green",
        "eye_color": "black",
        "gender": "male",
    })

    assert response.status_code == 200

def test_update_personagem_favorito_do_user_com_token():
    response = client.post("/users/me/favorite/", headers={'Content-Type':
    'application/json', "Authorization":"Bearer token"},
    json={
        "name": "Luke Skywalker",
        "height": "172",
        "mass": "77",
        "skin_color": "fair",
        "eye_color": "blue",
        "gender": "male",
    })

    assert response.status_code == 200

def test_delete_do_personagem_favorito_com_token():
    response = client.delete("/users/me/favorite/?char_id=n", headers={'Content-Type':
    'application/json', "Authorization":"Bearer token"})

    assert response.status_code == 200

def test_update_do_personagem_favorito_sem_token():
    response = client.put("/users/me/favorite/", headers={'Content-Type':
    'application/json'})

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

def test_delete_personagem_favorito_sem_token():
    response = client.delete("/users/me/favorite/", headers={'Content-Type':
    'application/json'})

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

def test_endpoint_para_pesquisa_de_personagens():
    response = client.get("/characters/?character_id=1",  headers={'Content-Type':
    'application/json'})

    assert response.status_code == 200
    assert response.json() == {
  "name": "Luke Skywalker",
  "height": "172",
  "mass": "77",
  "hair_color": "blond",
  "skin_color": "fair",
  "eye_color": "blue",
  "birth_year": "19BBY",
  "gender": "male"
}