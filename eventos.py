from datetime import datetime
import json
import etiqueta_evento
import etiquetas

class Evento():
    def __init__(self):
        self.id=" "
        self.titulo = " "
        self.fecha_y_hora = " "
        self.duracion = 1
        self.descripcion = " "
        self.importancia = " "

    def set_id(self, id):
        self.id = id

    def set_titulo(self, titulo):
        self.titulo = titulo
    
    def set_fecha_y_hora(self, fecha_y_hora):
        self.fecha_y_hora = fecha_y_hora

    def set_duracion(self, duracion):
        self.duracion = duracion

    def set_descripcion(self, descripcion):
        self.descripcion = descripcion

    def set_importancia(self, importancia):
        self.importancia = importancia

    def set_id(self):
        return self.id

    def set_titulo(self):
        return self.titulo 
    
    def set_fecha_y_hora(self):
        return self.fecha_y_hora 

    def set_duracion(self):
        return self.duracion 

    def set_descripcion(self):
        return self.descripcion 

    def set_importancia(self):
        return self.importancia 

def guardar(self):
        with open('evento2.json', 'r') as archivo:
            try:
                eventos = json.load(archivo)
            except ValueError:
                eventos=[]

        evento={}
        evento["id"]= len(eventos) 
        evento["Titulo"] = self.titulo
        evento["Fecha y Hora"] = self.fecha_y_hora
        evento["Duracion"] = self.duracion
        evento["Descripcion"] = self.descripcion
        evento["Importancia"] = self.importancia
        eventos.append(evento)

        with open ('evento2.json', 'w') as archivo:
            json.dump(eventos, archivo, indent=4)

    
def editar(self, id_evento):
    with open("evento2.json", 'r') as archivo:
        try:
                eventos = json.load(archivo)
        except ValueError:
                pass
    aux = []
    indice = 0
    for elem in eventos:
        if indice != id_evento:
            aux.append(elem)
        else:
            print("elemento ", elem)
            evento = {}
            evento["id"] = id_evento
            evento["Titulo"] = self.titulo
            evento["Fecha y Hora"] = self.fecha_y_hora
            evento["Descripcion"] = self.descripcion
            evento["Duracion"] = self.duracion
            evento["Importancia"] = self.importancia
            aux.append(evento)
        indice += 1
    eventos = aux

    with open("evento2.json", 'w') as archivo:
        json.dump(eventos, archivo, indent=4)

@staticmethod
def eliminar(id_evento):
    with open("evento2.json", 'r') as archivo:
        try:
                eventos = json.load(archivo)
        except ValueError:
                pass
    aux = []
    indice=0
    for elem in eventos:
        if indice != id_evento:
            aux.append(elem)
        indice+=1

        eventos = aux

        with open("evento2.json", 'w') as archivo:
            json.dump(eventos, archivo, indent=4)

