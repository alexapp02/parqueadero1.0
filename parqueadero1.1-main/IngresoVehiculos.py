import sys
import datetime
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton,
                             QVBoxLayout, QMessageBox, QTableWidget, QTableWidgetItem, QInputDialog)
from login.database import Database  # Asegúrate de que la clase Database esté en el archivo adecuado


class IngresoVehiculos(QWidget):
    def __init__(self):
        super().__init__()
        self.conexion = Database("postgres", "Soloparami34", "localhost").conectar()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Sistema de Parqueadero")
        self.setGeometry(100, 100, 700, 400)  # Ajustar el ancho para nuevas columnas

        # Crear layout principal
        layout = QVBoxLayout()

        # Etiquetas y campos de entrada
        self.placa_label = QLabel("Placa:")
        self.placa_entry = QLineEdit()

        self.tipo_label = QLabel("Tipo de Vehículo:")
        self.tipo_entry = QLineEdit()

        self.hora_entrada_label = QLabel("Hora de Entrada (HH:MM):")
        self.hora_entrada_entry = QLineEdit()

        self.id_espacio_label = QLabel("ID de Espacio:")
        self.id_espacio_entry = QLineEdit()

        # Botón de registrar vehículo
        self.registrar_button = QPushButton("Registrar Vehículo")
        self.registrar_button.clicked.connect(self.registrar_vehiculo)

        # Tabla para mostrar los vehículos registrados
        self.tabla_vehiculos = QTableWidget()
        self.tabla_vehiculos.setColumnCount(7)  # Placa, Tipo, Hora Entrada, Hora Salida, Espacio Asignado, Estado, Editar
        self.tabla_vehiculos.setHorizontalHeaderLabels(["Placa", "Tipo", "Hora Entrada", "Hora Salida", "Espacio Asignado", "Estado", "Editar"])

        # Botón para cargar la tabla con los vehículos
        self.cargar_vehiculos_button = QPushButton("Cargar Vehículos")
        self.cargar_vehiculos_button.clicked.connect(self.cargar_vehiculos)

        # Añadir widgets al layout
        layout.addWidget(self.placa_label)
        layout.addWidget(self.placa_entry)
        layout.addWidget(self.tipo_label)
        layout.addWidget(self.tipo_entry)
        layout.addWidget(self.hora_entrada_label)
        layout.addWidget(self.hora_entrada_entry)
        layout.addWidget(self.id_espacio_label)
        layout.addWidget(self.id_espacio_entry)
        layout.addWidget(self.registrar_button)
        layout.addWidget(self.cargar_vehiculos_button)
        layout.addWidget(self.tabla_vehiculos)

        # Establecer layout en la ventana
        self.setLayout(layout)

    def registrar_vehiculo(self):
        placa = self.placa_entry.text()
        tipo_vehiculo = self.tipo_entry.text()
        hora_entrada = self.hora_entrada_entry.text()
        id_espacio = self.id_espacio_entry.text()

        if not (placa and tipo_vehiculo and hora_entrada and id_espacio):
            QMessageBox.warning(self, "Error", "Por favor complete todos los campos.")
            return

        # Validar formato de hora y convertir a datetime
        try:
            hora_entrada_obj = datetime.datetime.strptime(hora_entrada, "%H:%M")
            hora_entrada_obj = datetime.datetime.combine(datetime.datetime.today().date(), hora_entrada_obj.time())
        except ValueError:
            QMessageBox.warning(self, "Error", "La hora debe estar en formato HH:MM.")
            return

        # Verificar disponibilidad del espacio
        verificar_espacio_query = "SELECT estado FROM espacio WHERE id_espacio = %s"
        cursor = self.conexion.cursor()
        try:
            cursor.execute(verificar_espacio_query, (id_espacio,))
            estado_espacio = cursor.fetchone()

            if estado_espacio is None:
                QMessageBox.warning(self, "Error", "El ID de espacio no existe.")
                return

            if estado_espacio[0] != 'disponible':
                QMessageBox.warning(self, "Error", "El espacio no está disponible.")
                return

            # Registrar vehículo en la base de datos
            query = """
            INSERT INTO vehiculo (placa, tipo_vehiculo, hora_entrada, hora_salida, id_espacio)
            VALUES (%s, %s, %s, NULL, %s);
            """
            values = (placa, tipo_vehiculo, hora_entrada_obj, id_espacio)

            cursor.execute(query, values)
            self.conexion.commit()

            # Cambiar el estado del espacio a "ocupado"
            actualizar_espacio_query = "UPDATE espacio SET estado = 'ocupado' WHERE id_espacio = %s"
            cursor.execute(actualizar_espacio_query, (id_espacio,))
            self.conexion.commit()

            QMessageBox.information(self, "Éxito", "Vehículo registrado exitosamente.")
            self.clear_fields()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al registrar el vehículo: {e}")
            self.conexion.rollback()
        finally:
            cursor.close()

    def clear_fields(self):
        self.placa_entry.clear()
        self.tipo_entry.clear()
        self.hora_entrada_entry.clear()
        self.id_espacio_entry.clear()

    def cargar_vehiculos(self):
        cursor = self.conexion.cursor()
        query = "SELECT placa, tipo_vehiculo, hora_entrada, hora_salida, id_espacio FROM vehiculo"
        cursor.execute(query)
        vehiculos = cursor.fetchall()
        self.tabla_vehiculos.setRowCount(len(vehiculos))

        for row_idx, vehiculo in enumerate(vehiculos):
            for col_idx, data in enumerate(vehiculo):
                self.tabla_vehiculos.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))

            # Agregar la columna de Espacio Asignado
            id_espacio = vehiculo[4]  # ID del espacio
            self.tabla_vehiculos.setItem(row_idx, 4, QTableWidgetItem(str(id_espacio)))

            # Agregar la columna de Estado
            estado = "Presente" if vehiculo[3] is None else "No Presente"  # La hora de salida está en la posición 3
            self.tabla_vehiculos.setItem(row_idx, 5, QTableWidgetItem(estado))

            # Crear un botón para editar la hora de salida
            editar_button = QPushButton("Editar")
            editar_button.clicked.connect(lambda _, idx=row_idx: self.editar_hora_salida(idx))
            self.tabla_vehiculos.setCellWidget(row_idx, 6, editar_button)

        cursor.close()

    def editar_hora_salida(self, row_idx):
        placa = self.tabla_vehiculos.item(row_idx, 0).text()
        hora_entrada_str = self.tabla_vehiculos.item(row_idx, 2).text()

        # Convertir hora de entrada a datetime
        hora_entrada_obj = datetime.datetime.strptime(hora_entrada_str, "%Y-%m-%d %H:%M:%S")

        # Solicitar la hora de salida al usuario
        hora_salida, ok = QInputDialog.getText(self, "Editar Hora de Salida", "Ingrese la hora de salida (HH:MM):")

        if ok and hora_salida:
            try:
                # Validar el formato de la hora de salida
                hora_salida_obj = datetime.datetime.strptime(hora_salida, "%H:%M")
                hora_salida_obj = datetime.datetime.combine(datetime.datetime.today().date(), hora_salida_obj.time())

                # Validar que la hora de salida no sea menor a la hora de entrada
                if hora_salida_obj < hora_entrada_obj:
                    QMessageBox.warning(self, "Error", "La hora de salida no puede ser anterior a la hora de entrada.")
                    return
            except ValueError:
                QMessageBox.warning(self, "Error", "La hora debe estar en formato HH:MM.")
                return

            cursor = self.conexion.cursor()
            query = "UPDATE vehiculo SET hora_salida = %s WHERE placa = %s"
            cursor.execute(query, (hora_salida_obj, placa))
            self.conexion.commit()

            # Cambiar el estado del espacio a "disponible" después de que el vehículo haya salido
            actualizar_espacio_query = """
            UPDATE espacio
            SET estado = 'disponible'
            WHERE id_espacio = (
                SELECT id_espacio
                FROM vehiculo
                WHERE placa = %s
            )
            """
            cursor.execute(actualizar_espacio_query, (placa,))
            self.conexion.commit()

            QMessageBox.information(self, "Éxito",
                                    f"Hora de salida actualizada y espacio liberado para el vehículo con placa {placa}.")
            self.cargar_vehiculos()  # Recargar la tabla actualizada

            cursor.close()


# Código principal
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = IngresoVehiculos()
    ventana.show()
    sys.exit(app.exec_())
