# hello.py

## Importamos la clase FastAPI desde el modulo FastAPI, para poder crear una app de tipo API
from fastapi import FastAPI
## Importamos desde [Pydantic](https://docs.pydantic.dev/latest/) la clase BaseModel, y el validador de
## texto EmailStr, para poder crear un campo de tipo correo electronico
from pydantic import BaseModel, EmailStr


## Creamos una aplicacion de FastAPI, con algunos parametros
app: FastAPI = FastAPI(
    debug=True,
    title="API de prueba",
    version="0.0.1",
)


## Para poder pedir datos en un request de tipo POST, debemos tener una clase que herede desde BaseModel
## de Pydantic. Esto permitira habilitar las validaciones de datos necesarias
class UserLogin(BaseModel):
    user: str
    pswd: str
    email: EmailStr


## Nuestro primer endpoint sera en la raiz del sitio (`localhost/`). Para ello, decoramos la funcion a ejecutar
## con `@app.<metodo>`, donde nuestro primer metodo sera GET
@app.get("/")
## Definimos la funcion a ejecutar en la ruta `localhost:<puerto>/`
### PYTHONTIP: El guion bajo o _underscore_ tiene varios roles en Python ([text](https://www.geeksforgeeks.org/underscore-_-python/))
### En este caso, lo usamos para definir una funcion cuyo nombre no es relevante
def _():
## El cuerpo de nuestra funcion solo retorna un diccionario, con un mensaje
    return {
        "message": "Hello World from my first API",
    }


## Nuestro segundo endpoint se ubicara en la ruta `localhost/login`. Como es un metodo POST, se decora con
## `@app.post`
@app.post("/login")
## Esta funcion tiene un parametro de tipo UserLogin, la clase definida en la linea 37. Asi, al enviar un request
## a este endpoint, se requerira la data presente en la clase definida, en formato JSON
def _(payload: UserLogin):
## Es notable que, como definimos un modelo de Pydantic, podemos acceder a sus miembros con notacion de punto
## (<objeto>.<atributo>)
    return {
        "message": f"user {payload.user} was successfully created",
        "details": {
            "user_name": payload.user,
            "user_email": payload.email,
            ### PYTHONTIP: Mala practica de seguridad. NUNCA se deben mostrar ni enviar credenciales no encriptadas
            "user_password": payload.pswd,
        }
    }
