import json
import kivy
import pymysql
from kivy.uix.screenmanager import Screen
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from ColorLabel import ColorLabel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
kivy.require("1.9.1")

class menu(Screen):
    ban=False
    lista=[]
    def iniciarBD(self):
        print("iniciando base de datos")  ##iciar y crear tablas
        Conf = None
        with open("accesoJson.json") as jsonfile:
            Conf = json.load(jsonfile)
        self.connection = pymysql.connect(
            host=Conf['HOST'], user=Conf['DBUSER'],
            password=Conf['DBPASS'], database=Conf['DBNAME'],
            charset='utf8mb4', port=Conf['PORT'])
        if self.connection:
            print("conexion realizada")
            self.instruccionesSQL()


    def instruccionesSQL(self):
        print("entrando a decidir")
        SQL = []
        self.MiCursor = self.connection.cursor()
        self.MiCursor.execute("show tables")
        resultado = self.MiCursor.fetchall()
        for i in range(0, len(resultado), 1):
            print(resultado[i][0])
            if resultado[i][0] == "Puntuacion" or resultado[i][0]=="puntuacion":
                self.ban = True
                break
        print(self.ban)
        if self.ban==False:
            abc = """create table if not exists Puntuacion(Rank smallint(2)  unsigned primary KEY auto_increment,
                                                Nombre varchar(5) not null,
                                                Tiempo SMALLINT(3) unsigned not null,
                                                leftTries tinyint(2) unsigned not null)engine=InnoDB;"""
            SQL.append(abc)
            for i in range(0, 10, 1):
                abc = "INSERT INTO Puntuacion VALUES(NULL,'-----',999,0);"
                SQL.append(abc)
            for i in range(0, len(SQL), 1):
                print(SQL[i])
                self.MiCursor.execute(SQL[i])
        self.connection.commit()
        self.MiCursor.execute("Select * from Puntuacion")
        resultado = self.MiCursor.fetchall()
        for i in range(0, 10, 1):
            self.lista.append([resultado[i][0], resultado[i][1], resultado[i][2],resultado[i][3]] )


    def nuevoJuego(self, obj): ####metodo boton nuevo juego
        self.SM.current = "Pantalla Game"

    def verRecords(self, obj): ####metodo boton records
        c = canvas.Canvas("FT_Score.pdf", pagesize=letter)
        if self.lista:
            resta=572-40
            c.line(40, 720, 572, 720)
            a = 720
            for i in range(-1, 10, 1):
                if i == -1:
                    b = a
                    a = a - 40
                    c.line(40, a, 572, a)  # linea inferior
                    c.line(40, b, 40, a)  # primer linea vertical
                    c.drawCentredString(93, a + 5, "Rank")
                    c.line(40+resta*0.25, b, 40+resta*0.25, a)  # Primer campo
                    c.drawCentredString(219.125, a + 5, "Nombre")
                    c.line(40+resta*0.5, b, 40+resta*0.5, a)  # Primer campo
                    c.drawCentredString(365.375, a + 5, "Tiempo")
                    c.line(40+resta*0.75, b, 40+resta*0.75, a)  ##segndo campo
                    c.drawCentredString(505.25, a + 5, "leftTries")
                    c.line(572, b, 572, a)
                else:
                    b = a
                    a = a - 40
                    c.line(40, a, 572, a)  # linea inferior
                    c.line(40, b, 40, a)  # primer linea vertical
                    c.drawCentredString(93, a + 5, str(self.lista[i][0]))
                    c.line(40+resta*0.25, b, 40+resta*0.25, a)  # Primer campo
                    c.drawCentredString(219.125, a + 5, str(self.lista[i][1]))
                    c.line(40+resta*0.5, b, 40+resta*0.5, a)  # Primer campo
                    c.drawCentredString(365.375, a + 5, str(self.lista[i][2]))
                    c.line(40+resta*0.75, b, 40+resta*0.75, a)  ##segndo campo
                    c.drawCentredString(505.25, a + 5, str(self.lista[i][3]))
                    c.line(572, b, 572, a)
        else:
            c.line(40, 660, 572, 660)
            c.drawCentredString(306, 661, "NO SE HAN ENCONTRADO RESULTADOS")
        c.showPage()
        c.save()


    def build(self, SM=None, DC=None):
        self.SM = SM
        self.DC = DC
        self.iniciarBD()
        box=BoxLayout(orientation="vertical")
        Titulo=ColorLabel(text="Treasure Finder")
        Titulo.background_color=[0.7,0.7,0.7,1]
        Titulo.font_size=25
        box.add_widget(Titulo)
        buttonNG=Button(text="Nuevo Juego")
        box.add_widget(buttonNG)
        buttonNG.bind(on_press=self.nuevoJuego)
        buttonPDF=Button(text="Generar PDF puntuacion")
        box.add_widget(buttonPDF)
        buttonPDF.bind(on_press=self.verRecords)
        self.add_widget(box)
        return self

if __name__ == '__main__':
    pass