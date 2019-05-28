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
            command=self.return_values)
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

pathstring=""
pathwindow=inputwindow()
pathwindow.master.title("Ange alternativ.")
pathwindow.mainloop()

pathstring.replace("\\","\\\\")

if(massstring != ""):
    try:
        massstring = "-m "+str(int(massstring))
    except:
        massstring = ""

if(pathstring=="" or pathstring==pathdefault):
    pathstring=os.path.dirname(os.path.realpath(__file__))

logstring=""
if(dologplot):
    logstring = " -l"

os.system("histogramifiera.pyw"+" -p \""+pathstring+"\" "+massstring+logstring+">log.txt")