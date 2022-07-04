from mqtt import MQTTClient
import time
import ujson
import machine
import ssd1306
from machine import Pin
from machine import I2C
from dht import DHT

def sub_cb(topic, msg):
   print(msg)

# MQTT Setup
client = MQTTClient('philip971234',
                    'mqtt.datacake.co',
                    user='9106070f315939e58e694fe49bc74360c72f38bf',
                    password='9106070f315939e58e694fe49bc74360c72f38bf',
                    port=1883)

client.set_callback(sub_cb)
client.connect()
print('connected')

#topics for datacake
ttemp = "dtck-pub/myheltec-2/59daf0d5-0e97-4b73-9a49-f1c355a0156c/TEMPERATURE"
thumid = "dtck-pub/myheltec-2/59daf0d5-0e97-4b73-9a49-f1c355a0156c/HUMIDITY"


# Start OLED
oled_width = 128
oled_height = 64
# Setup the I2C pins
i2c_scl = Pin('P4', mode=Pin.OUT, pull=Pin.PULL_UP)
i2c_sda = Pin('P3', mode=Pin.OUT, pull=Pin.PULL_UP)
i2c = I2C(0, I2C.MASTER, baudrate=100000, pins=(i2c_sda,i2c_scl))
time.sleep_ms(500)
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
oled.fill(0)

#start dht11
th = DHT(Pin('P23', mode=Pin.OPEN_DRAIN), 0)
time.sleep(2)

#main loop
while True:

    #sensor readings
    payload = th.read()
    while not payload.is_valid():
        time.sleep(10)
        payload = th.read()

    #oled screen print
    oled.fill(0)
    oled.text("Humidity {} %".format(payload.humidity), 0, 0)
    oled.text("Temp: {} C".format(payload.temperature), 0, 25)
    oled.show()

    #send data to the cloud
    client.publish(topic=ttemp, msg=str(payload.temperature))
    client.check_msg()
    client.publish(topic=thumid, msg=str(payload.humidity))
    client.check_msg()
    #time until next reading
    time.sleep(120)
