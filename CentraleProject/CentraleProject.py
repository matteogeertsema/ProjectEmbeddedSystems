import serial                                               # import pySerial module
import time                                                 # import time module
import tkinter as tk                                        # import tkinter module
import matplotlib.pyplot as plt                             # import Matplotlib module, voor het plotten van grafieken
import os.path
import matplotlib.animation as animation

import serial.tools.list_ports                              # import Serial module, voor het aansturen van de arduino
from tkinter import *
from tkinter import messagebox

Ports= []
ToegewezenPorts = {}
Henk = 0


# ----------------------------------------------------------- Functies -------------------------------------------------------
# Kijkt welke ports allemaal gebruikt worden //Autheur Ries Bezemer
def GetPorts():
    print("Ports aan het scannen...\nEen moment geduld alstublieft...")
    ports = serial.tools.list_ports.comports(include_links=False)
    for port, desc, name in sorted(ports):
        if (desc.split(' ', 1)[0] == "Serieel"):  # Filtert de bluetooth ComPorts
            Ports.append(port)  # Voegt de ports toe aan een list voor de drop down menu
            print("Er is een bedieningseenheid aangesloten op: "+port)
    if(Ports.__len__()==0):
        print("Er zijn geen bedieningseenheden aangesloten")

# -----------------------------------------------Classes-------------------------------------------------------------------------
class BedieningsEenheid(Frame):
        # De constructor van de classe //Autheur Ries Bezemer
    def __init__(self,frame,i):
        self.frame = frame
        self.eenheid = i + 1
        self.BedPaneel()
        self.poort = 'COM3'
        self.MaxUitrol = 35
        self.ComPort = ''
        self.fig = plt.figure()
        self.ax1 = self.fig.add_subplot(1, 1, 1)

    def GetData(self,sensor):
        import serial, time
        ComPort = serial.Serial(self.poort)  # open the COM Port
        ComPort.baudrate = 19200  # set Baud rate to 9600
        ComPort.bytesize = 8  # Number of data bits = 8
        ComPort.parity = 'N'  # No parity
        ComPort.stopbits = 1  # Number of Stop bits = 1
        # Schrijft data naar de poort
        sensor = str(sensor)
        #print("Data wordt verzonden...")
        time.sleep(1.58)
        ComPort.write(sensor.encode())
        # Leest de data van de poort
        time.sleep(0.5)
        out = ""
        while ComPort.inWaiting() > 0:
            # print(ComPort.in_waiting)
            out += ComPort.read(1).decode(errors='ignore')
            print(out)
        # Sluit de seriele connectie af
        ComPort.close()  # Close the C/OM Port
        return(out)

        # Haalt data op van de sensor, zet de waardes vervolgens in een txt file //Autheur Ries Bezemer
    def GetGrafiekData(self,sensor):
        AantalCrash = 0
        #print("Grafiek Data wordt opgehaald")
        data = self.GetData(4)
        #print("De ontvangen data is:"+data)
        BestandNaam = "Besturingseenheid" + str(self.eenheid) + "Grafiek.txt"
        if(os.path.isfile(BestandNaam)):
            file = open(BestandNaam, 'r').read()
            file.rstrip("\n")
            lines = file.split(':')
            x = lines.__len__()
        else: x = 0
        if(data != ""): # Vangt een crash op waar de arduino geen waarde terug geeft
            waarde = str(x)+','+data+':'
            lines.append(waarde)
            print("De waarde die naar de grafiek moet: "+waarde)
            file = open(BestandNaam, 'a')
            file.write(lines[x])  # could be any text, appended @ the end of file
        else:
            AantalCrash = AantalCrash + 1
            print(str(AantalCrash)+" Crashes opgevangen")

        # Tekent een grafiek //Autheur: sentdex op Youtube
    def animate(self, i):
        print("De Grafiek wordt geüpdated")
        BestandNaam = "Besturingseenheid" + str(self.eenheid) + "Grafiek.txt"
        self.GetGrafiekData(4)
        file = open(BestandNaam, 'r').read()
        lines = file.split(':')
        xs = []
        ys = []
        for line in lines:
            if len(line) > 1:
                x, y = line.split(',')
                xs.append(float(x))
                ys.append(float(y))
        self.ax1.clear()
        self.ax1.plot(xs, ys)

        # Doet het zonnescherm omhoog //Autheur Ries Bezemer
    def omhoog(self):
        print("Besturingseenheid " + str(self.eenheid) + " wordt omhoog gedaan")
        print("Een moment geduld alstublieft...")

        # Doet het zonnescherm omlaag //Autheur Ries Bezemer
    def omlaag(self):
        print("Besturingseenheid " + str(self.eenheid) + " wordt omlaag gedaan")
        print("Een moment geduld alstublieft...")

        # Drukt een grafiek af //Autheur Ries Bezemer
    def grafiek(self):
        print("De grafiek voor besturingseenheid " + str(self.eenheid) + " wordt getekend")
        ani = animation.FuncAnimation(self.fig, self.animate, interval=1)
        plt.show()

        # Stelt de poort van de bedieningseenheid in //Autheur Ries Bezemer
    def SetPoort(self,waarde):
        # Kijkt of de poort al is toegewezen aan een andere bedieningseenheid
        if(waarde != self.poort):
            if waarde in ToegewezenPorts:
                # Als de poort al is toegewezen dan wordt er om een confirmatie gevraagd
                print("De Poort die u probeert toe te wijzen is al aan een andere eenheid toegewezen")
                if messagebox.askyesno('Let op!', 'De poort die u probeert toe te wijzen is al in gebuik,\nWilt u alsnog deze poort instellen?'):
                    self.poort = waarde
                    print("De COMport van bedieningseenheid " + str(self.eenheid) + " is op " + str(self.poort) + " gezet")
                    ToegewezenPorts[waarde] = self.eenheid
                else:
                    print("Poort "+str(waarde)+" wordt niet aan bedieningseenheid "+str(self.eenheid)+" toegevoegd")
            # Als de poort niet toegewezen is dan wordt hij zonder confirmatie toegewezen
            else:
                self.poort = waarde
                print("De COMport van bedieningseenheid " + str(self.eenheid) + " is op " + str(self.poort) + " gezet")
                ToegewezenPorts[waarde] = self.eenheid

        # Stelt de maximale uitrolstand in //Autheur Ries Bezemer
    def InvoerWaarde(self,waarde,eenheid):
        self.MaxUitrol = waarde
        print("De maximale uitrolwaarde voor bedieningseenheid "+str(eenheid)+" is: "+str(waarde))

        # Drukt de knoppen van de bedieningseenheid af //Autheur Ries Bezemer
    def BedPaneel(self):
        frame = tk.Frame(self.frame, highlightbackground="black",highlightthickness=1)  # zet een frame in elkaar voor de knoppen
        frame.pack()
        label = Label(frame, text="Besturingseenheid " + str(self.eenheid)) # Geeft een label aan de frame
        label.pack()
        # Selecteer COM port

        variable = StringVar(self.frame)
        variable.set("Selecteer een poort")

        Menu = tk.OptionMenu(frame,variable,*Ports,command=self.SetPoort)
        Menu.pack(side=tk.TOP)

        # Knop voor omhoog
        button = tk.Button(frame,
                           text="Omhoog",
                           fg="black", bg="white",
                           command=lambda: self.omhoog(), height=2, width=12, overrelief=RIDGE, cursor="hand2")
        button.pack(side=tk.TOP)
        # Knop voor omlaag
        button = tk.Button(frame,
                           text="Omlaag",
                           fg="black", bg="white",
                           command=lambda: self.omlaag(), height=2, width=12, overrelief=RIDGE, cursor="hand2")
        button.pack(side=tk.TOP)
        # Knop voor grafiek
        button = tk.Button(frame,
                           text="Grafiek",
                           fg="black", bg="white",
                           command=lambda: self.grafiek(), height=2, width=12, overrelief=RIDGE, cursor="hand2")
        button.pack(side=tk.TOP)  # zorgt ervoor dat alle knoppen onder elkaar staan
        # Invoer voor maximale uitrolstand
        invoer = Entry(frame)
        invoer.pack(side=tk.LEFT)
        button = tk.Button(frame, text='Verstuur', command=lambda : self.InvoerWaarde(invoer.get(),self.eenheid))
        button.pack(side=tk.LEFT)

        frame.pack(side=tk.LEFT)  # zorgt ervoor dat alle frames naast elkaar komen

# ------------------------------------------------Buildup van gui //Autheur Ries Bezemer -----------------------------------------
print("Een moment geduld het programma wordt opgestart...")
GetPorts()
if (Ports.__len__() > 0):
    root = tk.Tk()
    root.title("Centrale Project Embedded Systems")
    label = tk.Label(root, fg="dark green")
    label.pack()
    label.config(text="Centrale Project Embedded Systems")
    i = 0
    e = Ports.__len__() #maakt voor elke bordje die aangesloten is een bedienings paneel
    while(i < int(e)):
        app = BedieningsEenheid(root, i) #Start de knoppen op.
        i = i + 1
    tk.mainloop()
else:
    Fout = tk.Tk()      #Zorgt ervoor dat er geen leeg windows komt als er een fout melding wordt opgedaan
    Fout.withdraw()
    messagebox.showerror("Let Op!", "U heeft geen bedieningseenheid aangesloten\nSluit een bordje aan en probeer het opnieuw!")
#------------------------------------------------------------Tekst //Autheur Ries Bezemer -------------------------------------------------
#Tekst = "Project Leden:\nKarel Koster\nMatteo Geertsema\nMark de Vries\nRies Bezemer"
#msg = tk.Message(root, text = Tekst)
#msg.config(bg='White', font=('Arial', 14))
#msg.pack()
