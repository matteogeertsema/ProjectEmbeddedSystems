import serial                    # import pySerial module
# Setup voor Serial Connectie
poort = input("ComPort: ")
print("U heeft poort "+poort+" geselecteerd")
ComPort = serial.Serial('COM3')   # open the COM Port
ComPort.baudrate = 9600          # set Baud rate to 9600
ComPort.bytesize = 8             # Number of data bits = 8
ComPort.parity   = 'N'           # No parity
ComPort.stopbits = 1             # Number of Stop bits = 1

# Schrijft data naar de poort
data = bytearray(b'A')
print("Schijft "+data+" naar port 3")
No = ComPort.write(data)

# Leest de data van de poort
data = ComPort.readline()        # Wait and read data
print(data)

# Sluit de seriele connectie af
print("De verbinding met"+poort+"wordt afgesloten")
ComPort.close()                  # Close the COM Port