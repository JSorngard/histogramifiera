**Beskrivning**  
Histogramifiera är en kort pythonscript som läser txt-filer som har exporterats från
programmet Hypatia i den angivna mappen och plottar dem i ett histogram.  
Hypatia låter en prova på att analysera riktig data från partikelkollisioner i LHC vid CERN. Orkar man inte
sitta och generera data genom hypatia för att testa programmet kan man generera sin egen med datagenerator.pyw.  
Detta program skrevs av J Sörngård under 2019 och 2020.

**Systemkrav för att köra pythonkoden**  
Kör man programmet via exe-filen under [releases på gihub](https://github.com/JSorngard/histogramifiera/releases) så behövs inget extra. Vill man köra pythonkoden direkt behövs:  
- python 3.x med modulerna:  
- matplotlib  
- numpy  
*för att generera egen data behövs även*  
- scipy

**Systemkrav för att kompilera källkoden till en exekverbar windowsfil**  
- Allt som krävs för att köra pythonkoden, samt  
- PyInstaller

**Kompilering**  
Kör kommandot "python -m PyInstaller --onefile -w histogramifiera.pyw" i en kommandotolk som befinner sig i mappen med histogramifiera.pyw. Efteråt så finns histogramifiera.exe i den nya mappen "dist".  
Vill man göra en exe-fil som startar snabbare kan man skippa --onefile, men då genereras många filer som alla behövs för att programmet ska köra. I detta fall kan det vara användbart att använda sig av NSIS för att komprimera alla filer och mappar i dist/histogramifiera till en självextraherande installationsfil.

**Användning**  
datagenerator.pyw och histogramifiera.pyw går att köra genom att dubbelklicka på dem. Datagenerator.pyw lägger de genererade filerna i mappen den befinner sig i.
