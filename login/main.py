import psycopg2
from usuario import Usuario
from database import Database
from administrador import Administrador

# Inicializar la conexión a la base de datos
conexion = Database("postgres", "Soloparami34", "localhost").conectar()

# Crear un usuario
if Usuario.crearUsuario(conexion, "Pepito", "pepito@example.com", "password123", "123456789"):
    print("USUARIO CREADO EXITOSAMENTE")
else:
    print("ERROR DE CREACION")

# Consultar un usuario por ID
Usuario.consultarUsuario(conexion, 1)

# Consultar todos los usuarios
Usuario.consultarUsuarios(conexion)

# Crear un nuevo administrador
if Administrador.crearAdministrador(conexion, "admin1", "admin1@example.com", "adminpass"):
    print("ADMINISTRADOR CREADO EXITOSAMENTE")
else:
    print("ERROR DE CREACION")
# Consultar un administrador
Administrador.consultarAdministrador(conexion, 1)

# Consultar todos los administradores
Administrador.consultarAdministradores(conexion)

# Actualizar un administrador
Administrador.actualizarAdministrador(conexion, 1, "admin_actualizado", "newemail@example.com")

# Eliminar un administrador
Administrador.eliminarAdministrador(conexion, 1)
