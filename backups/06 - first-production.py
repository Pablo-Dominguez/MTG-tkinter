#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import messagebox
from tkinter import ttk 
from PIL import ImageTk, Image
from screeninfo import get_monitors
import tkinter.tix as tix
import os
import pandas as pd
from fuzzywuzzy import fuzz
import requests
from io import BytesIO
import json


welcome_text = ''' 

                  MTG COLLECTOR MANAGER                  
_________________________________________________________
'''


def get_ratio(row,text):
        name = row['Cardname']
        return fuzz.token_set_ratio(name, text)

def combine_funcs(*funcs):
        def combined_func(*args, **kwargs):
            for f in funcs:
                f(*args, **kwargs)
        return combined_func

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
        
        self.exit_button = ttk.Button(self.top, text='Salir',compound="top", command=combine_funcs(self.top.destroy,self.saveChanges),image = self.exit_icon).place(x=int(self.width*0.8), y=int(self.height*0.8))
        
        self.collection_button = ttk.Button(self.top, text='My collections',compound="top", command=combine_funcs(self.showCollections,self.destroyButtons,self.saveChanges),image = self.collection_icon)
        
        self.collection_button.place(x=int(self.width*0.15), y=int(self.height*0.8))
        
        
        
        self.newc_button = ttk.Button(self.top, text='New list',compound="top", command=self.createCollection,image = self.newc_icon)
        
        self.newc_button.place(x=int(self.width*0.15), y=int(self.height*0.65))

        self.canvas.new_text = None
        self.canvas.text_window = None
        self.canvas.card_text = None
        self.canvas.card_output = None
        self.canvas.card_output_01 = None
        self.panel = None
        self.up_card = None
        self.red_card = None
        self.canvas.button1 = None
        self.row_df = None
        self.error = False
        
        self.top.mainloop()
    
    def createCollection(self):
        self.saveChanges()
        self.destroyElems()
        self.destroyButtons()
        self.canvas.create_image(-self.width*0.25, 0, image=self.bg, anchor="nw")
        
        if not self.error:
        
            text = chr(10)+'Type a collection name and double press enter to create it:'+chr(10)
            self.canvas.new_text = self.canvas.create_text(0,self.height*0.1, text=text, fill="white", anchor='nw',font = "Helvetica 16 bold",justify='left',tag='new_coll')
        
        else: 
        
            text = chr(10)+'Error creating collection. Maybe it already exists?'+chr(10)
            self.new_text = self.canvas.create_text(0,self.height*0.1, text=text, fill="white", anchor='nw',font = "Helvetica 16 bold",justify='left',tag='new_coll')
        
        
        x1,y1,x2,self.y2_newc = self.canvas.bbox('new_coll')
            
        self.entry = Entry(self.canvas,justify='right',width=25)
        self.canvas.text_window = self.canvas.create_window((0,self.y2_newc),window=self.entry,width=500)
        self.entry.bind('<Return>',self.createCollAux)
    
    def createCollAux(self,event):
      
        self.action = 'CREATING'
        collection_text = self.entry.get()
        try:
            os.mkdir('collections/'+collection_text)
            df_output = pd.DataFrame(columns = ['Cardname','Times_owned'])
            df_output.to_csv('collections/'+collection_text+'/'+collection_text+'.csv',sep=';',index=False)
            #self.entry.delete(0, 'end')
            self.entry.bind('<Return>',self.editCollection)
        except:
            self.entry.delete(0, 'end')
            
            if self.canvas.new_text is not None:
                self.canvas.delete(self.canvas.new_text)
            
            self.error = True
            self.createCollection()
        
        #self.editCollection()
    
    
    
    def showCollections(self):
        # Reset content
        self.destroyElems()
        self.destroyButtons()
        
        self.canvas.create_image(-self.width*0.25, 0, image=self.bg, anchor="nw")

        text = '''
        YOUR COLLECTIONS
        _________________________________________________________
        '''
        collections = os.listdir('collections')
        if collections == []:
            text_to_add = "Sorry, you have no collections yet. Please create one"
            text = text+chr(10)+text_to_add +chr(10)
            self.new_text = self.canvas.create_text(0,self.height*0.1, text=text, fill="white", anchor='nw',font = "Helvetica 16 bold",justify='left',tag='new_text')
        else:
            for folder in os.listdir('collections'):
                text_to_add = "---> {}".format(folder)
                text = text+chr(10)+text_to_add +chr(10)
        
            text = text + chr(10)+'Type a collection name to edit and press enter'+chr(10)
            self.new_text = self.canvas.create_text(0,self.height*0.1, text=text, fill="white", anchor='nw',font = "Helvetica 16 bold",justify='left',tag='new_text')
            x1,y1,x2,y2 = self.canvas.bbox('new_text')
            
            self.entry = Entry(self.canvas,justify='right',width=25)
            self.canvas.text_window = self.canvas.create_window((0,y2),window=self.entry,width=500)
            self.action = 'EDITING'
            self.entry.bind('<Return>',self.editCollection)
    
    def editCollection(self,event):
        # Reset content
        self.destroyElems()
        self.destroyButtons()
         
        self.canvas.create_image(-self.width*0.25, 0, image=self.bg, anchor="nw")
        
        collections = os.listdir('collections')
        collections_full = collections+[coll.lower() for coll in collections]+[coll.upper() for coll in collections]
        collection_text = self.entry.get()
        text = ''
        if collection_text in collections_full:
            self.canvas.delete(self.canvas.text_window)
            self.collection_name = [coll for coll in collections_full if coll == collection_text][0]
            text = '''
        {} {}
        _________________________________________________________
        '''.format(self.action,self.collection_name) +chr(10)
            text = text+'Enter a card name:'+chr(10)
            self.canvas.coll_text = self.canvas.create_text(0,self.height*0.1, text=text, fill="white", anchor='nw',font = "Helvetica 16 bold",justify='left',tag='coll_text')
            x1,y1,x2,self.y2 = self.canvas.bbox('coll_text')
            
            self.card_entry = Entry(self.canvas,justify='right',width=25)
            self.canvas.card_text = self.canvas.create_window((0,self.y2),window=self.card_entry,width=500)
            self.card_entry.bind('<Return>',self.addCards)
        else:
            text = '''
            Sorry, wrong collection name. Please try again.'''+chr(10)
            for coll in collections:
                text_to_add = "---> {}".format(coll)
                text = text+chr(10)+text_to_add +chr(10)
                
            self.canvas.create_text(0,self.height*0.1, text=text, fill="white", anchor='nw',font = "Helvetica 16 bold",justify='left',tag='new_text')
        
        
    
    def addCards(self,event):
        self.saveChanges()
        
        self.collection_df = pd.read_csv('./collections/'+self.collection_name+'/'+self.collection_name+'.csv',sep=';')
        
        card_text = self.card_entry.get()
        
        # Reset elements
        if self.panel is not None:
            self.panel.destroy() 
        self.card_entry.delete(0, 'end')
        if self.canvas.card_output is not None:
            self.canvas.delete(self.canvas.card_output)
        if self.canvas.card_output_01 is not None:
            self.canvas.delete(self.canvas.card_output_01)
        self.destroyButtons()
        
        self.collection_df_search = self.collection_df[self.collection_df.apply(get_ratio,text = card_text, axis=1) > 90]
        condition = self.collection_df_search.shape[0]
        if condition > 0:
            self.cardname = self.collection_df_search['Cardname'].iloc(0)[0]
            self.times_owned = self.collection_df_search['Times_owned'].iloc(0)[0]
            text = f'Cardname: {self.cardname} '+' \t ' + f' Times owned: {self.times_owned}'
            self.lv_y = self.card_entry.winfo_rooty()
            self.canvas.card_output = self.canvas.create_text(0,self.lv_y, text=text, fill="white", anchor='nw',font = "Helvetica 16 bold",justify='left')
            
            
            url = 'https://api.scryfall.com/cards/named?fuzzy='
            card_to_search = card_text.lower().replace('\'','').replace(' ','+')
            url_to_search = url+card_to_search
            response = requests.get(url_to_search)
            result = json.loads(response.text)
            image_url = result['image_uris']['normal']
            response = requests.get(image_url)
            
            
            self.card_img = Image.open(BytesIO(response.content))
            self.card_image = ImageTk.PhotoImage(self.card_img.resize((int(self.width*0.25),int(self.height*0.6))))
            
            
            self.panel = Label(self.top, image=self.card_image)
            self.panel.image = self.card_image
            #self.panel.place(relheight=.095,relwidth=0.25,relx=0.7,rely=0.03)
            self.panel.place(x=self.width*0.25, y=self.lv_y+28, relwidth=0.25, relheight=0.6)
            
            
            self.add_img = Image.open("./pics/plus_mtg.png")
            icon_width, icon_height = self.add_img.size
            self.add_icon = ImageTk.PhotoImage(self.add_img.resize((int(icon_width*0.1),int(icon_height*0.1))))
            
            self.up_card = ttk.Button(self.top, text='Add',compound="top", command=self.upCard,image = self.add_icon)
            self.up_card.place(x=self.width*0.65, y=self.lv_y+55)
            
            self.red_img = Image.open("./pics/less_mtg.png")
            icon_width, icon_height = self.red_img.size
            self.red_icon = ImageTk.PhotoImage(self.red_img.resize((int(icon_width*0.1),int(icon_height*0.1))))
            
            self.red_card = ttk.Button(self.top, text='Reduce',compound="top", command=self.downCard,image = self.red_icon)
            
            self.red_card.place(x=self.width*0.55, y=self.lv_y+55)
            
            

            
        else:
            
            
            url = 'https://api.scryfall.com/cards/named?fuzzy='
            card_to_search = card_text.lower().replace('\'','').replace(' ','+')
            url_to_search = url+card_to_search
            response = requests.get(url_to_search)
            result = json.loads(response.text)
            image_url = result['image_uris']['normal']
            response = requests.get(image_url)
            
            self.cardname = result['name']
            text = f'{self.cardname} is not in your collection.'
            self.lv_y = self.card_entry.winfo_rooty()
            self.canvas.card_output = self.canvas.create_text(0,self.lv_y, text=text, fill="white", anchor='nw',font = "Helvetica 16 bold",justify='left')
            
            text = 'Do you want to add it?'
            self.lv_y = self.card_entry.winfo_rooty()
            self.canvas.card_output_01 = self.canvas.create_text(int(self.width*0.28),self.lv_y+28, text=text, fill="white", anchor='nw',font = "Helvetica 16 bold",justify='left')
            
            self.card_img = Image.open(BytesIO(response.content))
            self.card_image = ImageTk.PhotoImage(self.card_img.resize((int(self.width*0.25),int(self.height*0.6))))
            
            
            self.panel = Label(self.top, image=self.card_image)
            self.panel.image = self.card_image
            #self.panel.place(relheight=.095,relwidth=0.25,relx=0.7,rely=0.03)
            self.panel.place(x=self.width*0.25, y=self.lv_y+28, relwidth=0.25, relheight=0.6)
            
            
            self.add_img = Image.open("./pics/plus_mtg.png")
            icon_width, icon_height = self.add_img.size
            self.add_icon = ImageTk.PhotoImage(self.add_img.resize((int(icon_width*0.1),int(icon_height*0.1))))
            
            self.up_card = ttk.Button(self.top, text='Add',compound="top", command=self.upNewCard,image = self.add_icon)
            self.up_card.place(x=self.width*0.65, y=self.lv_y+55)
            
    def upNewCard(self):

        try:
            self.red_card.place_forget()
        except:
            pass
        
        try:
            self.canvas.delete(self.canvas.card_output_01)
        except:
            pass
        
        if self.row_df is None:
            a_row = [(self.cardname, 1)]
            #df = pd.DataFrame([[3, 4], [5, 6]])
            self.row_df = pd.DataFrame(a_row, columns=['Cardname','Times_owned'])
            #self.collection_df = pd.concat([self.collection_df, row_df], ignore_index=True)
            #self.collection_df.to_csv('./collections/'+self.collection_name+'/'+self.collection_name+'.csv',sep=';',index=False)
        else:
            self.rownumber = self.row_df[self.row_df['Cardname']==self.cardname].index[0]
            self.row_df.at[self.rownumber,'Times_owned'] = self.times_owned + 1
            
        
        self.cardname = self.row_df['Cardname'].iloc(0)[0]
        self.times_owned = self.row_df['Times_owned'].iloc(0)[0]
        
        text = f'Adding card {self.times_owned} times.'
        self.lv_y = self.card_entry.winfo_rooty()
        self.canvas.card_output_01 = self.canvas.create_text(int(self.width*0.28),self.lv_y+28, text=text, fill="white", anchor='nw',font = "Helvetica 16 bold",justify='left')
        
        self.red_img = Image.open("./pics/less_mtg.png")
        icon_width, icon_height = self.red_img.size
        self.red_icon = ImageTk.PhotoImage(self.red_img.resize((int(icon_width*0.1),int(icon_height*0.1))))
        
        self.red_card = ttk.Button(self.top, text='Reduce',compound="top", command=self.downNewCard,image = self.red_icon)
        
        self.red_card.place(x=self.width*0.55, y=self.lv_y+55)
    
    def downNewCard(self):
        
        try:
            self.canvas.delete(self.canvas.card_output_01)
        except:
            pass
        
        self.rownumber = self.row_df[self.row_df['Cardname']==self.cardname].index[0]
        self.row_df.at[self.rownumber,'Times_owned'] = self.times_owned - 1
        
        self.times_owned = self.times_owned - 1
        
        text = f'Adding card {self.times_owned} times.'
        self.lv_y = self.card_entry.winfo_rooty()
        self.canvas.card_output_01 = self.canvas.create_text(int(self.width*0.28),self.lv_y+28, text=text, fill="white", anchor='nw',font = "Helvetica 16 bold",justify='left')
        
        if self.times_owned <= 0:
            self.times_owned = 0
            self.destroyButtons()

            self.panel.destroy()
            self.canvas.delete(self.canvas.card_output)
            self.canvas.delete(self.canvas.card_output_01)
            
            self.row_df = None
        
    def downCard(self):
        self.rownumber = self.collection_df[self.collection_df['Cardname']==self.cardname].index[0]
        self.collection_df.at[self.rownumber,'Times_owned'] = self.times_owned - 1
        
        self.times_owned = self.times_owned - 1
        text = f'Cardname: {self.cardname} '+' \t ' + f' Times owned: {self.times_owned}'
        
        if self.times_owned > 0:
            self.lv_y = self.card_entry.winfo_rooty()
            self.canvas.delete(self.canvas.card_output)
            self.canvas.card_output = self.canvas.create_text(0,self.lv_y, text=text, fill="white", anchor='nw',font = "Helvetica 16 bold",justify='left')
            self.collection_df.to_csv('./collections/'+self.collection_name+'/'+self.collection_name+'.csv',sep=';',index=False)
            
        else:
            self.collection_df.drop(axis=0,index=self.rownumber,inplace=True)
            self.destroyButtons()
            #self.up_card.destroy()
            #self.red_card.destroy()
            self.panel.destroy()
            self.canvas.delete(self.canvas.card_output)
            self.collection_df.to_csv('./collections/'+self.collection_name+'/'+self.collection_name+'.csv',sep=';',index=False)
            
    def destroyButtons(self):
        try:
            self.up_card.place_forget()
        except:
            pass
        try:
            self.red_card.place(x=self.width, y=self.lv_y)
        except:
            pass
            
        
    def upCard(self):
        self.rownumber = self.collection_df[self.collection_df['Cardname']==self.cardname].index[0]
        self.collection_df.at[self.rownumber,'Times_owned'] = self.times_owned + 1
        
        self.times_owned = self.times_owned + 1
        text = f'Cardname: {self.cardname} '+' \t ' + f' Times owned: {self.times_owned}'
        self.lv_y = self.card_entry.winfo_rooty()
        self.canvas.delete(self.canvas.card_output)
        self.canvas.card_output = self.canvas.create_text(0,self.lv_y, text=text, fill="white", anchor='nw',font = "Helvetica 16 bold",justify='left')
        self.collection_df.to_csv('./collections/'+self.collection_name+'/'+self.collection_name+'.csv',sep=';',index=False)
    
    def destroyElems(self):
        
        if self.canvas.text_window is not None: 
            self.canvas.delete(self.canvas.text_window)
        
        if self.canvas.new_text is not None:
            self.canvas.delete(self.canvas.new_text)
            
        if self.canvas.card_text is not None:
            self.canvas.delete(self.canvas.card_text)
            
        if self.canvas.card_output is not None:
            self.canvas.delete(self.canvas.card_output)
            
        if self.canvas.card_output_01 is not None:
            self.canvas.delete(self.canvas.card_output_01)
            
        if self.panel is not None:
            self.panel.destroy()
            
    def saveChanges(self):
        if self.row_df is not None:
            self.collection_df = pd.concat([self.collection_df, self.row_df], ignore_index=True)
            self.collection_df.to_csv('./collections/'+self.collection_name+'/'+self.collection_name+'.csv',sep=';',index=False)
            self.row_df = None
        else:
            pass
    
    
    
def main():
    mi_app = Aplicacion()
    return 0

if __name__ == '__main__':
    main()
