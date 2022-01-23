# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 15:17:02 2022

@author: mizo_
"""

import numpy as np
import pandas as pd
from myclasses import MyLabel

from kivy.app import App
from kivymd.uix.screen import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.uix.widget import Widget
from kivy.uix.button import Button

from kivy.properties import ListProperty, StringProperty
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput

#from kivymd.app import MDApp
# from kivymd.uix.textfield import MDTextField
# from kivy.lang import Builder


class Chooser2(TextInput):
    choicesfile = StringProperty()
    choiceslist = ListProperty([])

    def __init__(self, **kwargs):
        self.choicesfile = kwargs.pop('choicesfile', '')  # each line of file is one possible choice
        self.choiceslist = kwargs.pop('choiceslist', [])  # list of choices
        super(Chooser2, self).__init__(**kwargs)
        self.size_hint= (1,.1)
        self.multiline = False
        self.halign = 'left'
        self.bind(choicesfile=self.load_choices)
        self.bind(text=self.on_text)
        self.load_choices()
        self.dropdown = None
        # self.btn = Button(text="Open")
        # self.add_widget(self.btn)

    def open_dropdown(self, *args):
        print(f"dropdown is '{self.dropdown}'")
        if self.dropdown:
            self.dropdown.open(self)
            print(f"dropdown is '{self.dropdown}'")


    def load_choices(self):
        #print(f"choicesfile is '{self.choicesfile}'" )
        if self.choicesfile:
            with open(self.choicesfile) as fd:
                for line in fd:
                    print(f"inside cf {line}")
                    self.choiceslist.append(line.strip('\n'))
        self.values = []

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if self.suggestion_text and keycode[0] == ord('\r'):  # enter selects current suggestion
            self.suggestion_text = ' '  # setting suggestion_text to '' screws everything
            #print(f"self.values = {self.values}")
            self.text = self.values[0]
            if self.dropdown:
                self.dropdown.dismiss()
                #self.dropdown = None
        else:
            super(Chooser2, self).keyboard_on_key_down(window, keycode, text, modifiers)


    def on_text(self, chooser, text):
        #print(f"on_text = {text, chooser}")
        if self.dropdown:
            self.dropdown.dismiss()
            #self.dropdown = None
        if text == '':
            return
        values = []
        for choice in self.choiceslist:
            #print(f"on_text choice = {choice}")
            if text in choice:
                #print(f"{text} is in {choice}")
                values.append(choice)

        self.values = values
        
        if len(values) > 0:
            self.dropdown = DropDown()
            for val in self.values:
                self.dropdown.add_widget(Button(text=val, size_hint_y=None, height=100, on_release=self.do_choose))
            self.dropdown.open(self)


    def do_choose(self, butt):
        self.text = butt.text
        #print(self.text)
        if self.dropdown:
            self.dropdown.dismiss()
            #self.dropdown = None
            
    def clear_data(self):
            self.text=''
            choicesfile = StringProperty()
            choiceslist = ListProperty([])
            self.values = []
            self.dropdown = None
            self.load_choices()


class Chooser(TextInput):
    choicesfile = StringProperty()
    choiceslist = ListProperty([])

    def __init__(self, **kwargs):
        self.choicesfile = kwargs.pop('choicesfile', '')  # each line of file is one possible choice
        self.choiceslist = kwargs.pop('choiceslist', [])  # list of choices
        super(Chooser, self).__init__(**kwargs)
        
        self.size_hint= (1,1)
        
        self.multiline = False
        self.halign = 'left'
        self.bind(choicesfile=self.load_choices)
        self.bind(text=self.on_text)
        self.load_choices()
        self.dropdown = None

    def open_dropdown(self, *args):
        if self.dropdown:
            self.dropdown.open(self)

    def load_choices(self):
        if self.choicesfile:
            with open(self.choicesfile) as fd:
                for line in fd:
                    self.choiceslist.append(line.strip('\n'))
        self.values = []
        

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if self.suggestion_text and keycode[0] == ord('\r'):  # enter selects current suggestion
            self.suggestion_text = ' '  # setting suggestion_text to '' screws everything
            self.text = self.values[0]
            if self.dropdown:
                self.dropdown.dismiss()
                self.dropdown = None
        else:
            super(Chooser, self).keyboard_on_key_down(window, keycode, text, modifiers)

    
    def on_text(self, chooser, text):
        if self.dropdown:
            self.dropdown.dismiss()
            self.dropdown = None
        if text == '':
            return
        values = []
        for addr in self.choiceslist:
            if addr.startswith(text):
                values.append(addr)
        self.values = values
        if len(values) > 0:
            if len(self.text) < len(self.values[0]):
                self.suggestion_text = self.values[0][len(self.text):]
            else:
                self.suggestion_text = ' '  # setting suggestion_text to '' screws everything
            self.dropdown = DropDown()
            for val in self.values:
                self.dropdown.add_widget(Button(text=val, size_hint_y=None, height=100, on_release=self.do_choose))
            self.dropdown.open(self)

    def do_choose(self, butt):
        self.text = butt.text
        #print(self.text)
        if self.dropdown:
            self.dropdown.dismiss()
            self.dropdown = None

    def clear_data(self):
            self.text=''
            choicesfile = StringProperty()
            choiceslist = ListProperty([])
            self.values = []
            self.dropdown = None
            self.load_choices()



class MainLayout(BoxLayout):

    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
        self.orientation='vertical'
        
    
        with self.canvas.before:
            Color(0.78, 0.78, 0.78, 1, mode='rgba')
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(size=self.update_rect)
        
        #self.df = pd.read_excel("data2.xlsx", engine='openpyxl')
        
        self.df = pd.read_csv("new_codes.csv")
        
        self.drug_list = []
        self.disease_list = []
        self.selection = []
        self.icd10 = ''
        self.prep_data()
        
        self.title = MyLabel(text=
                            'Welcome to ICD10 finder', 
                            size_hint=(1, 0.18), 
                            font_size= '{}sp'.format(25), 
                            color=[0.25,0.25,0.4,1],
                            valign='middle',
                            halign='center'
                            )
        self.title.col=(.4, 0.7, .85, 1)
        self.add_widget(self.title)
        
        
        
        self.choose_drug = Chooser(choiceslist=self.drug_list, 
                          hint_text='Please enter the drug', 
                          size_hint=(0.5, None), 
                          #height=20, 
                          #pos_hint={'center_x':0.5, 'center_y':0.5}
                          )
        
        self.ids['c_drugs']=self.choose_drug
        
        self.drug_lyt= BoxLayout(size_hint=(1,.06))
        self.drug_lyt.add_widget(self.ids['c_drugs'])
        self.add_widget(self.drug_lyt)
        
        
        self.btn1 = Button(
        text="Show Diseases", 
        size_hint=(1,.12),
        font_size='20sp',
        background_color= (.4, .8,.4,1),
        background_normal='',
        )
        self.ids['btn1']= self.btn1
        self.add_widget(self.ids['btn1'])
        self.ids['btn1'].bind(on_release=self.get_disease_list)
        
        
        self.choose_disease = Chooser2(choiceslist=self.disease_list, 
                          hint_text='Please press SPACE to see suggestions \nor type the diagnosis...', 
                          size_hint=(0.5, None), height=30, 
                          pos_hint={'center_x':0.5, 'center_y':0.5})
        self.ids['c_disease']=self.choose_disease
        self.add_widget(self.ids['c_disease'])
        
        
        self.btn2 = Button(text="Get the ICD10",
        size_hint=(1,.12),
        font_size='20sp',
        background_color= (.2, .4,.8,1),
        background_normal='',
          )
        self.ids['btn2']=self.btn2
        self.add_widget(self.ids['btn2'])
        self.ids['btn2'].bind(on_release=self.get_icd10)
        
        
        
        self.icd10_widget = MyLabel(text=
                            'ICD-10: ', 
                            size_hint=(1, 0.4), 
                            font_size= '{}sp'.format(25), 
                            color=[0.25,0.25,0.4,1],
                            valign='middle',
                            halign='center'
                            )
        self.ids['icd10'] = self.icd10_widget
        self.ids['icd10'].col=(.8, 0.7, .65, 1)
        self.add_widget(self.ids['icd10'])
        
        self.hint_text= "1- Enter the drug name, then press 'Show Diseases' button\n2- Then type the disease name in the Textbox\n3- Select the disease from the dropdown list\n4- Press the 'Get ICD10' button \n5- Please use Clear Button before entering a enter new drug\n6- Please don't use the backspace to clear text fields"
        
        self.hint_box = MyLabel(text=
                            self.hint_text, 
                            size_hint=(1, 0.2), 
                            font_size= '{}sp'.format(14), 
                            color=[0.35,0.35,0.35,1],
                            valign='middle',
                            halign='center'
                            )
        self.ids['hint_box'] = self.hint_box
        self.ids['hint_box'].col=(1, 1, .55, 1)
        self.add_widget(self.ids['hint_box'])
        
        self.btn3 = Button(text="Clear",
        size_hint=(1,.15), color=(.1,.1,.1,1), font_size='20sp',background_color= (.9, .35,.3,1), background_normal='',)
        self.ids['btn3']=self.btn3
        self.add_widget(self.ids['btn3'])
        self.ids['btn3'].bind(on_release=self.clear_data)
        
        
        
    def prep_data (self, *args):
        #self.df.dropna(axis=1, inplace=True)
        #self.df.drop(['Unnamed: 0'], axis='columns', inplace=True)
        self.cols = self.df.columns
        print(self.cols)

        for i in self.cols:
            print(i)
            self.df[i] = self.df[i].str.lower()
        self.drug_list = list(self.df[self.cols[2]].unique())
        
            
    def clear_data(self, *args):
        self.ids['c_disease'].clear_data()
        self.ids['c_drugs'].clear_data()
        self.ids['icd10'].text='ICD-10: '
        
        
    def get_disease_list(self, *args):
        print(self.choose_drug.text)
        self.selection = self.df[(self.df == 
                      self.ids['c_drugs'].text).any(axis=1)]
        #print(self.selection)
        self.disease_list = list(self.selection[self.cols[1]].unique())
        #print(self.disease_list)
        self.ids['c_disease'].choiceslist = self.disease_list
        self.ids['c_disease'].load_choices()
        self.ids['c_disease'].open_dropdown()
        
        
    def get_icd10 (self, *args):
        print(self.ids['c_disease'].text)
        self.icd10 = str(self.selection[
            (self.df==self.ids['c_disease'].text).any(
                axis=1)][self.cols[0]].unique())
        print(self.icd10)
        self.icd10_widget.text = f"ICD10 = {str(self.icd10)}"
    
            
            
    def update_rect(self, *args):
        """FUNCTION TO UPDATE THE RECATANGLE OF CANVAS 
        TO FIT THE WHOLE SCREEN OF MAINSCREEN ALWAYS"""
        self.rect.pos = self.pos
        self.rect.size = self.size
        #print(self.size)

		
class ICD10App(App):
    def build(self):
        return MainLayout()
		
if __name__ == "__main__":
    
    ICD10App().run()
	