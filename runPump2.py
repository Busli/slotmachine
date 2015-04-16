import time
import serial

ser = serial.Serial('/dev/ttyACM0', 9600)

ser.write("34")

while True:
    time.sleep(1)
    print("waiting for value")
    value = ser.readline()
    print(value)


ser.close()
