import socket
import machine

led = machine.Pin(2, machine.Pin.OUT)

# HTML to send to browsers
html = """<!DOCTYPE html>
<html>
<head>
    <title>ESP8266 LED Control</title>
</head>
<body>
    <h1>ESP8266 LED Control</h1>
    <button onclick="toggleLed('on')">Turn On</button>
    <button onclick="toggleLed('off')">Turn Off</button>
    <script>
        function toggleLed(state) {
            var xhr = new XMLHttpRequest();
            xhr.open("GET", "/" + state, true);
            xhr.send();
        }
    </script>
</body>
</html>
"""

# Setup the socket web server
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

print('Listening on', addr)

def handle_client(client):
    request = client.recv(1024)
    request = str(request)
    
    led_on = request.find('/on')
    led_off = request.find('/off')
    
    if led_on == 6:
        led.value(1)
    if led_off == 6:
        led.value(0)
    
    response = html
    client.send('HTTP/1.1 200 OK\n')
    client.send('Content-Type: text/html\n')
    client.send('Connection: close\n\n')
    client.sendall(response)
    client.close()

while True:
    client, addr = s.accept()
    print('Client connected from', addr)
    handle_client(client)
