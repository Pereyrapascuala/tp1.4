
import tkinter as tk
import gui_calendario
import config 
import eventos
import etiqueta_evento
import etiquetas
import datos


def main():
    # crear db y tabla si no existe
    datos.create_if_not_exists()

    
    root = tk.Tk()
    root.title("CALENDARIO")
    root.geometry("800x600+100+100")
    root.config(bg="#B5F1CC")
    gui_calendario(root).grid(sticky=(tk.N, tk.S, tk.E, tk.W))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.resizable(False, False)
    #App(root).grid()
    root.mainloop()

if __name__ == "__main__":
    main