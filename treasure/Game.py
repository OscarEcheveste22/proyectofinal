import kivy
from kivy.uix.screenmanager import Screen
from ColorLabel import ColorLabel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
kivy.require("1.9.1")
import random
from kivy.clock import Clock
#from DatosCompartidos import DatosCompartidos

class pantallaJuego(Screen):
    segundos=0
    tesoro=0
    jugando = True
    intentos=0
    ganador=False
    inicio=0

    def buscarTesoro(self, obj):
        self.inicio=1
        if obj.key==self.tesoro:
            obj.background_color=[1,0,0,1]
            obj.backdround_normal=""
            obj.disabled=True
            self.ganador=True
        else:
            obj.background_color = [1, 0, 0, 1]
            obj.backdround_normal = ""
            obj.disabled = True
            self.intentos=self.intentos-1
            self.lblintentos.text = str(self.intentos)

    def perder(self):
        if self.intentos==0:
            self.SM.current = "Game Over"




    def Callback_Clock(self, dt):
        self.perder()
        if self.jugando==True and self.ganador==False and self.SM.current=="Pantalla Game" and self.inicio==1:
            self.segundos = self.segundos + 1
            self.cronometro.text = "tiempo: % d..." % self.segundos
        if self.ganador==True:
            self.DC.segundos=self.segundos
            self.DC.intentos=self.intentos
            self.ganador=False
            self.inicio=0
            self.ganar()


    def ganar(self):
        self.SM.current = "Winner"

    def build(self, SM=None, DC=None):
        self.SM = SM
        self.DC = DC
        a=[]
        tablero=[]
        lineas=random.randint(1,8)
        columnas=random.randint(1,8)
        self.tesoro=random.randint(1,(lineas*columnas))
        print(self.tesoro)
        contador=0
        x=(lineas*columnas)*0.4
        self.intentos= int(x)
        for i in range(0,columnas,1):
            a.append(None)
        for i in range(0,lineas,1):
            tablero.append(a)
        principal=GridLayout(rows=1,cols=2)
        colIzq=GridLayout(rows=lineas, cols=columnas)
        for i in range(0,lineas,1):
            for j in range(0,columnas,1):
                contador+=1
                tablero[i][j] = Button(text="")
                tablero[i][j].background_color = [0.8,0.8,0.8,1]
                tablero[i][j].key = contador
                tablero[i][j].bind(on_press=self.buscarTesoro)
                colIzq.add_widget(tablero[i][j])
        colDerecha=BoxLayout(orientation="vertical", size_hint_x=None, width=200)
        cajita=BoxLayout(orientation="vertical",size_hint_y=None, height=200)
        self.cronometro=ColorLabel(text="0")
        self.lblintentos = ColorLabel(text="intentos restantes"+str(self.intentos))
        cajita.add_widget(self.cronometro)
        cajita.add_widget(self.lblintentos)
        lblnegra=ColorLabel(text="")
        lblnegra.background_color=[0,0,0,0]
        colDerecha.add_widget(cajita)
        colDerecha.add_widget(lblnegra)
        principal.add_widget(colIzq)
        principal.add_widget(colDerecha)
        Clock.schedule_interval(self.Callback_Clock, 1)
        self.add_widget(principal)
        return self

if __name__ == '__main__':
    pass