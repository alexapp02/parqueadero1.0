from PyQt5 import QtWidgets, uic
import psycopg2
from database import Database

# Clase para la aplicación de registro de usuario
class RegistroUsuarioApp(QtWidgets.QMainWindow):
    def __init__(self, login_window):
        super(RegistroUsuarioApp, self).__init__()
        uic.loadUi('RegistroUsuario.ui', self)

        # Guardamos una referencia a la ventana de login para volver a ella
        self.login_window = login_window

        # Conexión a la base de datos
        self.conexion = Database("postgres", "Soloparami34", "localhost")

        # Conectar botones
        self.aceptar.clicked.connect(self.registrar_usuario)
        self.cancelar.clicked.connect(self.regresar_login)

    def registrar_usuario(self):
        nombre = self.nombre.text().strip()
        email = self.email.text().strip()
        password = self.contrasena.text().strip()
        celular = self.celular.text().strip()  # Suponiendo que tienes un campo para celular

        if not nombre or not email or not password or not celular:
            self.mostrar_error("Todos los campos son obligatorios.")
            return

        try:
            # Obtener la conexión una sola vez
            connection = self.conexion.conectar()
            with connection.cursor() as cursor:
                # Verificar si el correo ya existe
                cursor.execute("SELECT * FROM usuario WHERE email = %s;", (email,))
                if cursor.fetchone():
                    self.mostrar_error("El correo ya está en uso.")
                    return

                # Si el correo no existe, insertar el nuevo usuario
                cursor.execute("INSERT INTO usuario (nombre, email, password, celular) VALUES (%s, %s, %s, %s)",
                               (nombre, email, password, celular))
                connection.commit()  # Confirmar la transacción
                self.mostrar_mensaje("Usuario creado con éxito.")
                self.regresar_login()
        except psycopg2.Error as e:
            self.mostrar_error(f"Error: {e}")
            print(f"Error al registrar usuario: {e}")  # Mensaje de depuración

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
