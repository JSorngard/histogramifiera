#Kodades av Johan Sörngård för Vetenskapens hus.

if(not __name__=="__main__"):
    print("histogramifiera_GUI: Måste köras som huvudprogram.")
    exit()

import tkinter as tk #Behövs för GUI.
import os #Behövs för att hitta sökvägar.
import subprocess #Behövs för att kalla på histogramifiera.pyw
import ctypes #Behövs för att visa rutor med felmeddelanden.

#------------Namn på olika textelement.--------------------
pathdefault=""
massdefault=""
buttondefault="Histogramifiera!"
maxmassatext="Maximal massa att plotta till"
sokvagstext="Sökväg till data"
logplottext="Gör logaritmisk plot"
titeltext="Ange alternativ"
#----------------------------------------------------------

#Ta fram nuvarande sökväg.
currentpath=os.path.dirname(os.path.realpath(__file__))

def fel(meddelande):
    """Funktion som tar emot en sträng och öppnar ett fönster med den stängen i."""
    ctypes.windll.user32.MessageBoxW(0,meddelande,"Fel", 1)

class inputwindow(tk.Frame):
    """Ett litet fönster som läser in diverse input och skicakr den vidare till histogramifiera."""
    def __init__(self, master=None):
        tk.Frame.__init__(self,master)
        self.grid(sticky="news")
        master.rowconfigure(0,weight=1)
        master.columnconfigure(0,weight=1)
        self.createWidgets()

    def createWidgets(self):
        
        #Skapa ett textfält för sökvägen
        self.pathfield = tk.Entry() #Skapa fältet.
        self.pathfield.insert(0,pathdefault) #Stoppa in defaulttexten.
        self.pathfield.grid(row=0,column=1) #Placera det i fönstret.

        #Placera förklarande text bredvid
        self.pathlabeltext = tk.StringVar() #Skapa en sträng.
        self.pathlabeltext.set(sokvagstext) #Sätt strängen till defaulttexten.
        self.pathlabel = tk.Label(textvariable=self.pathlabeltext) #Skapa en etikett.
        self.pathlabel.grid(row=0,column=0) #Sätt texten på etiketten till den nyligen skapade strängen.

        #Skapa ett textfält för den maximala massan.
        self.massfield = tk.Entry()
        self.massfield.insert(0,massdefault)
        self.massfield.grid(row=1,column=1)

        #Placera förklarande text bredvid.
        self.masslabeltext = tk.StringVar()
        self.masslabeltext.set(maxmassatext)
        self.masslabel = tk.Label(textvariable=self.masslabeltext)
        self.masslabel.grid(row=1,column=0)

        #Skapa och placera en kryssruta för om man vill göra en logplot.
        self.dolog = tk.IntVar() #Skapa en integer.
        self.logcheck = tk.Checkbutton(variable=self.dolog) #Skapa en kryssruta som lagrar resultatet i den nyligen skapade integern.
        self.logcheck.grid(row=2,column=1) #Placera kryssrutan i fönstret.

        #Placera en förklarande text bredvid.
        self.loglabeltext = tk.StringVar()
        self.loglabeltext.set(logplottext)
        self.loglabel = tk.Label(textvariable=self.loglabeltext)
        self.loglabel.grid(row=2,column=0)

        #Skapa en knapp som kallar på run_histogramifiera när den trycks på.
        self.gobutton = tk.Button(text=buttondefault,command=self.run_histogramifiera)
        self.gobutton.grid(row=3,column=1)

        #Placera fokus i sökvägsfältet.
        self.pathfield.focus_set()

    def run_histogramifiera(self):
        """Funktion som extraherar data från alla fönsterelement, bearbetar den och skickar den till histogramifiera."""
        sokvag=self.pathfield.get()
        maxmassa=self.massfield.get()
        gorlogplot=self.dolog.get()

        #Byt ut \ mot \\ så att de kommer att tolkas korrekt av histogramifiera.pyw.
        sokvag.replace("\\","\\\\")

        #Testa att läsa in maxmassan till en int, funkar det inte visas ett felmeddelande, annars skickas den med "-m".
        if(maxmassa != "" and maxmassa != "0"):
            try:
                maxmassa = "-m "+str(int(maxmassa))
            except:
                fel("Ogiltig maxmassa")
                return
        else:
            maxmassa = ""

        #Om en sökväg inte är angiven, skicka nuvarande plats med "-p".
        if(sokvag=="" or sokvag==pathdefault):
            sokvag=currentpath

        #Om logplot är 1, lägg till "-l" som kommando.
        logstring=""
        if(gorlogplot):
            logstring = " -l"

        log=subprocess.check_output("pythonw histogramifiera.pyw"+" -p \""+sokvag+"\" "+maxmassa+logstring)
        logfil=open("log.txt","w")
        logfil.write(str(log))
        logfil.close()
        #os.system("histogramifiera.pyw"+" -p \""+sokvag+"\" "+maxmassa+logstring+">log.txt")

#------------Startar upp det lilla inputfönstret-----------
root=tk.Tk()
root.title(titeltext) #Ange fönstrets titel.
try:
    #Försök sätta fönsterikonen till kugghjul.ico.
    root.iconbitmap("kugghjul.ico")
except:
    #Finns den inte så strunta i det.
    pass
program=inputwindow(master=root) #Lägg in alla funktioner definierade i inputwindow.
program.mainloop() #Starta fönstret.
#----------------------------------------------------------