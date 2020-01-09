"""
Kodades av J Sörngård under 2019 för Vetenskapens hus.
histogramifiera läser in data om partikelmassor som har exporterats
från Hypatia.exe i form av txt-filer och plottar den i ett histogram.
"""

#-------------Importera alla moduler som behövs------------
import tkinter as tk #Behövs för GUI.
import os #Behövs för att hitta sökvägar.
import ctypes #Behövs för att visa rutor med felmeddelanden.
import numpy as np #Behövs för generering av logaritmiska plottar.
from matplotlib import pyplot as plt #Behövs för plottning.
#----------------------------------------------------------


#------------Namn på olika textelement.--------------------
pathdefault = ""
massdefault = ""
bindefault = "1"
debugdefault = False
buttondefault = "Histogramifiera!"
maxmassatext = "Maximal massa att plotta till"
bintext = "Binfaktor"
sokvagstext = "Sökväg till data"
logplottext = "Gör logaritmisk plot"
titeltext = "Ange alternativ"
debugtext = "Debuginfo till loggen"
#----------------------------------------------------------

#------------------Programalternativ-----------------------
width = 300 #Bredd på fönstret i pixlar.
height = 114 #Höjd på fönstret i pixlar.
#----------------------------------------------------------

#-------------------HÅRDKODADE ALTERNATIV------------------
version = "v1.02"
min_massa = 0     #Datavärden under detta ignoreras.
pile = ['e','m','4ee','4mm','4me',' '] #En hög med skräp som ska rensas bort ur alla txt-filer. Placera ' ' sist.
#----------------------------------------------------------

#Ta fram nuvarande sökväg.
current_path = os.path.dirname(os.path.realpath(__file__))

def fel(meddelande):
    """Funktion som tar emot en sträng och öppnar ett fönster med den strängen i."""
    ctypes.windll.user32.MessageBoxW(0,meddelande,"Fel", 1)

class inputwindow(tk.Frame):
    """
    Ett litet fönster som läser in diverse input och 
    skickar den vidare till histogramifiera.
    """
    def __init__(self, master=None):
        tk.Frame.__init__(self,master)
        self.grid(sticky="news")
        master.rowconfigure(0,weight=1)
        master.columnconfigure(0,weight=1)
        self.createWidgets()

    def createWidgets(self):
        """
        Initierar alla knappar och textfält som används av programmet.
        """
        
        #Skapa ett textfält för sökvägen
        self.pathfield = tk.Entry() #Skapa fältet.
        self.pathfield.insert(0,pathdefault) #Stoppa in defaulttexten.
        self.pathfield.grid(row=1,column=1) #Placera det i fönstret.

        #Placera förklarande text bredvid
        self.pathlabeltext = tk.StringVar() #Skapa en sträng.
        self.pathlabeltext.set(sokvagstext) #Sätt strängen till defaulttexten.
        self.pathlabel = tk.Label(textvariable=self.pathlabeltext) #Skapa en etikett.
        self.pathlabel.grid(row=1,column=0) #Sätt texten på etiketten till den nyligen skapade strängen.

        #Skapa ett textfält för den maximala massan.
        self.massfield = tk.Entry()
        self.massfield.insert(0,massdefault)
        self.massfield.grid(row=2,column=1)

        #Placera förklarande text bredvid.
        self.masslabeltext = tk.StringVar()
        self.masslabeltext.set(maxmassatext)
        self.masslabel = tk.Label(textvariable=self.masslabeltext)
        self.masslabel.grid(row=2,column=0)

        #Skapa ett textfält för att läsa in en binfaktor.
        self.binfield = tk.Entry()
        self.binfield.insert(0,bindefault)
        self.binfield.grid(row=3,column=1)

        #Placera förklarande text bredvid.
        self.binlabeltext = tk.StringVar()
        self.binlabeltext.set(bintext)
        self.binlabel = tk.Label(textvariable=self.binlabeltext)
        self.binlabel.grid(row=3,column=0)

        #Skapa och placera en kryssruta för om man vill göra en logplot.
        self.dolog = tk.IntVar() #Skapa en integer.
        self.logcheck = tk.Checkbutton(variable=self.dolog) #Skapa en kryssruta som lagrar resultatet i den nyligen skapade integern.
        self.logcheck.grid(row=4,column=1) #Placera kryssrutan i fönstret.

        #Placera en förklarande text bredvid.
        self.loglabeltext = tk.StringVar()
        self.loglabeltext.set(logplottext)
        self.loglabel = tk.Label(textvariable=self.loglabeltext)
        self.loglabel.grid(row=4,column=0)

        #Skapa en knapp som kallar på prepare_histogramifiera när den trycks på.
        self.gobutton = tk.Button(text=buttondefault,command=self.prepare_histogramifiera)
        self.gobutton.grid(row=5,column=1)

        #---Denna ruta och dess text placeras ovanför fönstret. Man måste förstora det för att se.
        #Skapa och placera en kryssruta för om man vill skriva debuginformation till loggen.
        self.dodebug = tk.IntVar()
        self.debugcheck = tk.Checkbutton(variable=self.dodebug)
        self.debugcheck.grid(row=0,column=1)
        if debugdefault: #Det är också möjligt att aktivera denna ruta genom kommandoraden.
            self.debugcheck.select()

        #Placera en förklarande text bredvid.
        self.debuglabeltext = tk.StringVar()
        self.debuglabeltext.set(debugtext)
        self.debuglabel = tk.Label(textvariable=self.debuglabeltext)
        self.debuglabel.grid(row=0,column=0)
        #---

        #Placera fokus i sökvägsfältet.
        self.pathfield.focus_set()

    def histogramifiera(self,sokvag,max_massa,log_plot,binfaktor,debug):
        """
        Läser in all data i txt-filer genererade av Hypatia som
        befinner sig i sökvägen sokvag. Rensar dem på skräp och
        plottar sedan datan som ett histogram. Plottar inte någon
        data som är större än max_massa. Om log_plot är sann så
        görs en logaritmisk plot istället. Antalet staplar i
        histogramet multipliceras med binfaktor. Om debug är
        sann genereras en loggfil som innehåller information
        om vad programmet gjort.
        """

        if not os.path.isdir(sokvag):
            fel("Den angivna sökvägen är inte giltig. Angiven sökväg: \'"+sokvag+"\'.")
            return

        #Alla 'if debug ' utförs endast om den lilla debugrutan är ikryssad.
        if debug:
            #Skapa en logfil.
            log = open("histogramifiera_log.txt","w")
            log.write("Detta är histogramifiera "+version+", skrivet av J Sörngård åt Vetenskapens Hus under 2019. Källkoden (och eventuella uppdateringar) finns på https://github.com/JSorngard/histogramifiera/releases.")
            log.write("DEBUG-läge aktiverat, fler utskrifter följer.\n")
            log.write("\nStapelfaktor: "+str(binfaktor)+", logplot?: "+str(log_plot)+", maximal massa: "+str(max_massa)+".\n")
            log.write("Letar efter txt-filer i "+sokvag+"...\n")
            
        #Generera en lista över den kompletta sökvägen till alla txt-filer i den nuvarande mappen.
        files = []
        for file in os.listdir(sokvag):
            if file.endswith(".txt"):
                files.append(os.path.join(sokvag, file))
            
        #Om det inte hittades några txt-filer så avslutar programmet sig självt.
        if len(files) == 0:
            fel("Hittade inga txt-filer. Placera programmet i, eller ange via kommandorad eller GUI, en sökväg till en mapp med txt-filer genererade av Hypatia. Använde sökvägen: \'"+sokvag+"\'.")
            return
        elif debug:
            log.write("Hittade "+str(len(files))+" stycken.\n")

        #En plats att lägga all data på.
        data = np.array([])

        #För varje sådan txt-fil vi hittade
        for fil in files:

            if debug:
                log.write("Bearbetar "+str(fil)+"...\n")
            
            #Ifall fil inte har fler än 23 tecken i sitt namn
            #så ligger denna bit i ett tryblock.
            try:
                if fil[-23:] == "histogramifiera_log.txt":
                    if debug:
                        log.write(" det var loggen, skippa den.\n")
                    continue
            except:
                #Det var inte loggen då den garanterat har åtminståne 23 tecken,
                #så vi ignorerar felet.
                pass

            #Så öppnar vi den.
            with open(fil,'r') as nuvarande_fil:
                if debug:
                    log.write(" öppnade\n")
                #Och läser in dess innehåll.
                contents = nuvarande_fil.read()
                if debug:
                    log.write("  läste in innehållet\n")


            #Sedan tar vi bort alla 'e', 'm', '4ee', '4mm', '4me' och ' '.
            for trash in pile:
                contents = contents.replace(trash,"")
            
            #Och delar upp filen efter radbrytningar.
            contents = contents.split("\n")

            #Sedan filtrerar vi ut alla rader som inte är någonting.
            contents = list(filter(lambda x: x!='',contents))

            if debug:
                log.write("    rensade datan\n")

            #Och försöker omvandla allt kvarvarande innehåll till flyttal.
            try:
                contents = [ float(entry) for entry in contents ]
            except:
                #Funkar det inte så antar vi att filen inte skapades av Hypatia och går vidare till nästa.
                if debug:
                    log.write("    inte en Hypatiafil (kunde inte omvandla till flyttal). Skippar till nästa.\n")
                continue
            
            if debug:
                log.write("     konverterade datan till flyttal\n")
            
            #Sedan lägger vi in den resulterande arrayen av siffror i slutet av 'data'.
            data = np.append(data,np.array(contents))
            
        #Filtrera ut datapunkter större än max_massa (om angett) och mindre än min_massa.
        if max_massa != 0:
            data = np.array(list(filter(lambda x: x > min_massa and x < max_massa,data)))
        else:
            data = np.array(list(filter(lambda x: x > min_massa,data)))

        if debug and max_massa == 0:
            log.write("Filtrerade ut för små massor.\n")
        elif debug:
            log.write("Filtrerade ut för små och för stora massor.\n")

        #Beräkna antalet staplar.
        sig = int(round(binfaktor*np.sqrt(len(data))))

        #Om vi vill göra en logplot så måste staplarna skalas korrekt.
        if log_plot:
            bins = np.logspace(np.log10(min(data)),np.log10(max(data)),sig)
        else:
            bins = sig
            
        if debug:
            log.write("Plottar...\n")
            
        #Rensa vad som redan kan tänkas finnas i fönstret.
        plt.clf()

        #Plotta histogrammet...
        plt.hist(data,bins=bins)

        #och sätt x-axeln till logaritmisk om vi gör en logplot.
        if log_plot:
            plt.gca().set_xscale("log")
        else:
            plt.gca().set_xscale("linear")

        #Plotinställningar
        plt.xlabel("Invariant massa [GeV/c^2]")
        plt.ylabel("Antal händelser")

        #Gör så att fönstret går att interagera med samtidigt som man ändrar på saker
        #i inställningsfönstret.
        plt.ion()

        #Visa resultatet.
        plt.show()

        if debug:
            log.write("Slut på loggen.")
            log.close()

    def prepare_histogramifiera(self):
        """
        Funktion som extraherar data från alla fönsterelement,
        bearbetar den och skickar den till histogramifiera.
        """
        sokvag = self.pathfield.get()
        max_massa = self.massfield.get()
        gorlogplot = self.dolog.get()
        binfaktor = self.binfield.get()
        debug = self.dodebug.get()

        #Byt ut \ mot \\ så att de kommer att tolkas korrekt av histogramifiera.
        sokvag.replace("\\","\\\\")

        #Testa att läsa in maxmassan till en int, funkar det inte visas ett felmeddelande.
        if max_massa != "" and max_massa != "0":
            try:
                max_massa = float(max_massa)
            except:
                fel("Den maximala massan måste vara en siffra.")
                return
            if max_massa <= min_massa:
                fel("Den maximala massan måste vara positiv.")
                return
        else:
            max_massa = 0

        try:
            binfaktor = float(binfaktor)
        except:
            fel("Binfaktorn måste vara en siffra.")
            return

        #Om en sökväg inte är angiven, skicka nuvarande plats.
        if sokvag == "":
            sokvag = current_path

        #Om logplot är 1, gör en logplot
        log_plot = True if gorlogplot else False

        #Histogramifiera!
        self.histogramifiera(sokvag,max_massa,log_plot,binfaktor,debug)


#------------Startar upp det lilla inputfönstret-----------
root = tk.Tk() #Skapa ett fönsterobjekt.
root.title(titeltext) #Ange fönstrets titel.
root.geometry(str(width)+"x"+str(height))
root.minsize(width=width,height=height) #Gör så att fönstret inte går att förminska under en minimistorlek.
program = inputwindow(master=root) #Lägg in alla funktioner definierade i inputwindow.
program.mainloop() #Starta fönstret.
#----------------------------------------------------------
