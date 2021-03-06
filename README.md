# StarWarsProject
API que realiza request para outra API de personagens de Starwars, criação de usuários e definição de seus personagens favoritos.
***
## 🐱‍💻Desenvolvimento:
* A API foi desenvolvida utilizando a linguagem de programação python, fazendo uso do framework FastAPI, PostgreSQL como o banco de dados e o Docker como ambiente de desenvolvimento.
***
## 🧾Instruções para o Uso:
## **Pré-requisitos:**
* Docker .
* Python.
## **Instruções**:
* Clone este repositório ```git clone https://github.com/Estevao-Lucas/StarWarsProject.git```
* Entre na pasta StarWarsProject ```cd StarWarsProject/```
* Execute o comando ```docker-compose up```
* Feito isso sua aplicação estará rodando na porta :8000.

## 📕 Documentação:
***
* A Documentação do projeto pode ser lida e realizada as ações em ```/docs``` ou ```/redoc```.
***
### 🚀 Rotas:
***
* Endpoint : ```/token/```
* Methods : ```POST```
* Action: method ```POST``` Geração de Token
* Body, Header x-www-form-urlencoded: ```username:str```, ```password:str```.
* OBS: ```Necessita de Cadastro prévio```
***
* Endpoint : ```/users/```
* Methods : ```GET, POST```
* Token : ```Não necessário```
* Action: method ```GET``` Lista todos os usuários cadatrados junto de seus dados
* Action: method ```POST``` Realiza o Cadastro do usuário
* Body [```POST```]: ```username:str```, ```email:str```, ```password:str```
***
* Endpoint : ```/users/me/```
* Methods: ```GET, DELETE```
* Token : ```Necessário```
* Action: method ```GET``` Lista os dados do usuário autenticado
* Action: method ```DELETE``` Deleta o usuário logado
***
* Endpoint : ```/users/me/favorite/```
* Methods : ```DELETE, POST, PUT```
* Token : ```Necessário```
* Action: method ```POST``` Adiciona um personagem favorito ao usuario logado
* Body:
 ```
 [```POST```]:
 {
    "name": "string",
    "height": "string",
    "mass": "string",
    "hair_color": "string",
    "skin_color": "string",
    "eye_color": "string",
    "birth_year": "string",
    "gender": "string"
}
```
* Action: method ```PUT``` Atualiza o personagem favorito de um usuario
* OBS: ```Necessita ser passado o parametro na url: /users/me/favorite/?char_id=(id do personagem)```
* Body:
```
{
  "name": "string",
  "height": "string",
  "mass": "string",
  "hair_color": "string",
  "skin_color": "string",
  "eye_color": "string",
  "birth_year": "string",
  "gender": "string",
  "id": 0, (Não necessita preencher)
  "owner_id": 0 (Não necessita preencher)
}
```
* Action:method ```DELETE``` Deleta o personagem favorito do usuário logado
* OBS: ```Necessita ser passado o parametro na url: /users/me/favorite/?char_id=(id do personagem)```
***
* Endpoint:```/favorites/``` Lista todos os personagens favoritos registrados
* Methods: ```GET```
* Token: ```Não é necessário```
***
* Endpoint: ```/characters/``` Realiza um request para a api de starwars e retorna os dados do personagem com o id procurado
* Methods: ```GET```
* Token: ```Não é necessário```
* Pesquisa com a URL ```/characters/?character_id=(id do personagem desejado)```
* Retorna:
```
Exemplo id: 1
{
  "name": "Luke Skywalker",
  "height": "172",
  "mass": "77",
  "hair_color": "blond",
  "skin_color": "fair",
  "eye_color": "blue",
  "birth_year": "19BBY",
  "gender": "male"
}
```
***
## 🛠 Testes
* Para executar os testes utilize o comando ```docker-compose exec web pytest```
* Para ver o coverage dos testes utilize o comando:
*  ```docker-compose exec web pytest --cov-config=.coveragerc --cov=app app/tests/ ```
* Para rotas com autenticação é necessário a substituição da palavra ```Token``` nos testes pelo Token de fato gerado com o login
* Para rotas que necessitam de query-params é necessário a substituição do paramêtro
