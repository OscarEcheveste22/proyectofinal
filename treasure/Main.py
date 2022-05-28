import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from DatosCompartidos import DatosCompartidos
from Menu import menu
from Game import pantallaJuego
from GameOver import gameOver
from Victoria import victoria

class Principal(App):
    def build(self):
        mPantalla=ScreenManager()
        DcCompa=DatosCompartidos()
        p1=menu(name="Pantalla Menu").build(SM=mPantalla, DC=DcCompa)
        p2 = pantallaJuego(name="Pantalla Game").build(SM=mPantalla, DC=DcCompa)
        p3 = gameOver(name="Game Over").build(SM=mPantalla, DC=DcCompa)
        p4 = victoria(name="Winner").build(SM=mPantalla, DC=DcCompa)
        mPantalla.add_widget(p1)
        mPantalla.add_widget(p2)
        mPantalla.add_widget(p3)
        mPantalla.add_widget(p4)
        mPantalla.current="Pantalla Menu"
        return mPantalla

if __name__=='__main__':
    miapp=Principal()
    miapp.run()