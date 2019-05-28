#Kodade av Johan Sörngård för Vetenskapens hus.

import sys
import subprocess
import ctypes
import os

dependecies=["scipy","numpy","matplotlib"]
installerat=[]
wait=10

def is_admin():
	try:
		return ctypes.windll.shell32.IsUserAnAdmin()
	except:
		return False

if(int(sys.hexversion) < 50791408):
	print("En uppdaterad version av python 3 behövs. Den kan laddas ned från www.python.org.")
	os.system("pause")
	exit()

if(not is_admin()):
	ctypes.windll.shell32.ShellExecuteW(None,"runas",sys.executable,__file__,None,1)
	exit()

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

os.system("pause")