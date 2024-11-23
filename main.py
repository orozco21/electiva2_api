from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
from core.conexion import conexion
from models.user import User
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator

app = FastAPI()

class User(BaseModel):
    Username: str
    Password: str

# Configurar CORS
app.add_middleware(
CORSMiddleware,
allow_origins=["*"],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)

@app.post("/login")
async def login(user: User):
    cursor = conexion.cursor()
    query = "SELECT * FROM usuarios WHERE Username = %s AND Password = %s"
    values = (user.Username, user.Password)

    cursor.execute(query, values)
    resultado = cursor.fetchone()

    if resultado:
        return {"success": True}
    else:
        raise HTTPException(status_type=401, detail="Credenciales incorrectas")
    
# Ruta crear Usuario
@app.post('/user')
async def create_user(user: User):
    cursor = conexion.cursor()
    query = "INSERT INTO usuarios(Username, Password) VALUES(%s,%s)"
    values = (user.Username, user.Password)

    try:
        cursor.execute(query, values)
        conexion.commit()
        return {"message": "Usuario creado correctamente"}
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Error al guardar usuario: {err}")
    except ValueError as e:
        raise HTTPException(status_code=403, detail=f"Error al guardar el usuario: {e}")
    finally:
        cursor.close()

# Ruta Actualizar Usuario
# Ruta Actualizar Usuario
@app.put("/user/{username}")
async def update_user(username: str, user: User):
    cursor = conexion.cursor()

    # Verificar si el usuario existe
    check_query = "SELECT * FROM usuarios WHERE Username = %s"
    cursor.execute(check_query, (username,))
    existing_user = cursor.fetchone()

    if not existing_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Actualizar el usuario
    query = "UPDATE usuarios SET Password = %s WHERE Username = %s"
    values = (user.Password, username)

    try:
        cursor.execute(query, values)
        conexion.commit()

        return {"message": "Contraseña actualizada correctamente"}
    except mysql.connector.Error as err:
        print(f"Error de base de datos: {err}")
        raise HTTPException(status_code=500, detail=f"Error al actualizar contraseña: {err}")
    except Exception as err:
        print(f"Error general: {err}")
        raise HTTPException(status_code=500, detail=f"Error al actualizar contraseña: {err}")
    finally:
        cursor.close()
    

    
# Ruta Eliminar Usuario
@app.delete("/user/{user_id}")
async def delete_user(user_id: int):
    cursor = conexion.cursor()
    query = "DELETE FROM usuarios WHERE id = %s" 
    values = (user_id,)

    try:
        cursor.execute(query, values)
        conexion.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return {"message": "Usuario eliminado correctamente"}
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Error al eliminar usuario: {err}")
    finally:
        cursor.close()

# Ruta obtener usuarios
@app.get("/users")
async def get_users():
    cursor = conexion.cursor()
    query = "SELECT * FROM usuarios"

    try:
        cursor.execute(query)
        resultado = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]
        usuarios = [dict(zip(columnas, row)) for row in resultado]
        return {"users": usuarios}
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Error al obtener usuarios: {err}")
    finally:
        cursor.close()
