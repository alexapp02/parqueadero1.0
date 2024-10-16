from PyQt5 import QtWidgets, uic
import psycopg2
from database import Database
import re

class RegistroUsuario(QtWidgets.QMainWindow):
    def __init__(self, login_window):
        super(RegistroUsuario, self).__init__()
        uic.loadUi('RegistroUsuario.ui', self)  # Carga la interfaz desde el archivo .ui

        # Guardamos una referencia a la ventana de login para volver a ella
        self.login_window = login_window

        # Conexión a la base de datos
        self.conexion = Database("postgres", "Soloparami34", "localhost")

        # Conectar botones
        self.aceptar.clicked.connect(self.registrar_usuario)  # Asegúrate de que este nombre sea correcto
        self.cancelar.clicked.connect(self.regresar_login)  # Asegúrate de que este nombre sea correcto

    def registrar_usuario(self):
        nombre = self.nombre.text().strip()
        email = self.email.text().strip()
        password = self.password.text().strip()  # Cambié a 'password' que corresponde a tu ui

        if not nombre or not email or not password:
            self.mostrar_error("Todos los campos son obligatorios.")
            return

        if not self.validar_contrasena(password):
            self.mostrar_error("La contraseña debe tener al menos 8 caracteres, una mayúscula, una minúscula y un número.")
            return

        try:
            connection = self.conexion.conectar()
            with connection.cursor() as cursor:
                # Verificar si el correo ya existe
                cursor.execute("SELECT * FROM usuario WHERE email = %s;", (email,))
                if cursor.fetchone():
                    self.mostrar_error("El correo ya está en uso.")
                    return

                # Si el correo no existe, insertar el nuevo usuario
                cursor.execute("INSERT INTO usuario (nombre, email, password) VALUES (%s, %s, %s)",
                               (nombre, email, password))
                connection.commit()  # Confirmar la transacción
                self.mostrar_mensaje("Usuario creado con éxito.")
                self.regresar_login()
        except psycopg2.Error as e:
            self.mostrar_error(f"Error: {e}")

    def mostrar_mensaje(self, mensaje):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText(mensaje)
        msg.setWindowTitle("Éxito")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()

    def mostrar_error(self, mensaje):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText(mensaje)
        msg.setWindowTitle("Error")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()

    def regresar_login(self):
        # Volver a la ventana de login
        self.hide()
        self.login_window.show()

    def validar_contrasena(self, password):
        # Regex para validar la contraseña
        regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$'
        return bool(re.match(regex, password))

        # Getters
        def get_nombre_usuario(self):
            return self.nombre.text().strip()

        def get_email(self):
            return self.email.text().strip()