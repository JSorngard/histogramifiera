import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import cauchy
import imageio
import argparse
import os

mydir=os.path.dirname(os.path.realpath(__file__))

bildrutor=10 #Hur många bildrutor genereras?
varaktighet=5 #Hur många sekunder varar giffen?
pnktr=1000 #Hur många datapunkter skapar vi?
massa=130 #Simulerad partikels massa.
bredd=5 #Simulerad partikels bredd.
skala=1000 #Cauchyfördelningen skalas med detta tal.
#Använd för att få fler händelser på y-axeln.
bakgrund=5 #Storlek på bakgrundbruser.
sparabilder=False #Ska bilderna sparas var för sig?
skapagif=False #Ska bilderna kombineras till en gif?
loopa=False #Ska giffen loopa?

parser=argparse.ArgumentParser(description="Enkel pythonscript som kan användas för att generera plotter för att förklara hur det kommer sig att masspektrat i bosonjaktsbesöket ser ut som det gör.")
parser.add_argument("-m","--massa",required=False,type=float,default=massa,help="Ange partikelns massa i GeV/c^2. Använder "+str(massa)+" som standard.")
parser.add_argument("-w","--bredd",required=False,type=float,default=bredd,help="Ange partikelns bredd. Använder "+str(bredd)+" som standard.")
parser.add_argument("-r","--bildrutor",required=False,default=bildrutor,type=int,help="Specificera antalet bildrutor som ska genereras.")
parser.add_argument("-b","--sparabilder",required=False,action="store_true",help="Ange detta kommando för att spara de genererade bilderna var för sig.")
parser.add_argument("-g","--sparagif",required=False,action="store_true",help="Ange detta kommando för att spara de genererade bilderna som en gif.")
parser.add_argument("-l","--loopa",required=False,action="store_true",help="Ange detta kommando om du vill att giffen ska loopa för evigt.")

args=vars(parser.parse_args())

bildrutor=args["bildrutor"]
sparabilder=args["sparabilder"]
skapagif=args["sparagif"]
loopa=args["loopa"]
massa=args["massa"]
bredd=args["bredd"]

maxmassa=(100*bredd/massa+massa)*1.6

if(loopa):
	loopa=0
else:
	loopa=1

x=np.linspace(0,maxmassa,pnktr)
y=skala*cauchy.pdf(x,massa,bredd)
nothing=np.zeros(pnktr)
y=np.add(bakgrund*np.random.rand(pnktr),y)
xtext="Kollisionsenergi [GeV]"
ytext="Antal händelser"
titel="Fältrespons"
ymax=1.2*np.max(y)
counter=1
gifbildrutor=[]
fps=int(round(bildrutor/varaktighet))
if(sparabilder or skapagif):
	for i in range(0,pnktr,int(round(pnktr/bildrutor))):
		fig=plt.figure()
		fig.add_subplot(111)
		plt.plot(x,np.concatenate((y[0:i],nothing[i:])))
		plt.ylim(0,ymax)
		plt.xlabel(xtext)
		plt.ylabel(ytext)
		plt.title(titel)
		fig.canvas.draw()
		if(sparabilder):
			plt.savefig("energi_"+str(round(x[i]))+".png")
		if(skapagif):
			data=np.frombuffer(fig.canvas.tostring_rgb(),dtype=np.uint8)
			data=data.reshape(fig.canvas.get_width_height()[::-1]+(3,))
			gifbildrutor.append(data)
		plt.close()
		print(str(100*counter/bildrutor)[:4]+"% klar.")
		counter+=1
else:
	print("Klar.")

if(sparabilder):
	print("Klar.")

if(skapagif):
	print("Sparar animation...")
	imageio.mimsave(mydir+"\\energisvep.gif",gifbildrutor,fps=fps,subrectangles=True,loop=loopa)
	print("Klar.")