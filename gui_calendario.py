import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import datos
from eventos import*
from etiquetas import*
from etiqueta_evento import*
import mysql.connector


class App(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=2)
        self.parent=parent
       

        #grillas del trievew
        columna=('id', 'Titulo', 'Fecha_y_Hora', 'Duracion','Descripcion', 'Importancia')
        self.arbol=ttk.Treeview(parent, columns=columna, show='headings')

        self.arbol.heading('id', text='ID')
        self.arbol.heading('Titulo', text='Titulo')
        self.arbol.heading('Fecha_y_Hora', text='Fecha y Hora')
        self.arbol.heading('Duracion', text='Duracion')
        self.arbol.heading('Descripcion', text='Descripcion')
        self.arbol.heading('Importancia', text='Importancia')

        self.arbol.grid(row=0, column=0, padx = 1, pady = 1)

        #Botones de la ventana principal
        ttk.Button(self, text="Crear", command=self.abrir_ventana).grid()
        ttk.Button(self, text="Editar", command=self.editar_evento).grid()
        ttk.Button(self, text="Eliminar", command=self.eliminar_evento).grid()
        #ttk.Button(self, text="Ver", command=self.ver_evento).grid()
        
        self.arbol.bind('<<TreeviewSelect>>', self.item_seleccionado)
        self.cargar_tabla()
    
    def cargar_tabla(self):
        registros = datos.get_evento()
        id = 0
        for evento in registros:
            self.arbol.insert(parent='', index='end', text="", values=(id, evento['Titulo'],evento['Fecha y Hora'],evento['Duracion'],evento['Descripcion'],evento['Importancia']))
            id+=1
    
    def item_seleccionado(self, event):
        seleccion =self.arbol.selection()
        # si selection() devuelve una tupla vacia, no hay seleccion
        if seleccion:
            for item_id in seleccion:
                item = self.arbol.item(item_id) # obtenemos el item y sus datos
                fila= item['values'][0]

    def abrir_ventana(self):
        # creamos la ventana Alta
        # como padre indicamos la ventana principal
        toplevel = tk.Toplevel(self.parent)
        # agregamos el frame (Alta) a la ventana (toplevel)
        Alta(toplevel, self).grid()

    def actualizar_lista(self, evento):
        # add data to the treeview
        self.arbol.insert('', tk.END, values=evento)

    def editar_evento(self):
        seleccion = self.arbol.selection()
        # si selection() devuelve una tupla vacia, no hay seleccion
        if seleccion:
            for item_id in seleccion:
                item = self.arbol.item(item_id) # obtenemos el item y sus datos
                id_evento = item['values'][0] # capturo el id de mi registro
                #Receta.eliminar(id_receta) # actualizo mi .json
                #self.tree.delete(item_id) # actualizo treeview

                # creamos la ventana Alta
                # como padre indicamos la ventana principal
                toplevel = tk.Toplevel(self.parent)
                # agregamos el frame (Alta) a la ventana (toplevel)
                self.ventana_editar = Editar(toplevel, self)
                self.ventana_editar.grid() 
                
                self.ventana_editar.set_id(item['values'][0])
                self.ventana_editar.set_titulo(item['values'][1])
                self.ventana_editar.set_fecha_y_hora(item['values'][2])
                self.ventana_editar.set_duracion(item['values'][3])
                self.ventana_editar.set_descripcion(item['values'][4])
                self.ventana_editar.set_importancia(item['values'][5])

    def clear_all(self):
        for item in self.arbol.get_children():
            self.arbol.delete(item)

    def eliminar_evento(self):
        seleccion = self.arbol.selection()
        # si selection() devuelve una tupla vacia, no hay seleccion
        if seleccion:
            for item_id in seleccion:
                item = self.arbol.item(item_id) # obtenemos el item y sus datos
                id_evento = item['values'][0] # capturo el id de mi registro
                print("Id:",id_evento)
                if messagebox.askyesno(message="¿Desea eliminar el '"+item['values'][1]+"'?", title="Advertencia"):
                    Evento.eliminar(id_evento) # actualizo mi .json
                    self.arbol.delete(item_id) # actualizo treeview

#Ventanas secundarias
class Alta(ttk.Frame):
    def __init__(self, parent, marco):
        super().__init__(parent, padding=(20))
        self.parent = parent
        self.marco = marco
        parent.title("Nuevo Evento")
        parent.geometry("500x300+180+100")
        self.grid(sticky=(tk.N, tk.S, tk.E, tk.W))
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        parent.resizable(False, False)

        self.titulo = tk.StringVar()
        self.fecha_y_hora = tk.StringVar()
        self.duracion = tk.StringVar()
        self.descripcion = tk.StringVar()
        self.importancia = tk.StringVar()

        ttk.Label(self, text="Titulo:").grid(row=1, column=1, sticky=tk.W, padx=3, pady=3)
        ttk.Entry(self, textvariable=self.titulo).grid(row=1, column=2, columnspan=3)
        ttk.Label(self, text="Fecha y Hora:").grid(row=2, column=1, sticky=tk.W,  padx=3, pady=3)
        ttk.Entry(self, textvariable=self.fecha_y_hora).grid(row=2, column=2, columnspan=3)
        ttk.Label(self, text="Duracion:").grid(row=3, column=1, sticky=tk.W,  padx=3, pady=3)
        ttk.Entry(self, textvariable=self.duracion).grid(row=3, column=2, columnspan=3)
        ttk.Label(self, text="Descripcion:").grid(row=4, column=1, sticky=tk.W,  padx=3, pady=3)
        ttk.Entry(self, textvariable=self.descripcion).grid(row=4, column=2, columnspan=3)
        ttk.Label(self, text="Importancia:").grid(row=5, column=1, sticky=tk.W,  padx=3, pady=3)
        ttk.Radiobutton(self, text="Normal",
                        value="Normal", variable=self.importancia,
                 command = lambda : self.on_importancia_changed).grid(row=5, column=2)
        ttk.Radiobutton(self, text="Importante",
                        value="Importante", variable=self.importancia,
                 command = lambda : self.on_importancia_changed).grid(row=5, column=3)
    
        #ttk.Label(self, text="nombre").grid(row=7, column=1, sticky=tk.W,  padx=3, pady=3)
        #combo=ttk.Combobox(self, values=["Cumpleaños","Viaje","Boda","Reunion","Entrevista","Torneo"], textvariable=nombre)
        ##ttk.Button(self, text="Elegir", command=self.on_importancia_changed).grid(row=6, column=3)
    
     
        ttk.Button(self, text="Guardar", command=self.guardar_evento).grid(row=8, column=1)
        ttk.Button(self, text="Cerrar", command=parent.destroy).grid(row=9, column=1)
    """def selection_changed(self):
        selection=combo.get()
        messagebox.showinfo(title="Nuevo elemento seleccinado", message=selection)"""

    def on_importancia_changed(self):
        evento=Evento
        evento.set_importancia.get()

    def guardar_evento(self):
        evento=Evento()
        evento.set_titulo(self.titulo.get())
        evento.set_fecha_y_hora(self.fecha_y_hora.get())
        evento.set_duracion(self.duracion.get())
        evento.set_descripcion(self.descripcion.get())
        evento.set_importancia(self.importancia.get())
        evento.guardar()
            
        self.parent.destroy()

    def editar_evento(self):
        seleccion = self.arbol.selection()
        # si selection() devuelve una tupla vacia, no hay seleccion
        if seleccion:
            for item_id in seleccion:
                item = self.arbol.item(item_id) # obtenemos el item y sus datos
                id_evento = item['values'][0] # capturo el id de mi registro
                #Receta.eliminar(id_receta) # actualizo mi .json
                #self.tree.delete(item_id) # actualizo treeview

                # creamos la ventana Alta
                # como padre indicamos la ventana principal
                toplevel = tk.Toplevel(self.parent)
                # agregamos el frame (Alta) a la ventana (toplevel)
                self.ventana_editar = Editar(toplevel, self)
                self.ventana_editar.grid() 
                
                self.ventana_editar.set_id(item['values'][0])
                self.ventana_editar.set_titulo(item['values'][1])
                self.ventana_editar.set_fecha_y_hora(item['values'][2])
                self.ventana_editar.set_duracion(item['values'][3])
                self.ventana_editar.set_descripcion(item['values'][4])
                self.ventana_editar.set_importancia(item['values'][5])

    def clear_all(self):
        for item in self.arbol.get_children():
            self.arbol.delete(item)


class Editar(ttk.Frame):
    def __init__(self, parent, marco):
        super().__init__(parent, padding=(20))
        self.parent = parent
        self.marco = marco
        parent.title("Editar Evento")
        parent.geometry("500x300+180+100")
        self.grid(sticky=(tk.N, tk.S, tk.E, tk.W))
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        parent.resizable(False, False)

        self.id = None
        self.titulo = tk.StringVar()
        self.fecha_y_hora = tk.StringVar()
        self.duracion = tk.StringVar()
        self.descripcion = tk.StringVar()
        self.importancia = tk.StringVar()

        ttk.Label(self, text="Titulo:").grid(row=1, column=1, sticky=tk.W, padx=3, pady=3)
        ttk.Entry(self, textvariable=self.titulo).grid(row=1, column=2,  columnspan=3)
        ttk.Label(self, text="Fecha y Hora:").grid(row=2, column=1, sticky=tk.W, padx=3, pady=3)
        ttk.Entry(self, textvariable=self.fecha_y_hora).grid(row=2, column=2,  columnspan=3)
        ttk.Label(self, text="Duracion:").grid(row=3, column=1, sticky=tk.W, padx=3, pady=3)
        ttk.Entry(self, textvariable=self.duracion).grid(row=3, column=2,  columnspan=3)
        ttk.Label(self, text="Descripcion:").grid(row=4, column=1,sticky=tk.W, padx=3, pady=3)
        self.cuadro_texto = tk.Text(self)
        self.cuadro_texto.config(height=5, width=50)
        self.cuadro_texto.grid(row=4, column=2, pady=10, padx=10, sticky=tk.NSEW)
        self.cuadro_texto.insert('1.0', self.descripcion.get())

        ttk.Label(self, text="Importancia:").grid(row=5, column=1, sticky=tk.W, padx=3, pady=3)
        ttk.Entry(self, textvariable=self.importancia).grid(row=5, column=2)
        
        ttk.Button(self, text="Guardar", command=self.editar_evento).grid(row=6, column=1)
        ttk.Button(self, text="Cerrar", command=parent.destroy).grid(row=6, column=3)

    def set_id(self, id):
        self.id = id

    def set_titulo(self, titulo):
        self.titulo.set(titulo)
    
    def set_descripcion(self, descripcion):
        self.descripcion.set(descripcion)
        self.cuadro_texto.insert('1.0', self.descripcion.get())
    
    def set_fecha_y_hora(self, fecha_y_hora):
        self.fecha_y_hora.set(fecha_y_hora)

    def set_duracion(self, duracion):
        self.duracion.set(duracion)

    def set_importancia(self, importancia):
        self.importancia.set(importancia)

    def editar_evento(self):
        #print("duracion", self.duracion)

        eventos =Evento()
        eventos.set_id(self.id)
        eventos.set_titulo(self.titulo.get())
        eventos.set_duracion(self.duracion.get())
        eventos.set_descripcion(self.cuadro_texto.get('1.0', 'end'))
        eventos.set_fecha_y_hora(self.fecha_y_hora.get())
        eventos.set_importancia(self.importancia.get())
        eventos.editar(self.id)
        
        self.marco.clear_all()
        self.marco.cargar_tabla()
    
        self.parent.destroy()

class Elimionar:
    pass


       
        
    
    

