import serial                                               # import pySerial module
import time                                                 # import time module
import tkinter as tk                                        # import tkinter module

def write_slogan():
    print("Tkinter is easy to use!")

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
# Besturingseenheid 1
from tkinter import *
frame1 = tk.Frame(root, highlightbackground="black", highlightthickness=1)
frame1.pack()
label = Label(frame1, text="Besturingseenheid 1 ").pack()
# Knop voor omhoog
button = tk.Button(frame1,
                   text="Omhoog",
                   fg="black", bg="white",
                   command=lambda : omhoog(1), height=2, width=12,overrelief=RIDGE,cursor="hand2")
button.pack(side=tk.TOP)
# Knop voor omlaag
button = tk.Button(frame1,
                   text="Omlaag",
                   fg="black", bg="white",
                   command=lambda : omlaag(1), height=2, width=12,overrelief=RIDGE,cursor="hand2")
button.pack(side=tk.TOP)
#Knop voor grafiek
button = tk.Button(frame1,
                   text="Grafiek",
                   fg="black", bg="white",
                   command=lambda : grafiek(1), height=2, width=12,overrelief=RIDGE,cursor="hand2")
button.pack(side=tk.TOP)
frame1.pack(side=tk.LEFT)

# Besturingseenheid 2
frame2 = tk.Frame(root,highlightbackground="black", highlightthickness=1)
frame2.pack()
label = Label(frame2, text="Besturingseenheid 2 ").pack()
# Knop voor omhoog
button = tk.Button(frame2,
                   text="Omhoog",
                   fg="black", bg="white",
                   command=lambda : omhoog(2), height=2, width=12,overrelief=RIDGE,cursor="hand2")
button.pack(side=tk.TOP)
# Knop voor omlaag
button = tk.Button(frame2,
                   text="Omlaag",
                   fg="black", bg="white",
                   command=lambda : omlaag(2), height=2, width=12,overrelief=RIDGE,cursor="hand2")
button.pack(side=tk.TOP)
#Knop voor grafiek
button = tk.Button(frame2,
                   text="Grafiek",
                   fg="black", bg="white",
                   command=lambda : grafiek(2), height=2, width=12,overrelief=RIDGE,cursor="hand2")
button.pack(side=tk.TOP)
frame2.pack(side=tk.LEFT)

# Besturingseenheid 3
frame3 = tk.Frame(root,highlightbackground="black", highlightthickness=1)
frame3.pack()
label = Label(frame3, text="Besturingseenheid 3 ").pack()
# Knop voor omhoog
button = tk.Button(frame3,
                   text="Omhoog",
                   fg="black", bg="white",
                   command=lambda : omhoog(3), height=2, width=12,overrelief=RIDGE,cursor="hand2")
button.pack(side=tk.TOP)
# Knop voor omlaag
button = tk.Button(frame3,
                   text="Omlaag",
                   fg="black", bg="white",
                   command=lambda : omlaag(3), height=2, width=12,overrelief=RIDGE,cursor="hand2")
button.pack(side=tk.TOP)
#Knop voor grafiek
button = tk.Button(frame3,
                   text="Grafiek",
                   fg="black", bg="white",
                   command=lambda : grafiek(3), height=2, width=12,overrelief=RIDGE,cursor="hand2")
button.pack(side=tk.TOP)
frame3.pack(side=tk.LEFT)

# Besturingseenheid 4
frame4 = tk.Frame(root,highlightbackground="black", highlightthickness=1)
frame4.pack()
label = Label(frame4, text="Besturingseenheid 4 ").pack()
# Knop voor omhoog
button = tk.Button(frame4,
                   text="Omhoog",
                   fg="black", bg="white",
                   command=lambda : omhoog(3), height=2, width=12,overrelief=RIDGE,cursor="hand2")
button.pack(side=tk.TOP)
# Knop voor omlaag
button = tk.Button(frame4,
                   text="Omlaag",
                   fg="black", bg="white",
                   command=lambda : omlaag(3), height=2, width=12,overrelief=RIDGE,cursor="hand2")
button.pack(side=tk.TOP)
#Knop voor grafiek
button = tk.Button(frame4,
                   text="Grafiek",
                   fg="black", bg="white",
                   command=lambda : grafiek(4), height=2, width=12,overrelief=RIDGE,cursor="hand2")
button.pack(side=tk.TOP)
frame4.pack(side=tk.LEFT)

# Besturingseenheid 5
frame5 = tk.Frame(root,highlightbackground="black", highlightthickness=1)
frame5.pack()
label = Label(frame5, text="Besturingseenheid 5 ").pack()
# Knop voor omhoog
button = tk.Button(frame5,
                   text="Omhoog",
                   fg="black", bg="white",
                   command=lambda : omhoog(3), height=2, width=12,overrelief=RIDGE,cursor="hand2")
button.pack(side=tk.TOP)
# Knop voor omlaag
button = tk.Button(frame5,
                   text="Omlaag",
                   fg="black", bg="white",
                   command=lambda : omlaag(3), height=2, width=12,overrelief=RIDGE,cursor="hand2")
button.pack(side=tk.TOP)
#Knop voor grafiek
button = tk.Button(frame5,
                   text="Grafiek",
                   fg="black", bg="white",
                   command=lambda : grafiek(5), height=2, width=12,overrelief=RIDGE,cursor="hand2")
button.pack(side=tk.TOP)
frame5.pack(side=tk.LEFT)
#------------------------------------------------------------Tekst-----------------------------------------------------------------
Tekst = "Project Leden:\nKarel Koster\nMatteo Geertsema\nMark de Vries\nRies Bezemer"
msg = tk.Message(root, text = Tekst)
msg.config(bg='White', font=('Arial', 14))
msg.pack()
tk.mainloop()