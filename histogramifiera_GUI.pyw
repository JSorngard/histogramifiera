#Kodade av Johan Sörngård för Vetenskapens hus.

import tkinter as tk
import os

pathdefault="Sökväg"
massdefault="Maxmassa"
buttondefault="Histogramifiera!"

class inputwindow(tk.Frame):
    """Ett litet fönster som läser in diverse input och lagrar den i variabler."""
    def __init__(self, master=None):
        tk.Frame.__init__(self,master)
        self.dolog = tk.IntVar()
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        #Skapa en knapp som kallar på return_values när den trycks på.
        self.acceptButton = tk.Button(self,text=buttondefault,
            command=self.run_histogramifiera)
        self.acceptButton.grid()
        #Skapa ett textfält för sökvägen
        self.entryfield = tk.Entry()
        self.entryfield.insert(0,pathdefault)
        self.entryfield.grid()
        #Skapa ett textfält för den maximala massan.
        self.massfield = tk.Entry()
        self.massfield.insert(0,massdefault)
        self.massfield.grid()
        self.logcheck = tk.Checkbutton(text="Logplot",variable=self.dolog)
        self.logcheck.grid()

        #Placera fokus i sökvägsfältet.
        self.entryfield.focus_set()

    def return_values(self):
        #Gör dessa variabler globala så att de kan läsas på andra platser i programmet.
        global pathstring
        global massstring
        global dologplot
        #Hämtar innehållet i textfälten och lagrar det i de globala variablerna.
        pathstring = self.entryfield.get()
        massstring = self.massfield.get()
        dologplot = self.dolog.get()
        self.quit()

    def run_histogramifiera(self):
        sokvag=self.entryfield.get()
        maxmassa=self.massfield.get()
        gorlogplot=self.dolog.get()

        #Byt ut \ mot \\ så att de kommer att tolkas korrekt av histogramifiera.pyw.
        sokvag.replace("\\","\\\\")

        #Testa att läsa in maxmassan till en int, funkar det inte anges ingen maxmassa, annars skickas den med "-m".
        if(maxmassa != ""):
            try:
                maxmassa = "-m "+str(int(maxmassa))
            except:
                maxmassa = ""

        #Om en sökväg inte är angiven, skicka nuvarande plats med "-p".
        if(sokvag=="" or sokvag==pathdefault):
            sokvag=os.path.dirname(os.path.realpath(__file__))

        #Om logplot är 1, lägg till "-l" som kommando.
        logstring=""
        if(gorlogplot):
            logstring = " -l"

        os.system("histogramifiera.pyw"+" -p \""+sokvag+"\" "+maxmassa+logstring+">log.txt")


#Startar upp det lilla inputfönstret.
pathwindow=inputwindow()
pathwindow.master.title("Ange alternativ.")
pathwindow.mainloop()
'''
#När vi kommit hit är fönstret dött och vi fortsätter som en vanlig scipt.

#Byt ut \ mot \\ så att de kommer att tolkas korrekt av histogramifiera.pyw.
try:
    pathstring.replace("\\","\\\\")
except:
    #pathstring är inte definierad, alltså har användargränssnittet kryssats bort. Säkert att stänga av.
    exit()

#Testa att läsa in maxmassan till en int, funkar det inte anges ingen maxmassa, annars skickas den med "-m".
if(massstring != ""):
    try:
        massstring = "-m "+str(int(massstring))
    except:
        massstring = ""

#Om en sökväg inte är angiven, skicka nuvarande plats med "-p".
if(pathstring=="" or pathstring==pathdefault):
    pathstring=os.path.dirname(os.path.realpath(__file__))

#Om logplot är 1, lägg till "-l" som kommando.
logstring=""
if(dologplot):
    logstring = " -l"

os.system("histogramifiera.pyw"+" -p \""+pathstring+"\" "+massstring+logstring+">log.txt")
'''