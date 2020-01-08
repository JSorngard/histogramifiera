**Beskrivning**  
Histogramfifiera är ett kort pythonscript som läser txt-filer i den engivna mappen som har exporterats från
programmet Hypatia och plottar dem i ett histogram.
Hypatia låter en prova på att analysera riktig data från partikelkollisioner i LHC vid CERN. Orkar man inte
sitta och generera data genom hypatia för att testa programmet kan man generera sin egen med datagenerator.pyw.

**Systemkrav för att köra pythonkoden**  
Kör man programmet via exe-filen under [releases på gihub](https://github.com/JSorngard/histogramifiera/releases) så behövs inget extra. Vill man köra pythonkoden direkt behövs:  
- python 3.x  
- matplotlib  
- numpy  
*för att generera egen data behövs även*  
- scipy

**Systemkrav för att kompilera källkoden till en exekverbar windowsfil**  
- Allt som krävs för att köra pythonkoden, och  
- pyinstaller

**Kompilering**  
Kör kommandot "python -m PyInstaller --onefile -w histogramifiera.pyw" i en kommandotolk som befinner sig i mappen med histogramifiera.pyw. Efteråt så finns histogramifiera.exe i den nya mappen "dist".

**Användning**  
datagenerator.pyw och histogramifiera.pyw går att köra genom att dubbelklicka på dem. Datagenerator.pyw lägger de genererade filerna i mappen den befinner sig i.
