import serial                                               # import pySerial module
import time                                                 # import time module
import tkinter as tk                                        # import tkinter module
from tkinter import *
import serial.tools.list_ports                              # import list_port van de serial module

Ports= []

def StartCom():
    # Setup voor Serial Connectie
    com = 'COM3'  # Slaat de COM Port op in een variable
    print(com + " wordt opgestart...")
    ComPort = serial.Serial(com)  # open the COM Port
    print("Checking ComPort: " + ComPort.name)  # Checkt of de COM Port goed is ingesteld
    ComPort.baudrate = 9600  # set Baud rate to 9600
    ComPort.bytesize = 8  # Number of data bits = 8
    ComPort.parity = 'N'  # No parity
    ComPort.stopbits = 1  # Number of Stop bits = 1

    # Schrijft data naar de poort
    print("Checking if port is open: " + str(ComPort.is_open))  # Checkt of de compoNMKrt open staat
    input = bytearray(b'Test')  # Input naar de arduino in een variabele
    ComPort.write(input)  # Schrijft de waardes naar de arduino
    print("Data wordt verzonden...")

    # Leest de data van de poort
    print("Waiting for returning data...")
    output = ComPort.readline()  # Wait and read data
    print(output)  # Drukt de output af

    # Sluit de seriele connectie af
    print("Port " + com + " wordt afgesloten!")
    ComPort.close()  # Close the C/OM Port

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

# ------------------------------------------------Classes-------------------------------------------------------------------------
class BedieningsEenheid(Frame):
        # De constructor van de classe //Autheur Ries Bezemer
    def __init__(self,frame,i):
        self.frame = frame
        self.eenheid = i + 1
        self.BedPaneel()
        self.poort = ''
        self.MaxUitrol = 160

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
        Grafiek = tk.Tk()
        Grafiek.title("Grafiek besturingseenheid " + str(self.eenheid))
        fgrafiek = tk.Frame(Grafiek)
        fgrafiek.pack()

        # Button om de grafiek af te sluiten
        button = tk.Button(fgrafiek,
                           text="QUIT",
                           fg="red",
                           command=Grafiek.destroy)
        button.pack(side=tk.LEFT)

        # Stelt de poort van de bedieningseenheid in //Autheur Ries Bezemer
    def SetPoort(self,waarde):
        self.poort = waarde
        print("De COMport van bedieningseenheid "+str(self.eenheid)+" is op "+str(self.poort)+" gezet")

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

#------------------------------------------------------------Tekst //Autheur Ries Bezemer -------------------------------------------------
#Tekst = "Project Leden:\nKarel Koster\nMatteo Geertsema\nMark de Vries\nRies Bezemer"
#msg = tk.Message(root, text = Tekst)
#msg.config(bg='White', font=('Arial', 14))
#msg.pack()
tk.mainloop()