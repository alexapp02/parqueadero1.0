import psycopg2
from psycopg2 import sql
from datetime import datetime

def conectar_db():
    try:
        conn = psycopg2.connect(
            host="localhost",       # Cambia por la dirección de tu servidor
            database="nombre_db",    # Nombre de tu base de datos
            user="tu_usuario",       # Usuario de la base de datos
            password="tu_contraseña" # Contraseña del usuario
        )
        return conn
    except Exception as error:
        print(f"Error conectando a la base de datos: {error}")
        return None

def verificar_disponibilidad(conn, espacio, fecha, hora_entrada, hora_salida):
    cursor = conn.cursor()
    try:
        query = sql.SQL('''
            SELECT COUNT(*) 
            FROM reservaciones 
            WHERE espacio = %s 
            AND fecha = %s 
            AND estado = 'Activa'
            AND (
                (%s BETWEEN hora_entrada AND hora_salida) OR
                (%s BETWEEN hora_entrada AND hora_salida) OR
                (hora_entrada BETWEEN %s AND %s)
            )
        ''')
        cursor.execute(query, (espacio, fecha, hora_entrada, hora_salida, hora_entrada, hora_salida))
        resultado = cursor.fetchone()[0]
        if resultado == 0:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error al verificar la disponibilidad: {e}")
        return False

def crear_reserva(conn, espacio, fecha, hora_entrada, hora_salida):
    cursor = conn.cursor()
    if verificar_disponibilidad(conn, espacio, fecha, hora_entrada, hora_salida):
        try:
            query = sql.SQL('''
                INSERT INTO reservaciones (espacio, fecha, hora_entrada, hora_salida, estado)
                VALUES (%s, %s, %s, %s, 'Activa')
            ''')
            cursor.execute(query, (espacio, fecha, hora_entrada, hora_salida))
            conn.commit()
            print("Reservación creada exitosamente.")
        except Exception as e:
            print(f"Error al crear la reservación: {e}")
            conn.rollback()
    else:
        print("El espacio no está disponible en ese horario.")

def cancelar_reserva(conn, id_reserva):
    cursor = conn.cursor()
    try:
        query = sql.SQL('''
            UPDATE reservaciones
            SET estado = 'Cancelada'
            WHERE id = %s AND estado = 'Activa'
        ''')
        cursor.execute(query, (id_reserva,))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"Reservación {id_reserva} cancelada exitosamente.")
        else:
            print(f"No se pudo cancelar la reservación {id_reserva}. Puede que ya esté cancelada o no exista.")
    except Exception as e:
        print(f"Error al cancelar la reservación: {e}")
        conn.rollback()

if __name__ == "__main__":
    conn = conectar_db()

    if conn:
        crear_reserva(
            conn,
            espacio=5,
            fecha=datetime(2024, 10, 20).date(),
            hora_entrada=datetime(2024, 10, 20, 10, 0).time(),
            hora_salida=datetime(2024, 10, 20, 12, 0).time()
        )
        cancelar_reserva(conn, id_reserva=1)
