import psycopg2
def conectar_db():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="parqueadero1.0",
            user="postgres",
            password="321325"
        )
        return conn
    except Exception as error:
        print(f"Error conectando a la base de datos: {error}")
        return None

def ver_historial(conn):
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT fecha, espacio, nombre_usuario, email, hora_entrada, hora_salida FROM historial')
        registros = cursor.fetchall()

        print("Historial:")
        for registro in registros:
            fecha, espacio, nombre_usuario, email, hora_entrada, hora_salida = registro
            print(
                f"Fecha: {fecha}, Espacio: {espacio}, Usuario: {nombre_usuario}, Email: {email}, Entrada: {hora_entrada}, Salida: {hora_salida}")

    except Exception as e:
        print(f"Error al consultar el historial: {e}")

def ver_historial_facturacion(conn):
    cursor = conn.cursor()
    try:
        cursor.execute('''
            SELECT fecha, espacio, nombre_usuario, email, hora_entrada, hora_salida, id_factura, precio_final 
            FROM historial
        ''')
        registros = cursor.fetchall()

        print("Historial facturacion:")
        for registro in registros:
            fecha, espacio, nombre_usuario, email, hora_entrada, hora_salida, id_factura, precio_final = registro
            print(f"Fecha: {fecha}, Espacio: {espacio}, Usuario: {nombre_usuario}, Email: {email}, Entrada: {hora_entrada}, Salida: {hora_salida}, Factura ID: {id_factura}, Precio Final: {precio_final}")

    except Exception as e:
        print(f"Error al consultar el historial de facturacion: {e}")

if __name__ == "__main__":
    # Conexión a la base de datos
    conn = conectar_db()

    if conn:
        # Ver historial básico
        print("===== Historial Básico =====")
        ver_historial(conn)

        # Ver historial completo con factura y precio final
        print("\n===== Historial Completo =====")
        ver_historial_completo(conn)

        # Cerrar la conexión
        conn.close()