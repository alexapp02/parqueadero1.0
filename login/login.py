import psycopg2
from PyQt5 import QtWidgets, uic
from database import Database

conexion = Database("postgres", "Soloparami34", "localhost")

# Función para mostrar la ventana de registro de usuario
def abrir_registro_usuario():
    login.hide()  # Ocultar la ventana de inicio de sesión
    registro.show()  # Mostrar la ventana de registro de usuario

# Función para mostrar la ventana de registro de administrador
def abrir_registro_administrador():
    login.hide()  # Ocultar la ventana de inicio de sesión
    registro2.show()  # Mostrar la ventana de registro de administrador


# Función para manejar el inicio de sesión
def gui_login():
    name = login.user.text().strip()
    password = login.password.text().strip()

    # Verifica si el usuario existe en la tabla "usuario"
    try:
        with conexion.conectar().cursor() as cursor:
            cursor.execute("SELECT * FROM usuario WHERE nombre = %s AND password = %s;", (name, password))
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
            cursor.execute("SELECT * FROM administrador WHERE nombre = %s AND password = %s;", (name, password))
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




# Función para registrar al usuario
def registrar_usuario():
    # Capturar los datos de la interfaz
    nombre = registro.nombre.text().strip()  # Campo Nombre en la interfaz
    email = registro.email.text().strip()  # Campo Email en la interfaz
    password = registro.password.text().strip()  # Campo Contraseña en la interfaz
    celular = registro.celular.text().strip()

# Función para registrar al administrador
def registrar_administrador():
    # Capturar los datos de la interfaz
    nombre = registro2.nombre.text().strip()  # Campo Nombre en la interfaz
    email = registro2.email.text().strip()  # Campo Email en la interfaz
    password = registro2.contraseña.text().strip()  # Campo Contraseña en la interfaz


# Función para mostrar la ventana de confirmación
def gui_entrar():
    login.hide()
    entrar.show()

# Función para mostrar la ventana de error
def gui_error():
    login.hide()
    error.show()

# Función para regresar a la ventana de login desde la ventana de registro de administrador y usuario
def regresar_login():
    registro2.hide()
    registro.hide()
    login.show()

# Función para cerrar la aplicación con el botón cancelar
def cerrar_ventana():
    app.quit()

# Iniciar aplicación
app = QtWidgets.QApplication([])

# Cargar las interfaces de usuario
login_file = "login.ui"
registro_file = "RegistroUsuario.ui"
registro2_file = "RegistroAdministrador.ui"
entrar_file = "confirmacion.ui"
entrar2_file = "confirmacionuser.ui"
error_file = "ErrorRegistro.ui"
error2_file = "ErrorLogin.ui"

login = uic.loadUi(login_file)
registro = uic.loadUi(registro_file)
registro2 = uic.loadUi(registro2_file)
entrar = uic.loadUi(entrar_file)
entrar2 = uic.loadUi(entrar2_file)
error = uic.loadUi(error_file)
error2 = uic.loadUi(error2_file)

# Conectar botones de la ventana de login
login.aceptar.clicked.connect(gui_login)  # Conectar botón Aceptar para login
login.cancelar.clicked.connect(cerrar_ventana)  # Botón para cerrar la aplicación
login.regusuario.clicked.connect(abrir_registro_usuario)  # Conectar botón Registro Usuario
login.regadmin.clicked.connect(abrir_registro_administrador)  # Conectar botón Registro Administrador

# Conectar botones de la ventana de administrador
registro2.aceptar.clicked.connect(registrar_administrador)  # Conectar botón Aceptar en Registro Administrador
registro2.cancelar.clicked.connect(regresar_login)  # Conectar botón Cancelar en Registro Administrador para regresar al login

# Conectar botones de la ventana de usuario
registro.aceptar.clicked.connect(registrar_usuario)  # Conectar botón Aceptar en Registro usuario
registro.cancelar.clicked.connect(regresar_login)  # Conectar botón Cancelar en Registro Administrador para regresar al

# Mostrar la ventana de inicio de sesión
login.show()

# Ejecutar la aplicación
app.exec_()
