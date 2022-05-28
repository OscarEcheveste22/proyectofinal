import json

import kivy
import pymysql
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from ColorLabel import ColorLabel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
kivy.require("1.9.1")
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

class victoria(Screen):
    lista=[]
    banderaDC=0
    leftTries=0

    def Callback_Clock(self, dt):
            self.puntaje.text="your score is: "+str(self.DC.segundos)

    def iniciarBD(self):
        print("iniciando base de datos victoria")  ##iciar y crear tablas
        Conf = None
        with open("accesoJson.json") as jsonfile:
            Conf = json.load(jsonfile)
        self.connection = pymysql.connect(
            host=Conf['HOST'], user=Conf['DBUSER'],
            password=Conf['DBPASS'], database=Conf['DBNAME'],
            charset='utf8mb4', port=Conf['PORT'])
        if self.connection:
            print("conexion realizada")



    def extraerRecords(self):
        self.MiCursor = self.connection.cursor()
        self.MiCursor.execute("Select * from Puntuacion")
        resultado=self.MiCursor.fetchall()
        for i in range(0,10,1):
            self.lista.append([resultado[i][0],resultado[i][1],resultado[i][2],resultado[i][3]])
        print(type(self.lista))



    def continuar(self):
        puntero=-1

        for i in range(0, 10, 1):
            if self.DC.segundos < self.lista[i][2]:
                puntero=i
                break
        if puntero!=-1:
            for i in range(9,puntero,-1):
                self.lista[i][2] = self.lista[i - 1][2]
                self.lista[i][2] = self.lista[i - 1][2]
                self.lista[i][2]=self.lista[i-1][2]
            self.lista[puntero][1] = self.a
            self.lista[puntero][2] = self.DC.segundos
            self.lista[puntero][3] = self.DC.intentos
        instrucciones=[]
        for i in range(0,10,1):
            sql="UPDATE Puntuacion SET nombre=%s, tiempo=%s, leftTries=%s WHERE Rank=%s;"
            self.MiCursor.execute(sql, [self.lista[i][1],self.lista[i][2],self.lista[i][3], self.lista[i][0]])
        self.connection.commit()
        App.get_running_app().stop()
        # removing window
        Window.close()



    def acortarTexto(self, obj):
        self.a = None
        self.a = self.cajaNombre.text
        print(self.a)
        if 0 < len(self.a) <= 5:
                self.DC.nombre=self.a
                self.cajaNombre.text = ""
                self.continuar()
                ##################33aqui pasara a la 3 pantallas
        else:
            self.cajaNombre.text = ""
            self.cajaNombre.hint_text = 'ingresa una cadena de 5 caracteres o menos (no se aceptan cadenas vacias)'

    def build(self, SM=None, DC=None):
        Clock.schedule_interval(self.Callback_Clock, 1)
        self.iniciarBD()
        self.extraerRecords()
        self.SM = SM
        self.DC = DC
        box=BoxLayout(orientation="vertical")
        lineaSuperior=BoxLayout(orientation="horizontal")
        self.cajaNombre=TextInput(text="")
        self.cajaNombre.hint_text='ingresa una cadena de 5 caracteres o menos (no se aceptan cadenas vacias)'
        lineaSuperior.add_widget(self.cajaNombre)
        buttonSave=Button(text="Save")
        buttonSave.bind(on_press=self.acortarTexto)
        lineaSuperior.add_widget(buttonSave)
        lineaInferior=BoxLayout(orientation="vertical")
        congrats=ColorLabel(text="Winner")
        congrats.background_color=[1,0.72,0,1]
        self.puntaje=ColorLabel(text="your score is: "+str(self.DC.segundos))
        self.puntaje.background_color=[1,0.72,0,1]
        lineaInferior.add_widget(congrats)
        lineaInferior.add_widget(self.puntaje)
        box.add_widget(lineaSuperior)
        box.add_widget(lineaInferior)
        self.add_widget(box)
        return self

if __name__ == '__main__':
    pass