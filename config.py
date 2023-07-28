import mysql.connector
#Conexion a la base de datos
credenciales = {"user" : "root", 
             "password" : "root", 
             "host" : "127.0.0.1", 
             "datebase" : "calendario_de_eventos"}

"""class BaseDatos:
    def __init__(self,**kwargs):
        self.conn = mysql.connector.connect(**kwargs)
        self.cursor = self.conector.cursor()
    # Hace una consulta
    def consulta(self, sql):
        self.cursor.execute(sql)
        return self.cursor
    # Muestra las bases de datos del servidor
    def mostrar_bd(self):
        self.cursor.execute("SHOW DATABASES")
        for bd in self.cursor:
            print(bd)"""
