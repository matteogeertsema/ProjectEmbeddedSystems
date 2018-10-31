import serial                                               # import pySerial module
import time                                                 # import time module
import tkinter as tk                                        # import tkinter module

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
    print("Checking if port is open: " + str(ComPort.is_open))  # Checkt of de comport open staat
    input = bytearray(b'Test')  # Input naar de arduino in een variabele
    ComPort.write(input)  # Schrijft de waardes naar de arduino
    print("Data has been send...")

    # Leest de data van de poort
    print("Waiting for returning data...")
    output = ComPort.readline()  # Wait and read data
    print(output)  # Drukt de output af

    # Sluit de seriele connectie af
    print("Port " + com + " wordt afgesloten!")
    ComPort.close()  # Close the C/OM Port

def omhoog(eenheid):
    print("Besturingseenheid "+str(eenheid)+" wordt omhoog gedaan")
    print("Een moment geduld alstublieft...")

def omlaag(eenheid):
    print("Besturingseenheid " + str(eenheid) + " wordt omlaag gedaan")
    print("Een moment geduld alstublieft...")

def grafiek(eenheid):
    print("De grafiek voor besturingseenheid "+str(eenheid)+" wordt getekend")
    Grafiek = tk.Tk()
    Grafiek.title("Grafiek besturingseenheid "+str(eenheid))
    fgrafiek = tk.Frame(Grafiek)
    fgrafiek.pack()

    # Button om de grafiek af te sluiten
    button = tk.Button(fgrafiek,
                       text="QUIT",
                       fg="red",
                       command=Grafiek.destroy)
    button.pack(side=tk.LEFT)

# ------------------------------------------------Buildup van gui-----------------------------------------------------------------------
root = tk.Tk()
root.title("Centrale Project Embedded Systems")

# label
label = tk.Label(root, fg="dark green")
label.pack()
label.config(text="Centrale Project Embedded Systems")

# ------------------------------------------------Knoppen per besturings eenheid---------------------------------------------------------
from tkinter import *
i = 0
e = 4 #Staat op 4 omdat wij als project groep 4 leden hebben en dus 4 bordjes
#e = input("Aantal besturingseenheden: ") # Voor developpment uitgecommend
while(i < int(e)):
    frame = tk.Frame(root, highlightbackground="black", highlightthickness=1) #zet een frame in elkaar voor de knoppen
    frame.pack()
    label = Label(frame, text="Besturingseenheid "+str(i+1)).pack() #geeft een label aan een frame
    # Knop voor omhoog
    button = tk.Button(frame,
                       text="Omhoog",
                       fg="black", bg="white",
                       command=lambda: omhoog(i), height=2, width=12, overrelief=RIDGE, cursor="hand2")
    button.pack(side=tk.TOP)
    # Knop voor omlaag
    button = tk.Button(frame,
                       text="Omlaag",
                       fg="black", bg="white",
                       command=lambda: omlaag(i), height=2, width=12, overrelief=RIDGE, cursor="hand2")
    button.pack(side=tk.TOP)
    # Knop voor grafiek
    button = tk.Button(frame,
                       text="Grafiek",
                       fg="black", bg="white",
                       command=lambda: grafiek(i), height=2, width=12, overrelief=RIDGE, cursor="hand2")
    button.pack(side=tk.TOP) #zorgt ervoor dat alle knoppen onder elkaar staan
    frame.pack(side=tk.LEFT) #zorgt ervoor dat alle frames naast elkaar komen
    i = i + 1

#------------------------------------------------------------Tekst-----------------------------------------------------------------
Tekst = "Project Leden:\nKarel Koster\nMatteo Geertsema\nMark de Vries\nRies Bezemer"
msg = tk.Message(root, text = Tekst)
msg.config(bg='White', font=('Arial', 14))
msg.pack()
tk.mainloop()