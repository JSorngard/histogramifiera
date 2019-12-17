**Beskrivning**  
Histogramfifiera är ett kort pythonscript som läser txt-filer i den engivna mappen som har exporterats från
programmet Hypatia och plottar dem i ett histogram.
Hypatia låter en prova på att analysera riktig data från partikelkollisioner i LHC vid CERN. Orkar man inte
sitta och generera data genom hypatia för att testa programmet kan man generera sin egen med datagenerator.pyw.

**Systemkrav**  
Kör man programmet via exe-filen så behövs inget extra. Vill man köra pythonkoden direkt behövs:  
- python 3.x  
- matplotlib  
- numpy  
*för att generera egen data behövs även*  
- scipy

**Användning**  
datagenerator.pyw, histogramifiera.exe och histogramifiera.pyw går att köra genom att dubbelklicka på dem. Datagenerator.pyw lägger de genererade filerna i mappen den befinner sig i.