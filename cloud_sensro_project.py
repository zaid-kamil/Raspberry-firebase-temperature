import Adafruit_DHT
import time
import datetime as dt
import firebase_admin as fa
from firebase_admin import auth
from firebase_admin import firestore as fire

print("Connecting to Firebase cloud")
cred = fa.credentials.Certificate("service.json")
app = fa.initialize_app(cred)
print("Connection established")
# print(cred)
# print(app)

def collect(p = 4, s=Adafruit_DHT.DHT11,delay=3):
    while True:
        h, t = Adafruit_DHT.read_retry(s,p)
        if h is not None and t is not None:
            tf = t*9/5.0+32
            print(f"Temp:{t:.1f}C({tf:.1f}F), Humidity:{h}%")
            saveToCloud(t,h)
        else:
            print("Sensor failed to load data! check wiring")
        time.sleep(delay)
        print(".", end='')

def saveToCloud(t, h):
    path = '/dht11'
    print("Uploading to Firebase")
    nw=dt.datetime.now()
    currtime = nw.strftime("%Y-%m-%d %H:%M:%S")
    db = fire.client()
    db.collection('dht11').document(str(int(dt.datetime.timestamp(nw)))).set({
        'device': 'DP-Rpi-005',
        'humidity': h,
        'temperature': t,
        'created_at': currtime,
        'timestamp': dt.datetime.timestamp(nw)
        })
    print("Uploading complete")

if __name__ == "__main__":
    
    collect(delay=60)