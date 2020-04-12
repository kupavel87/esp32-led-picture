try:
    import gc
    import usocket as socket
except:
    import socket

# import urequests as requests
import network
import machine

import esp
esp.osdebug(None)

gc.collect()

import settings

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(settings.ssid, settings.password)

while station.isconnected() == False:
    pass

print('Connection successful')
print(station.ifconfig())

import ntptime
ntptime.settime()

# import webrepl
# webrepl.start()

# try:
#     import uasyncio as asyncio
# except:
#     import upip
#     upip.install('micropython-uasyncio')
#     upip.install('micropython-uasyncio.synchro')
#     upip.install('micropython-uasyncio.queues')
# import ujson
# upip.install('micropython-logging')
