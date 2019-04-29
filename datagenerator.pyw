import random #Behövs för att slumpa tal.
import os #Behövs för at skria och läsa filer.
import numpy as np #Behövs för diverse matte.
from scipy.stats import cauchy #Behövs för att dra från cauchyfördelningen.
#from bisect import bisect #Behövs för invertering av funktioner.
import argparse #Behövs för att läsa in kommandon från kommandotolken.
import matplotlib.pyplot as plt #Behövs för plottning.


#Ta fram vilken mapp vi befinner oss i.
mydir=os.path.dirname(os.path.realpath(__file__))

#Initeira variabler
files=[]
occupied=[]
signalpts=100 #Hur många datapunkter simuleras
signalnoiceratio=.15 #Hur mycket brus i förhållande till signal.
utnamn="simulerad_data_" #Prefix på de genererade filerna.

#------------------------------Hårdkodade alternativ---------------------
particlemasses=[3.096916,91.1876,1000] #GeV/c^2. Massorna hos partiklarna vi vill simulera.
widths=[93.2*10**(3-9),2.4952,10] #GeV/c^2. Massvidderna hos partiklarna.
relativepower=[.1,1,.1] #Hur stark signalen från parikeln är i jämförelse med de andra.
threshold=.005 #Ignorerar att simulera processer mer osannolika än detta.
#-------------------------------------------------------------------------

#Möjliggör användande av extrakommandon i kommandotolken för att ändra beteendet hos programmet.
parser=argparse.ArgumentParser(description='Genererar data som ser ut som den som exporteras från Hypatia.')
parser.add_argument("-n","--datapoints",required=False,type=int,default=signalpts,help="Specificera mängden datapunkter du vill generera med detta argument. Om det inte anges genereras "+str(signalpts)+" datapunkter.")
parser.add_argument("-r","--snratio",required=False,type=int,default=signalnoiceratio,help="Specifiera bruskvoten. Om inget anges används "+str(signalnoiceratio)+" som kvot.")
parser.add_argument("-p","--plot",required=False,action="store_true",help="Om detta argument anges genereras en plot av vilken fördelning programmet har försökt simulera och resultatet, samt den kumulativa fördelningen som använts vid generering av massorna.")
parser.add_argument("-x","--nowrite",required=False,action="store_false",help="Om detta argument anges skrivs inte något ut till fil.")
parser.add_argument("-o","--outputname",required=False,default=utnamn,help="Namnge filen som genereras av programmet. Om inget anges döps filen till "+str(utnamn)+"<siffra>.txt. Detta argument är meningslöst om -x är angett.")
parser.add_argument("-d","--debug",required=False,action="store_true",help="Om denna flagga används skriver programmet ut fler utskrifter.")

#Läs in värdet hos de definierade argumenten.
args=vars(parser.parse_args())

debug=args["debug"]

if(debug):
    print("\nDEBUG-läge aktiverat. Fler utskrifter följer.\n")

signalpts=args["datapoints"]
if(signalpts<=0):
    print("Du måste begära fler än 0 datapunkter.")
    exit()
signalnoiceratio=args["snratio"]
if(signalnoiceratio<0):
    print("Bruskvoten måste vara ett positivt tal.")
    exit()
plot=args["plot"]
write=args["nowrite"]
modutnamn=args["outputname"]

overwrite=False
if(modutnamn!=utnamn):
    overwrite=True
    utnamn=modutnamn

if(debug):
    print("Kommandoradsalternativ inlästa:\n")
    print("    begärda datapunkter: "+str(signalpts)+", bruskvot: "+str(signalnoiceratio)+",")
    print("    ska det plottas? "+str(plot)+", ska det skrivas till fil? "+str(write))
    if(modutnamn and write):
        print("    resultat skrivs till"+mydir+"\\"+utnamn+".txt")

#Binär sökning genom lista. Returnerar indexen för de två närmast liggande punkterna till target.
#Används för att invertera den kumulativa sannolikhetsfördelningen.
def binary_search(array, target):
    lower = 0
    upper = len(array)
    while lower < upper:
        x = lower + (upper - lower) // 2
        val = array[x]
        if target == val:
            return lower,upper
        elif target > val:
            if lower == x:
                break
            lower = x
        elif target < val:
            upper = x
    return lower,upper

if(debug):
    print("Letar efter .txt-filer...")

#Generera en lista över den kompletta sökvägen till alla .txt-filer i den nuvarande mappen.
for file in os.listdir(mydir):
    if file.endswith(".txt"):
        files.append(os.path.join(mydir, file))

#Om inget filnamn angetts, kolla ifall det redan finns datafiler genererade av programmet med standardnamnet.
if(len(files)!=0 and not overwrite):
	for file in files:
		occupied.append(int(file.replace(utnamn,'').replace('.txt','').split("\\")[-1]))
occupied.append(0)

if(debug and len(files)!=0):
    print("    hittade filer.\n")
elif(debug):
    print("    hittade inga filer.\n")

#PHYSICS TIME!

#Normalisera de relativa bidragen
relativepower=relativepower/np.linalg.norm(relativepower)

if(debug):
    print("Beräknar de högsta och lägsta massorna vi simulerar...")

#Ta fram den lägsta och högsta invarianta massan vi simulerar
pts=max([10*signalpts,1000])
minmass=np.max([0,np.min([cauchy.ppf(threshold,m,w) for m,w in zip(particlemasses,widths)])])
maxmass=np.max([cauchy.ppf(1-threshold,m,w) for m,w in zip(particlemasses,widths)])
x=np.linspace(minmass,maxmass,pts)

if(debug):
    print("    maxmassa: "+str(maxmass)+", minmassa: "+str(minmass)+".\n")
    print("Viktar ihop fördelningarna från de olika partiklarna...")

#Vikta ihop alla distributioner.
distcdf=[relativepower[i]*cauchy.cdf(x,m,w) for i,(m,w) in enumerate(zip(particlemasses,widths))]
distcdf=np.sum(distcdf,axis=0)
distcdf=distcdf/np.max(distcdf) #Omnormalisera så att högsta värdet är 1.
if(plot):
    distpdf=[relativepower[i]*cauchy.pdf(x,m,w) for i,(m,w) in enumerate(zip(particlemasses,widths))]
    distpdf=np.sum(distpdf,axis=0)

if(debug):
    print("Klar.\n")
    print("Slumpar data från fördelningen...")
    print(" genererar slumptal...")

#Dra från fördelningen.
probs=[random.random() for i in range(signalpts)]

if(debug):
    print("  inverterar kumulativ sannolikhetsfördelning...")
lus=[binary_search(distcdf,pt) for pt in probs]

if(debug):
    print("   beräknar massor...")
#masses=[distcdf[bisect(distcdf,pt)] for pt in probs] #Ett försök till snabbare invertering.
masses=[(x[l]+x[u])/2 for (l,u) in lus]

if(debug):
    print("Klar.\n")
    if(signalnoiceratio!=0):
        print("Lägger in bakgrundsbrus och fel...")

#Lägg till bakgrundsbrus
if(signalnoiceratio!=0):
    masses=np.append(masses,np.array(random.sample(list(x),int(signalnoiceratio*signalpts))))
    if(debug):
        print("Klar.\n")

if(debug and write):
    print("Skriver ut datan till fil...")

#Skriv ut till en ny fil.
if(write and overwrite):
    np.savetxt(mydir+"\\"+utnamn+".txt",masses,fmt='%f')
elif(write):
    np.savetxt(mydir+"\\"+utnamn+str(max(occupied)+1)+".txt",masses,fmt='%f')

if(debug and write):
    print("Klar.\n")

#Plotta.
if(plot):
    if(debug):
        print("Plottar...")
    cdfplot=plt.figure(2)
    plt.plot(x,distcdf)
    plt.xlabel("Invariant massa [GeV/c^2]")
    plt.title("Kumulativ sannolikhetsfördelning")

    pdfplot=plt.figure(1)
    N=len(masses)
    binfactor=2
    #Skalar om sannolikhetsfördelningen så att den går att se i histogrammet.
    plt.plot(x,10/binfactor*N*distpdf,label="Sannolikhetsfördelning")
    bins=int(round(binfactor*np.sqrt(N)))
    plt.hist(masses,bins=bins,label="Data")
    plt.xlabel("Invariant massa [GeV/c^2]")
    plt.title("Skalad sannolikhetsfördelning och datan som genererades från den.")
    plt.legend()
    plt.show()
if(debug):
    print("Klar med programmet.\n")