import psycopg2

class Administrador:
    nombre = ""
    email = ""
    password = ""

    def __init__(self, nombre, email, password):
        self.nombre = nombre
        self.email = email
        self.password = password

    def crearAdministrador(conexion, nombre, email, password):
        try:
            with conexion.cursor() as cursor:
                # Cambiado el nombre de la tabla a minúsculas
                consulta = "INSERT INTO administrador (nombre, email, password) VALUES (%s, %s, %s);"
                cursor.execute(consulta, (nombre, email, password))
            conexion.commit()
            print("Administrador creado con éxito")
            return True
        except psycopg2.Error as e:
            print("Ocurrió un error al crear el administrador: ", e)
            return False

    def consultarAdministrador(conexion, id_administrador):
        try:
            with conexion.cursor() as cursor:
                # Cambiado el nombre de la tabla y la columna a minúsculas
                cursor.execute("SELECT * FROM administrador WHERE id_administrador = %s;", (id_administrador,))
                administrador = cursor.fetchone()
                if administrador:
                    print(administrador)
                else:
                    print("El administrador no existe")
        except psycopg2.Error as e:
            print("Ocurrió un error al consultar: ", e)

    def consultarAdministradores(conexion):
        try:
            with conexion.cursor() as cursor:
                # Cambiado el nombre de la tabla a minúsculas
                cursor.execute("SELECT * FROM administrador;")
                administradores = cursor.fetchall()
                for administrador in administradores:
                    print(administrador)
        except psycopg2.Error as e:
            print("Ocurrió un error al consultar: ", e)

    def actualizarAdministrador(conexion, id_administrador, nombre, email):
        try:
            with conexion.cursor() as cursor:
                # Cambiado el nombre de la tabla y columna a minúsculas
                consulta = "UPDATE administrador SET nombre = %s, email = %s WHERE id_administrador = %s;"
                cursor.execute(consulta, (nombre, email, id_administrador))
            conexion.commit()
            print("El registro se actualizó con éxito")
        except psycopg2.Error as e:
            print("Ocurrió un error al actualizar: ", e)

    def eliminarAdministrador(conexion, id_administrador):
        try:
            with conexion.cursor() as cursor:
                # Cambiado el nombre de la tabla y columna a minúsculas
                consulta = "DELETE FROM administrador WHERE id_administrador = %s;"
                cursor.execute(consulta, (id_administrador,))
                print("Administrador eliminado con éxito")
            conexion.commit()
        except psycopg2.Error as e:
            print("Error eliminando: ", e)
