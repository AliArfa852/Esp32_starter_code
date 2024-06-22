import network

# Replace with your network credentials
SSID = 'Optix.194/A'
PASSWORD = 'optix2021'

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(SSID, PASSWORD)

while not station.isconnected():
    pass

print('Connection successful')
print(station.ifconfig())
