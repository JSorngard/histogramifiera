import os #Behövs för filinläsning
import numpy as np #Behövs för generering av logplottar
from matplotlib import pyplot as plt #Behövs för plottning
import argparse #Behövs för att läsa in kommandon från kommandotolken.

#-------------------HÅRDKODADE ALTERNATIV------------------------------------------
minval=0     #Datavärden under detta ignoreras.
#----------------------------------------------------------------------------------

#Ta fram vilken mapp vi befinner oss i.
mydir=os.path.dirname(os.path.realpath(__file__))

#Initiera variabler.
files=[]
data=np.array([])

#--------------------Lägg till lyssning efter extrakommandon.-------------------
#--------------Endast relevant om programmet körs via kommandotolken.-----------
#-------------------------------------------------------------------------------

#Skapa objektet som lyssnar efter kommandon.
parser=argparse.ArgumentParser(description='Genererar histogram av invarianta massor lagrade i de .txt-filer som skapas av Hypatia. Placera denna fil och alla .txt-filer du vill analysera i samma mapp och kör sedan programmet.')

#Definiera de möjliga argumenten.
parser.add_argument("-l","--logplot",required=False,dest="loghist",action="store_true",help="Inkludera detta kommando om du vill ha en logaritmisk plot.")
parser.add_argument("-n","--no-logplot",required=False,dest="loghist",action="store_false",help="Inkludera detta kommando om du vill ha en linjär plot. Om inget annat anges körs detta som standard.")
parser.add_argument("-b","--binmult",required=False,default=1.,type=float,help="Multiplicerar antalet staplar med denna faktor. Om inget annat anges är den 1. Antalet staplar beräknas som roten ur mängden datapunkter.")
parser.add_argument("-m","--maxmass",required=False,default=0,type=int,help="Filtrerar ut datapunkter med invarianta massor högre än detta värde. Om inget värde anges ignoreras denna gräns.")
parser.add_argument("-d","--debug",required=False,dest="debugging",action="store_true",help="Ange detta kommando om du vill få ut extrautskrifter från programmet.")

#Läs in värdet hos de definierade argumenten.
args=vars(parser.parse_args())

#Extrahera deras värden till relevanta variabler och se till att de är okej.
binfactor=args["binmult"]
if(binfactor<0):
    print("Antalet staplar kan endast multipliceras med ett positivt tal. Byter tecken på "+str(binfactor)+".")
    binfactor*=-1
loghist=args["loghist"]
maxval=args["maxmass"]
if(maxval<0):
    print("Maxmassan måste vara positiv. Byter tecken på "+str(maxval)+".")
    maxval*=-1
debug=args["debugging"]

#Alla 'if(debug)' utförs endast om kommandoradsalternativet -d är angett.
if(debug):
    print("\nDEBUG-läge aktiverat, fler utskrifter följer.\n")
    print("Kommandoradsalternativ är inlästa:")
    print("    stapelfaktor: "+str(binfactor)+", logplot: "+str(loghist)+", maxmassa: "+str(maxval)+".\n")
    
#-------------------------------------------------------------------------------

if(debug):
    print("Letar efter .txt-filer i nuvarande mapp...")

#Generera en lista över den kompletta sökvägen till alla .txt-filer i den nuvarande mappen.
for file in os.listdir(mydir):
    if file.endswith(".txt"):
        files.append(os.path.join(mydir, file))
    
#Om det inte hittades några .txt-filer så avslutar programmet sig självt.
if(len(files)==0):
    print("Nuvarande plats innehåller inga .txt-filer. Placera programmet och de exporterade .txt-filerna från Hypatia i samma mapp och försök igen.")
    exit()
elif(debug):
    print("Hittade "+str(len(files))+" stycken.\n")

#För varje sådan .txt-fil vi hittade
for fil in files:
    if(debug):
        print("Bearbetar "+str(fil)+"...")
              
    #Så öppnar vi den.
    with open(fil,'r') as myfile:
        if(debug):
            print(" öppnade")
        #Och läser in dess innehåll.
        contents=myfile.read()
        if(debug):
            print("  läste in innehållet")

    #Sedan tar vi bort alla 'e', 'm', '4ee', '4mm', '4me' och ' '.
    contents=contents.replace("4ee","").replace("4me","").replace("4mm","").replace("e","").replace("m","").replace(" ","")
    
    #Och delar upp filen efter radbrytningar.
    contents=contents.split("\n")

    #Sedan filtrerar vi ut alla rader som inte är någonting.
    contents=list(filter(lambda x: x!='',contents))

    if(debug):
        print("    rensade datan")

    #Och omvandlar allt kvarvarande innehåll till flyttal.
    contents=[float(entry) for entry in contents]

    if(debug):
        print("     konverterade datan till flyttal\n")
    
    #Sedan lägger vi in den resulterande arrayen av siffror i slutet av 'data'.
    data=np.append(data,np.array(contents))
    
#Filtrera ut datapunkter större än maxval (om angett) och mindre än minval.
if(maxval!=0):
    data=np.array(list(filter(lambda x: x>minval and x<maxval,data)))
else:
    data=np.array(list(filter(lambda x: x>minval,data)))

if(debug and maxval==0):
    print("Filtrerade ut för små massor.")
elif(debug):
    print("Filtrerade ut för små och för stora massor.")



#Beräkna antalet staplar.
sig=int(round(binfactor*np.sqrt(len(data))))

#Om vi vill göra en logplot så måste staplarna skalas korrekt.
if(loghist):
    bins=np.logspace(np.log10(min(data)),np.log10(max(data)),sig)
else:
    bins=sig
    
if(debug):
    print("Plottar...\n")
    
#Plotta histogrammet...
plt.hist(data,bins=bins)

#och sätt x-axeln till logaritmisk om vi gör en logplot.
if(loghist):
    plt.gca().set_xscale("log")
else:
    plt.gca().set_xscale("linear")

#Plotinställningar
plt.xlabel("Invariant massa [GeV/c^2]")
plt.ylabel("Antal händelser")

#Visa resultatet.
plt.show()
