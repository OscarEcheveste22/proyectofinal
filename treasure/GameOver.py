import kivy
from kivy.app import App
from kivy.uix.screenmanager import Screen
from ColorLabel import ColorLabel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
kivy.require("1.9.1")
from kivy.core.window import Window

class gameOver(Screen):

    def continuar(self, obj):
        App.get_running_app().stop()
        # removing window
        Window.close()


    def build(self, SM=None, DC=None):
        self.SM = SM
        self.DC = DC
        box=BoxLayout(orientation="vertical")
        lbl1=ColorLabel(text="")
        lbl1.background_color[3]=0
        lblgameover=ColorLabel(text="YOU LOST :'(")
        lblgameover.background_color=[0,0.12,0.53,1]
        lblgameover.font_size=30
        btnCont=Button(text="Salir")
        btnCont.bind(on_press=self.continuar)
        box.add_widget(lbl1)
        box.add_widget(lblgameover)
        box.add_widget(btnCont)
        self.add_widget(box)
        return self

if __name__ == '__main__':
    pass