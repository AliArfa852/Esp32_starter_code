import network
import socket
from machine import Pin, PWM
import time

# Configuration for your WiFi network
SSID = 'KDD Lab'
PASSWORD = 'kdd$ec123'

# Setup the WiFi connection
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

# Wait for connection
while not wlan.isconnected():
    pass

print('Connected to WiFi. IP:', wlan.ifconfig()[0])

# Setup the L298 motor driver pins
IN1 = Pin(25, Pin.OUT)
IN2 = Pin(26, Pin.OUT)
EN_A = PWM(Pin(27), freq=1000)

IN3 = Pin(33, Pin.OUT)
IN4 = Pin(32, Pin.OUT)
EN_B = PWM(Pin(14), freq=1000)

# Setup the servos
servo1 = PWM(Pin(21), freq=50)
servo2 = PWM(Pin(22), freq=50)

# Function to set motor speed and direction
def set_motor(speed, direction, motor):
    speed = int(speed * 1023 / 100)  # Convert 0-100% speed to duty cycle (0-1023)
    if motor == 'A':
        EN_A.duty(speed)
        if direction == 'forward':
            IN1.value(1)
            IN2.value(0)
        elif direction == 'backward':
            IN1.value(0)
            IN2.value(1)
        elif direction == 'stop':
            IN1.value(0)
            IN2.value(0)
    elif motor == 'B':
        EN_B.duty(speed)
        if direction == 'forward':
            IN3.value(1)
            IN4.value(0)
        elif direction == 'backward':
            IN3.value(0)
            IN4.value(1)
        elif direction == 'stop':
            IN3.value(0)
            IN4.value(0)

# Function to set servo angle
def set_servo(servo, angle):
    min_duty = 40  # Minimum duty cycle for 0 degrees
    max_duty = 115  # Maximum duty cycle for 180 degrees
    duty = int(min_duty + (angle / 180) * (max_duty - min_duty))
    servo.duty(duty)


# Setup the web server
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

print('Listening on', addr)

# HTML for the web page
html = """<!DOCTYPE html>
<html>
<head>
    <title>ESP32 Car Control</title>
</head>
<body>
    <h1>ESP32 Car Control</h1>
    <button onclick="sendCommand('forwardA')">Motor A Forward</button>
    <button onclick="sendCommand('backwardA')">Motor A Backward</button>
    <button onclick="sendCommand('stopA')">Motor A Stop</button>
    <br>
    <button onclick="sendCommand('forwardB')">Motor B Forward</button>
    <button onclick="sendCommand('backwardB')">Motor B Backward</button>
    <button onclick="sendCommand('stopB')">Motor B Stop</button>
    <br>
    <label for="speedA">Motor A Speed:</label>
    <input type="range" id="speedA" name="speedA" min="0" max="100" onchange="sendSpeed('A', this.value)">
    <br>
    <label for="speedB">Motor B Speed:</label>
    <input type="range" id="speedB" name="speedB" min="0" max="100" onchange="sendSpeed('B', this.value)">
    <br>
    <label for="servo1">Servo 1 Angle:</label>
    <input type="range" id="servo1" name="servo1" min="0" max="180" onchange="sendServoCommand('servo1', this.value)">
    <br>
    <label for="servo2">Servo 2 Angle:</label>
    <input type="range" id="servo2" name="servo2" min="0" max="180" onchange="sendServoCommand('servo2', this.value)">
    <script>
        function sendCommand(cmd) {
            var xhttp = new XMLHttpRequest();
            xhttp.open("GET", "/" + cmd, true);
            xhttp.send();
        }
        function sendSpeed(motor, speed) {
            var xhttp = new XMLHttpRequest();
            xhttp.open("GET", "/speed" + motor + "?value=" + speed, true);
            xhttp.send();
        }
        function sendServoCommand(servo, angle) {
            var xhttp = new XMLHttpRequest();
            xhttp.open("GET", "/" + servo + "?angle=" + angle, true);
            xhttp.send();
        }
    </script>
</body>
</html>
"""

# Main loop to handle web requests
while True:
    cl, addr = s.accept()
    print('Client connected from', addr)
    request = cl.recv(1024).decode()
    print('Request:', request)
    
    if 'GET /forwardA' in request:
        set_motor(100, 'forward', 'A')
    elif 'GET /backwardA' in request:
        set_motor(100, 'backward', 'A')
    elif 'GET /stopA' in request:
        set_motor(0, 'stop', 'A')
    elif 'GET /forwardB' in request:
        set_motor(100, 'forward', 'B')
    elif 'GET /backwardB' in request:
        set_motor(100, 'backward', 'B')
    elif 'GET /stopB' in request:
        set_motor(0, 'stop', 'B')
    elif 'GET /speedA' in request:
        speed = int(request.split('value=')[1].split(' ')[0])
        set_motor(speed, 'forward', 'A')
    elif 'GET /speedB' in request:
        speed = int(request.split('value=')[1].split(' ')[0])
        set_motor(speed, 'forward', 'B')
    elif 'GET /servo1' in request:
        angle = int(request.split('angle=')[1].split(' ')[0])
        set_servo(servo1, angle)
    elif 'GET /servo2' in request:
        angle = int(request.split('angle=')[1].split(' ')[0])
        set_servo(servo2, angle)

    # Send the HTML response
    response = html
    cl.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n')
    cl.send(response)
    cl.close()
