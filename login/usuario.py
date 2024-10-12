import psycopg2

class Usuario:
    nombre = ""
    email = ""
    password = ""
    telefono = ""

    def __init__(self, nombre, email, password, telefono):
        self.nombre = nombre
        self.email = email
        self.password = password
        self.telefono = telefono

    def crearUsuario(conexion, nombre, email, password, telefono):
        try:
            with conexion.cursor() as cursor:
                # Cambiado el nombre de la tabla a minúsculas
                consulta = "INSERT INTO usuario (nombre, email, password, telefono) VALUES (%s, %s, %s, %s);"
                cursor.execute(consulta, (nombre, email, password, telefono))
            conexion.commit()
            print("Usuario creado con éxito")
            return True
        except psycopg2.Error as e:
            print("Ocurrió un error al crear el usuario: ", e)
            return False

    def consultarUsuario(conexion, id_usuario):
        try:
            with conexion.cursor() as cursor:
                # Cambiado el nombre de la tabla y la columna a minúsculas
                cursor.execute("SELECT * FROM usuario WHERE id_usuario = %s;", (id_usuario,))
                usuario = cursor.fetchone()
                if usuario:
                    print(usuario)
                else:
                    print("El usuario no existe")
        except psycopg2.Error as e:
            print("Ocurrió un error al consultar: ", e)

    def consultarUsuarios(conexion):
        try:
            with conexion.cursor() as cursor:
                # Cambiado el nombre de la tabla a minúsculas
                cursor.execute("SELECT * FROM usuario;")
                usuarios = cursor.fetchall()
                for usuario in usuarios:
                    print(usuario)
        except psycopg2.Error as e:
            print("Ocurrió un error al consultar: ", e)

    def actualizarUsuario(conexion, id_usuario, nombre, email, telefono):
        try:
            with conexion.cursor() as cursor:
                # Cambiado el nombre de la tabla y columnas a minúsculas
                consulta = "UPDATE usuario SET nombre = %s, email = %s, telefono = %s WHERE id_usuario = %s;"
                cursor.execute(consulta, (nombre, email, telefono, id_usuario))
            conexion.commit()
            print("El registro se actualizó con éxito")
        except psycopg2.Error as e:
            print("Ocurrió un error al actualizar: ", e)

    def eliminarUsuario(conexion, id_usuario):
        try:
            with conexion.cursor() as cursor:
                # Cambiado el nombre de la tabla y columna a minúsculas
                consulta = "DELETE FROM usuario WHERE id_usuario = %s;"
                cursor.execute(consulta, (id_usuario,))
                print("Usuario eliminado con éxito")
            conexion.commit()
        except psycopg2.Error as e:
            print("Error eliminando: ", e)
