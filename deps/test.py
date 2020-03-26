#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *   
from tkinter import ttk  


welcome_text = ''' 
___________________________________________________________
|                                                         |
|                  MTG COLLECTOR MANAGER                  |
|_________________________________________________________|

Welcome to my mtg collector. 

'''


class Aplicacion():
    def __init__(self):
        
        
        # Window
        self.raiz = Tk()
        self.raiz.title('My MTG collection app')
        
        self.raiz.image = PhotoImage('mtg.jpg')
        background_label = Label(self.raiz, image=self.raiz.image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        
        #self.raiz.configure(bg = '#AFC3D2')
        #background_label = Label(self.raiz, #image=background_image)
        #background_label.pack()
        #self.raiz.geometry('900x600')
        
        
        # Frames
        
        topFrame = Frame(self.raiz)
        topFrame.pack()
        
        bottomFrame = Frame(self.raiz)
        bottomFrame.pack(side=BOTTOM,padx=5, pady=10)
        
        
        # Main text
        self.tinfo = Text(topFrame)
        self.tinfo.tag_configure("center", justify='center')
        self.tinfo.insert("1.0", welcome_text)  
        self.tinfo.tag_add("center","1.0","end")
        self.tinfo.pack(side=TOP) 
        
        # Buttons
        self.showCollection = ttk.Button(bottomFrame, text="Show collections", command=self.showCollection)
        
        
        self.exit = ttk.Button(bottomFrame, text='Salir', command=self.raiz.destroy)
        
        self.exit.grid(column=5, row = 1,padx=(100,5), pady=5)
        self.showCollection.grid(column=0, row = 1,padx=(5,100), pady=5)
        
        self.raiz.mainloop()
        
    def showCollection(self):
        self.tinfo.delete(1.0,END)
        self.tinfo.tag_configure("center",justify='center')
        self.tinfo.insert("1.0", 'culo')
        self.tinfo.tag_add("center","1.0","end")
# Define la función main() que es en realidad la que indica 
# el comienzo del programa. Dentro de ella se crea el objeto 
# aplicación 'mi_app' basado en la clase 'Aplicación':

def main():
    mi_app = Aplicacion()
    return 0

# Mediante el atributo __name__ tenemos acceso al nombre de un
# un módulo. Python utiliza este atributo cuando se ejecuta
# un programa para conocer si el módulo es ejecutado de forma
# independiente (en ese caso __name__ = '__main__') o es 
# importado:

if __name__ == '__main__':
    main()
