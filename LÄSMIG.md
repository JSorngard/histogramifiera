**Beskrivning**  
Histogramfifiera är ett kort pythonscript som läser txt-filer i den nuvarande mappen som har exporterats från
programmet Hypatia och plottar dem i ett histogram. Körs det via en kommandotolk kan diverse alternativ anges
för att ändra programmets beteende (skriv python histogramifiera.pyw -h i mappen med programmet för att se
möjligheterna).  
Hypatia låter en prova på att analysera riktig data från partikelkollisioner i LHC vid CERN. Orkar man inte
sitta och generera data genom hypatia för att testa programmet kan man generera sin egen med datagenerator.pyw.

**Systemkrav**  
- python 3.x  
- matplotlib  
- numpy  
*för att generera egen data behövs även*  
- scipy

**Installation**  
Börja med att se till att [python](www.python.org) 3.x är installerat och finns med i miljövariabeln PATH.  
Kör installera.py. Denna korta script försöker ladda ner de krävda python paketen via pip.  

**Användning**  
Både datagenerator.pyw och histogramifiera.pyw går att köra genom att dubbelklicka på dem. De kör då med
sina grundinställningar.  datagenerator.pyw lägger de genererade filerna i mappen den befinner sig i.  
histogramifiera.pyw antar att alla .txt-filer som finns i samma mapp som den själv kommer antingen från Hypatia
eller datagenerator.pyw, är detta inte sant kan problem uppstå.

Om man vill ha ett grafiskt användargränssnitt för inmatning av alternativ kan man köra histogramifiera_GUI.pyw
istället.