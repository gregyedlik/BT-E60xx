import serial
import time
import pickle

ser = serial.Serial("/dev/tty.usbserial-A50285BI", baudrate=9600, parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0)

file = open('startup_pickle', 'rb')
startup = pickle.load(file)
file.close()

start = time.time()
beginning = time.time()


def print_batch(batch2print):
    time_spent = time.time() - beginning
    list_of_bytes = [b['byte'] for b in batch2print]
    concatbytes = list_of_bytes[0]
    for b in list_of_bytes[1:]:
        concatbytes += b
    print('TX\t' + f'{time_spent:.2f}' + '\t' + str(concatbytes))


def listen():
    time_spent = time.time() - beginning
    rx = ser.readline()
    print('RX\t' + f'{time_spent:.2f}' + '\t' + str(rx))


for batch in startup:
    for rec in batch:
        while time.time() - start < rec['time'] - startup[0][0]['time']:
            time.sleep(0.001)
        ser.write(rec['byte'])
    print_batch(batch)
    listen()

print('Startup done')

while 1:
    start = time.time() - startup[-4][0]['time']
    for batch in startup[-4:]:
        for rec in batch:
            while time.time() - start < rec['time']:
                time.sleep(0.001)
            ser.write(rec['byte'])
        print_batch(batch)
        listen()
