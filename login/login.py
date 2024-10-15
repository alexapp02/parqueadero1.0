from PyQt5 import QtWidgets, uic
import psycopg2
from database import Database
from administrador import RegistroAdministrador # Importar la clase desde administrador.py
from usuario import RegistroUsuario  # Importar la clase desde usuario.py

conexion = Database("postgres", "Soloparami34", "localhost")

# Función para mostrar la ventana de registro de administrador
def abrir_registro_administrador():
    login.hide()  # Ocultar la ventana de inicio de sesión
    ventana_registro_admin.show()  # Mostrar la ventana de registro de administrador

# Función para mostrar la ventana de registro de usuario
def abrir_registro_usuario():
    login.hide()  # Ocultar la ventana de inicio de sesión
    ventana_registro_usuario.show()

# Función para manejar el inicio de sesión
def gui_login():
    user = login.user.text().strip()
    password = login.password.text().strip()

    # Verifica si el usuario existe en la tabla "usuario"
    try:
        with conexion.conectar().cursor() as cursor:
            cursor.execute("SELECT * FROM usuario WHERE email = %s AND password = %s;", (user, password))
            usuario = cursor.fetchone()
            if usuario:
                print("Inicio de sesión exitoso como usuario")
                entrar2.show()  # Muestra la ventana de confirmación de usuario
                login.hide()  # Oculta la ventana de inicio de sesión
                return
    except psycopg2.Error as e:
        print("Error al consultar la tabla usuario: ", e)

    # Verifica si el usuario existe en la tabla "administrador"
    try:
        with conexion.conectar().cursor() as cursor:
            cursor.execute("SELECT * FROM administrador WHERE email = %s AND password = %s;", (user, password))
            administrador = cursor.fetchone()
            if administrador:
                print("Inicio de sesión exitoso como administrador")
                entrar.show()  # Muestra la ventana de confirmación de administrador
                login.hide()  # Oculta la ventana de inicio de sesión
                return
    except psycopg2.Error as e:
        print("Error al consultar la tabla administrador: ", e)

    # Si el usuario no existe en ninguna de las tablas
    gui_error()  # Muestra la ventana de error si no se encontró el usuario

# Función para mostrar la ventana de error
def gui_error():
    login.hide()
    error.show()

# Función para cerrar la aplicación con el botón cancelar
def cerrar_ventana():
    app.quit()

# Iniciar aplicación
app = QtWidgets.QApplication([])

# Cargar las interfaces de usuario
login_file = "login.ui"
entrar_file = "confirmacion.ui"
entrar2_file = "confirmacionuser.ui"
error_file = "ErrorRegistro.ui"
error2_file = "ErrorLogin.ui"

login = uic.loadUi(login_file)
entrar = uic.loadUi(entrar_file)
entrar2 = uic.loadUi(entrar2_file)
error = uic.loadUi(error_file)
error2 = uic.loadUi(error2_file)

# Crear la ventana de registro de administrador desde administrador.py
ventana_registro_admin = RegistroAdministrador(login)
ventana_registro_usuario = RegistroUsuario(login)

# Conectar botones de la ventana de login
login.aceptar.clicked.connect(gui_login)  # Conectar botón Aceptar para login
login.cancelar.clicked.connect(cerrar_ventana)  # Botón para cerrar la aplicación
login.regadmin.clicked.connect(abrir_registro_administrador)  # Conectar botón Registro Administrador
login.regusuario.clicked.connect(abrir_registro_usuario)  # Conectar botón Registro Usuario

# Mostrar la ventana de inicio de sesión
login.show()

# Ejecutar la aplicación
app.exec_()
