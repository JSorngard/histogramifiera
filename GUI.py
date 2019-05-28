import tkinter as tk
import os

class inputwindow(tk.Frame):
    """Ett litet fönster som läser in diverse input och lagrar den i variabler."""
    def __init__(self, master=None):
        tk.Frame.__init__(self,master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        self.acceptButton = tk.Button(self,text="Ok",
            command=self.return_values)
        self.acceptButton.grid()
        self.entryfield = tk.Entry()
        self.entryfield.insert(0,"Sökväg")
        self.entryfield.grid()
        self.massfield = tk.Entry()
        self.massfield.insert(0,"Maxmassa")
        self.massfield.grid()
        self.entryfield.focus_set()

    def return_values(self):
        global pathstring
        global massstring
        pathstring = self.entryfield.get()
        massstring = self.massfield.get()
        self.quit()
        return pathstring, massstring

pathstring=""
pathwindow=inputwindow()
pathwindow.master.title("Ange sökväg.")
pathwindow.mainloop()

pathstring.replace("\\","\\\\")

if(massstring != ""):
    try:
        massstring = "-m "+int(massstring)
    except:
        massstring = ""

if(pathstring==""):
    pathstring=os.path.dirname(os.path.realpath(__file__))

os.system("python histogramifiera.pyw"+" -p \""+pathstring+"\" "+massstring)