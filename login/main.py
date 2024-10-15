import psycopg2
from usuario import Usuario
from database import Database
from administrador import Administrador

# Inicializar la conexión a la base de datos
conexion = Database("postgres", "Soloparami34", "localhost").conectar()

