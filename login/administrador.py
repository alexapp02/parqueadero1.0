from PyQt5 import QtWidgets, uic
import psycopg2
from database import Database
import re


# Clase para la aplicación de registro de administrador
class RegistroAdministrador(QtWidgets.QMainWindow):
    def __init__(self, login_window):
        super(RegistroAdministrador, self).__init__()
        uic.loadUi('RegistroAdministrador.ui', self)

        # Guardamos una referencia a la ventana de login para volver a ella
        self.login_window = login_window

        # Conexión a la base de datos
        self.conexion = Database("postgres", "Soloparami34", "localhost")

        # Conectar botones
        self.aceptar.clicked.connect(self.registrar_admin)
        self.cancelar.clicked.connect(self.regresar_login)

    def registrar_admin(self):
        nombre = self.nombre.text().strip()
        email = self.email.text().strip()
        password = self.contrasena.text().strip()

        if not nombre or not email or not password:
            self.mostrar_error("Todos los campos son obligatorios.")
            return

        # Validar la contraseña
        if not self.validar_contrasena(password):
            self.mostrar_error("La contraseña debe tener al menos 8 caracteres, una mayúscula, una minúscula y un número.")
            return

        try:
            connection = self.conexion.conectar()
            with connection.cursor() as cursor:
                # Verificar si el correo ya existe
                cursor.execute("SELECT * FROM administrador WHERE email = %s;", (email,))
                if cursor.fetchone():
                    self.mostrar_error("El correo ya está en uso.")
                    return

                # Si el correo no existe, insertar el nuevo administrador
                cursor.execute("INSERT INTO administrador (nombre, email, password) VALUES (%s, %s, %s)",
                               (nombre, email, password))
                connection.commit()  # Confirmar la transacción
                self.mostrar_mensaje("Administrador creado con éxito.")
                self.regresar_login()
        except psycopg2.Error as e:
            self.mostrar_error(f"Error: {e}")

    def validar_contrasena(self, password):
        # Regex para validar la contraseña
        regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$'
        return bool(re.match(regex, password))

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
