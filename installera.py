import sys
import subprocess
import time as t

dependecies=["scipy","numpy","matplotlib"]
installerat=[]
wait=10

if(__name__=='__main__'):
	#Hoppas pip finns...
	modlist=str(subprocess.check_output([sys.executable,"-m","pip","list"]))
	
	#Uppdatera pip om det behövs
	pipup=False
	if("You should consider upgrading" in modlist):
		pipup=True
		subprocess.call([sys.executable,"-m","pip","install","--upgrade","pip"])

	for dependency in dependecies:
		if(dependency not in modlist):
			print("Kunde inte hitta "+dependency+", installerar...")
			subprocess.call([sys.executable,"-m","pip","install",dependency])
			print("Färdig med "+dependency+".")
	if(pipup):
		print("Uppdaterade pip.")
	if(any(installerat)):
		print("Färdiginstallerat. Röd text ovanför detta meddelande är dåligt.")
		installeradepaket=[dependecies[i] for i in range(len(dependecies)) if installerat[i]]
		print("Behandlade"+str(installeradepaket))
	else:
		print("Ingenting behöver installeras.")
else:
	print("Något gick fel...")

print("Du kan stänga detta fönster. Det stängs av sig självt om "+str(wait)+" sekunder.")
t.sleep(wait)