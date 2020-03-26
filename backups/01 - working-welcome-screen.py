#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import messagebox
from tkinter import ttk 
from PIL import ImageTk, Image
from screeninfo import get_monitors
import tkinter.tix as tix
import os


welcome_text = ''' 

                  MTG COLLECTOR MANAGER                  
_________________________________________________________
'''




class Aplicacion():
    def __init__(self):
        
        # Window
        self.top = Tk()
        self.top.title('My MTG collection app')
        self.top.resizable(False, False)

        self.width = get_monitors()[0].width
        self.height = int(get_monitors()[0].height*0.92)
        self.top.geometry('{}x{}'.format(self.width,self.height))

        # Backgroud image
        self.img = Image.open("./pics/mtg-triple.png")
        self.img_copy = self.img.copy()
        
        self.bg = ImageTk.PhotoImage(self.img.resize((self.width,self.height)))

        
        self.background_label = Label(self.top, image=self.bg)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.canvas = Canvas(self.top, width=self.width*0.5, height=self.height*0.5,highlightthickness=0)
        
        
        self.canvas.image = self.bg
        
        self.canvas.pack()
        
        # Welcome text
        self.canvas.create_image(-self.width*0.25, 0, image=self.bg, anchor="nw")
        self.main_text = self.canvas.create_text(0,self.height*0.15, text=welcome_text, fill="white", anchor='nw',font = "Helvetica 16 bold",justify='center')
        
        # Buttons imgs
        self.exit_img = Image.open("./pics/exit.png")
        icon_width, icon_height = self.exit_img.size
        self.exit_icon = ImageTk.PhotoImage(self.exit_img.resize((int(icon_width*0.5),int(icon_height*0.5))))
        
        self.collection_img = Image.open("./pics/collection.png")
        icon_width, icon_height = self.collection_img.size
        self.collection_icon = ImageTk.PhotoImage(self.collection_img.resize((int(icon_width*0.5),int(icon_height*0.5))))
        
        self.newc_img = Image.open("./pics/new_collection.png")
        icon_width, icon_height = self.newc_img.size
        self.newc_icon = ImageTk.PhotoImage(self.newc_img.resize((int(icon_width*0.5),int(icon_height*0.5))))
        
        # Buttons
        
        self.exit_button = ttk.Button(self.top, text='Salir',compound="top", command=self.top.destroy,image = self.exit_icon).place(x=int(self.width*0.8), y=int(self.height*0.8))
        
        self.collection_button = ttk.Button(self.top, text='My collection',compound="top", command=self.showCollection,image = self.collection_icon).place(x=int(self.width*0.15), y=int(self.height*0.8))
        
        self.newc_button = ttk.Button(self.top, text='New list',compound="top", command=self.top.destroy,image = self.newc_icon).place(x=int(self.width*0.15), y=int(self.height*0.65))
        
        
        self.top.mainloop()
    
    def showCollection(self):
        # Reset content
        self.canvas.create_image(-self.width*0.25, 0, image=self.bg, anchor="nw")
        text = '''
        YOUR COLLECTIONS
        _________________________________________________________
        '''
        self.canvas.create_text(0,self.height*0.1, text=text, fill="white", anchor='nw',font = "Helvetica 16 bold",justify='left')
        
    
def main():
    mi_app = Aplicacion()
    return 0

if __name__ == '__main__':
    main()
