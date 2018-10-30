import serial                    # import pySerial module
ComPort = serial.Serial('COM25') # open the COM Port

ComPort.setRTS(0)                # Make RTS pin low
#put some delay, or ask for input
ComPort.setRTS(1)                # Make RTS pin high

ComPort.setDTR(0)                # Make DTR pin low
#put some delay, or ask for input
ComPort.setDTR(1)                # Make DTR pin high

ComPort.close()                  # Close the COM Port