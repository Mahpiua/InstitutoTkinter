import sqlite3


def iniciar_conexion():
    return sqlite3.connect("instituto.db")


def crear_bd():
    # Creamos la conexion
    conexion = iniciar_conexion()

    # Creamos el cursor
    cursor = conexion.cursor()

    # cursor.execute("INSERT INTO persona)
    conexion.commit()
    # cursor.execute("SELECT * from persona")
    conexion.close()

    def iniciar_carga():
        # Creamos la conexion
        conexion = iniciar_conexion()

        # Creamos el cursor
        cursor = conexion.cursor()

        # Insert inicial

        # Se realiza la conexion
        conexion.commit()

        # Cerramos la conexion
        conexion.close()