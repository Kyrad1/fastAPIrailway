from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import List, Optional
import logging

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="autenticar-usuario")


@app.get("/")
def root():
    return {
        "mensaje": "Bienvenido a la API de Orquestación de Servicios 🚚⚙️",
        "endpoints_disponibles": [
            "/autenticar-usuario",
            "/autorizar-acceso",
            "/orquestar",
            "/informacion-servicio/{id}",
            "/registrar-servicio",
            "/actualizar-reglas-orquestacion"
        ]
    }







# Simulación de usuarios
fake_users_db = {
    "admin": {"username": "admin", "password": "admin123", "role": "Administrador"},
    "orquestador": {"username": "orquestador", "password": "orq123", "role": "Orquestador"},
}

# Logger para auditoría
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("auditoria")

# Modelos
class AuthInput(BaseModel):
    nombre_usuario: str
    contrasena: str

class ServicioInput(BaseModel):
    nombre: str
    descripcion: str
    endpoints: List[str]

class OrquestarInput(BaseModel):
    servicio_destino: str
    parametros_adicionales: Optional[dict] = {}

class ReglasOrquestacion(BaseModel):
    reglas: dict

class AutorizacionInput(BaseModel):
    recursos: List[str]
    rol_usuario: str

# Simulador de autenticación
def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_users_db.get(token)
    if not user:
        raise HTTPException(status_code=401, detail="Token inválido")
    return user

# Endpoints

@app.post("/autenticar-usuario")
def autenticar_usuario(auth: AuthInput):
    user = fake_users_db.get(auth.nombre_usuario)
    if not user or user["password"] != auth.contrasena:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    return {"access_token": auth.nombre_usuario, "token_type": "bearer", "rol": user["role"]}

@app.post("/autorizar-acceso")
def autorizar_acceso(data: AutorizacionInput, user=Depends(get_current_user)):
    if data.rol_usuario != user["role"]:
        raise HTTPException(status_code=403, detail="Acceso no autorizado")
    return {"autorizado": True, "recursos_permitidos": data.recursos}

@app.post("/orquestar")
def orquestar_servicio(payload: OrquestarInput, user=Depends(get_current_user)):
    if user["role"] not in ["Administrador", "Orquestador"]:
        raise HTTPException(status_code=403, detail="No autorizado para orquestar servicios")
    logger.info(f"[ORQUESTACIÓN] Usuario: {user['username']} orquestó {payload.servicio_destino}")
    return {"mensaje": f"Servicio {payload.servicio_destino} orquestado correctamente"}

@app.get("/informacion-servicio/{id}")
def informacion_servicio(id: str, user=Depends(get_current_user)):
    logger.info(f"[INFO SERVICIO] Usuario: {user['username']} consultó info de {id}")
    return {"id": id, "nombre": f"Servicio {id}", "estado": "activo"}

@app.post("/registrar-servicio")
def registrar_servicio(servicio: ServicioInput, user=Depends(get_current_user)):
    if user["role"] != "Administrador":
        raise HTTPException(status_code=403, detail="Solo administradores pueden registrar servicios")
    logger.info(f"[REGISTRO] Usuario: {user['username']} registró el servicio {servicio.nombre}")
    return {"mensaje": f"Servicio {servicio.nombre} registrado exitosamente"}

@app.put("/actualizar-reglas-orquestacion")
def actualizar_reglas(reglas: ReglasOrquestacion, user=Depends(get_current_user)):
    if user["role"] != "Orquestador":
        raise HTTPException(status_code=403, detail="Solo orquestadores pueden actualizar reglas")
    logger.info(f"[ACTUALIZACIÓN] Usuario: {user['username']} actualizó reglas")
    return {"mensaje": "Reglas de orquestación actualizadas correctamente"}
