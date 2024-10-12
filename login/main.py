import psycopg2
from usuario import *
from database import *

# Inicializar la conexión a la base de datos
conexion = Database("postgres", "Soloparami34", "localhost")

# Crear instancias de Usuario
usuario = Usuario
usuario2 = Usuario
usuario3 = Usuario
usuario4 = Usuario
usuario5 = Usuario
usuario6 = Usuario

# Crear un usuario (asegurándose de usar 'Usuario' con la capitalización correcta)
if Usuario.crearUsuario(conexion.conectar(), "Pepito", "pepito@example.com", "password123", "123456789"):
    print("USUARIO CREADO EXITOSAMENTE")
else:
    print("ERROR DE CREACION")



# Consultar un usuario por ID
usuario.consultarUsuario(conexion.conectar(), 1)

# Consultar todos los usuarios
usuario.consultarUsuarios(conexion.conectar())

