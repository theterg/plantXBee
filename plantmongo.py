from pymongo.connection import Connection
import time

class plantmongo:
    def __init__(self, addr, user="plant", password="plant"):
        self.addr = addr
        self.user = user
        self.password = password
        self.conn = Connection(addr)
        self.db = conn.plant
        if not db.authenticate("plant","plant"):
            print "unable to authenticate to mongodb"
            self.connected = False
            return None
        self.coll = self.db.test

    def publish(self, xbeeobj):
        post = {"time": time.time(),
                "temp": xbeeobj.temp,
                "moisture": xbeeobj.moisture,
                "dewpoint": xbeeobj.dewpoint,
                "pressure": xbeeobj.pressure,
                "light": xbeeobj.light,
                "batt": xbeeobj.batt,
                "rssi": xbeeobj.rssi}
        self.coll.save(post)

    def close(self):
        self.conn.disconnect()
