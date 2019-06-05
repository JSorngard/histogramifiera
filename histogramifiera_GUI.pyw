#Kodades av Johan Sörngård för Vetenskapens hus.

import tkinter as tk
import os
import subprocess
import ctypes

pathdefault=""
massdefault=""
buttondefault="Histogramifiera!"
maxmassatext="Maximal massa att plotta till"
sokvagstext="Sökväg"
logplottext="Logplot"
titeltext="Ange alternativ"
currentpath=os.path.dirname(os.path.realpath(__file__))

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
        self.pathfield = tk.Entry()
        self.pathfield.insert(0,pathdefault)
        self.pathfield.grid(row=0,column=1)

        #Placera förklarande text bredvid
        self.pathlabeltext = tk.StringVar()
        self.pathlabeltext.set(sokvagstext)
        self.pathlabel = tk.Label(textvariable=self.pathlabeltext)
        self.pathlabel.grid(row=0,column=0)

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
        self.dolog = tk.IntVar()
        self.logcheck = tk.Checkbutton(text=logplottext,variable=self.dolog)
        self.logcheck.grid(row=2,column=0)

        #Skapa en knapp som kallar på run_histogramifiera när den trycks på.
        self.gobutton = tk.Button(text=buttondefault,command=self.run_histogramifiera)
        self.gobutton.grid(row=3,column=1)

        #Gör så att även tomma rader och kolonner tar plats.
        #for i in range(2):
        #    self.columnconfigure(i,weight=1)
        #for i in range(3):
        #    self.rowconfigure(i,weight=1)

        #Placera fokus i sökvägsfältet.
        self.pathfield.focus_set()

    def run_histogramifiera(self):
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
                ctypes.windll.user32.MessageBoxW(0,"Ogiltig maxmassa", "Fel", 1)
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

        log=subprocess.check_output("python histogramifiera.pyw"+" -p \""+sokvag+"\" "+maxmassa+logstring)
        logfil=open("log.txt","w")
        logfil.write(str(log))
        logfil.close()
        #os.system("histogramifiera.pyw"+" -p \""+sokvag+"\" "+maxmassa+logstring+">log.txt")

#Startar upp det lilla inputfönstret.
root=tk.Tk()
root.title(titeltext)
program=inputwindow(master=root)
program.mainloop()