import mysql.connector
from mysql.connector import errors
import config 

def conectar():
    """Conecta con la base de datos y devuelve un objeto conexion"""
    try:
        conn = mysql.connector (**config.credenciales)
    
        if conn.is_connected():
            print("Conexion Exitosa")
        cursor=conn.cursor()
        cursor.execute("SELECT DATABASE()*")
        row=cursor.fetchone()
        print("Conectado a la base de datos: {}".format(row))

    except errors.DatabaseError as err:
        print("Error al Conectar", err)
    else:
        return conn    
    finally:
        if conn.is_connected():
            conn.close()
            print("Conexion Finalizada")

def nuevo_evento(titulo, fecha_y_hora, duracion, descripcion, importancia):
    query = "INSERT INTO eventos (titulo, fecha_y_hora, duracion, descripcion, importancia) VALUES(%s, %s, %s, %s, %s)".format(titulo, fecha_y_hora, duracion, descripcion, importancia)
    conn=conectar()
    cur=conn.cursor()
    cur.execute(query,(titulo, fecha_y_hora, duracion, descripcion, importancia,))
    conn.commit()
    conn.close()

def editar_evento():
   pass

def eliminar_evento(id_evento):
    query = "DELETE FROM eventos (id_evento)  WHERE id_evento=%s".format(id_evento)
    conn=conectar()
    cur=conn.cursor()
    cur.execute(query,(id_evento,))
    conn.commit()
    conn.close()

def get_evento():
    consulta="""SELECT id_evento, titulo, fecha_y_hora, duracion, descripcion, importancia, etiqueta
                FROM eventos {} """
    WHERE = "WHERE eventos={}"
    conn=conectar()
    cur=conn.cursor()
    cur.execute(consulta)
    resultado=cur.fetchall()
    conn.close()
    return resultado
    

def create_if_not_exists():
    create_database = "CREATE DATABASE IF NOT EXISTS %s" %config.credenciales["database"]
    
    create_table_1 = """CREATE TABLE IF NOT EXISTS eventos (
                        id_evento INT NOT NULL AUTO_INCREMENT UNIQUE PRIMARY KEY,
                        titulo VARCHAR(100) NOT NULL,
                        fecha_y_hora DATETIME NOT NULL,
                        duracion TIME NOT NULL DEFAULT '00:01:00',
                        descripcion TEXT NOT NULL,
                        importancia VARCHAR(45) NOT NULL DEFAULT 'NORMAL'
                        )"""
    
    create_table_2 = """CREATE TABLE IF NOT EXISTS etiquetas (
                        id_etiqueta INT NOT NULL  AUTO_INCREMENT UNIQUE PRIMARY KEY,
                        nombre VARCHAR(45) NOT NULL
                        )"""

    create_table_3 = """CREATE TABLE IF NOT EXISTS etiqueta_evento (
                        id_evento INT NOT NULL,
                        id_etiqueta INT NOT NULL,
	                    CONSTRAINT id_etiqueta FOREIGN KEY (id_etiqueta) REFERENCES etiquetas (id_etiqueta),
                        CONSTRAINT id_evento FOREIGN KEY (id_evento) REFERENCES eventos (id_evento)
                        ) ENGINE=InnoDB;"""

    try:
        conn = mysql.connection.connect(user=config.credenciales["user"],
                                        password=config.credenciales["password"],
                                        host="127.0.0.1")
        cur=conn.cursor()
        cur.execute(create_database)
        cur.execute("USE %s" %config.credenciales["database"])
        cur.execute(create_table_1)
        cur.execute(create_table_2)
        cur.execute(create_table_3)
        conn.commit()
        conn.close()
    except errors.DatabaseError as err:
        print("Error al conectar o Crear la base de dats", err)
        raise
    

