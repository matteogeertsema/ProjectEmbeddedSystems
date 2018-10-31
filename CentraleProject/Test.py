import serial                    # import pySerial module
# Setup voor Serial Connectie
com = 'COM3'
print(com+" wordt opgestart...")
ComPort = serial.Serial(com)  # open the COM Port
ComPort.baudrate = 9600          # set Baud rate to 9600
ComPort.bytesize = 8             # Number of data bits = 8
ComPort.parity   = 'N'           # No parity
ComPort.stopbits = 1             # Number of Stop bits = 1

# Schrijft data naar de poort
input = bytearray(b'A')
No = ComPort.write(input)
print("Data has been send...")

# Leest de data van de poort
print("Waiting for returning data...")
output = ComPort.readline()        # Wait and read data
print(output)

# Sluit de seriele connectie af
print("Port "+com+" wordt afgesloten!")
ComPort.close()                  # Close the COM Port