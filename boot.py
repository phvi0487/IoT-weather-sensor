import network
import time
# setup as a station
wlan = network.WLAN(mode=network.WLAN.STA)
wlan.connect('Villa Champagne', auth=(network.WLAN.WPA2, 'fordmustang1967'))
while not wlan.isconnected():
    time.sleep_ms(50)
print(wlan.ifconfig())

# now use socket as usual
