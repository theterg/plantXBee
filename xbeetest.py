import serial
import time
from xbee import XBee

class xbeetest:
    def upload(self):
        self.fd.write(str(time.time() - self.starttime)+','+\
               str(self.temp)+','+\
               str(self.moisture)+','+\
               str(self.humidity)+','+\
               str(self.dewpoint)+','+\
               str(self.pressure)+','+\
               str(self.light)+','+\
               str(self.batt)+','+\
               str(self.rssi)+',\r\n')
        self.fd.flush()
    def parse(self, data):
        self.rssi = ord(data['rssi'])
        self.addr = data['source_addr']
        if data['id'] == 'rx':
            weather = data['rf_data'].split(',')
            if weather[0].find('RESET') != -1:
                return;
            try:
                self.temp = float(weather[1])
                self.humidity = int(weather[2])
                self.dewpoint = float(weather[3])
                self.pressure = float(weather[4])
                self.light = float(weather[5])
                self.batt = float(weather[6])
            except ValueError:
                return
            self.upload()
        elif data['id'] == 'rx_io_data':
            self.moisture = data['samples'][0]['adc-0']
    def __init__(self, port, baud):
        self.fd = open('logfile.csv','w')
        self.fd.write('time,temp,moisture,humidity,dewpoint,pressure,light'\
                ',batt,rssi,\r\n')
        self.moisture = -1
        self.temp = 0.0
        self.humidity = -1
        self.dewpoint = 0.0
        self.pressure = 0.0
        self.light = 0.0
        self.batt = 0.0
        self.rssi = 0
        self.addr = ""
        self.ser = serial.Serial(port, baud)
        self.xbee = XBee(self.ser, callback=self.parse)
        self.starttime = time.time()
    def close(self):
        self.xbee.halt()
        self.ser.close()

if __name__ == '__main__':
    xbt = xbeetest('/dev/ttyUSB0',9600)
    while True:
        try:
            time.sleep(0.5)
        except KeyboardInterrupt:
            break
    xbt.close()
