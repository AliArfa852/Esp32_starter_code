from machine import Pin, PWM
import time

# Define the GPIO pins for the servos
servo_pin1 = 12
servo_pin2 = 14

# Set up the PWM signals for the servos
# 50Hz corresponds to a 20ms period, typical for RC servos
servo1 = PWM(Pin(servo_pin1), freq=60)
servo2 = PWM(Pin(servo_pin2), freq=60)

# Function to set the angle of a servo
def set_angle(servo, angle):
    # Convert the angle to a duty cycle
    # The duty cycle for a servo typically ranges from 2.5% to 12.5%
    # which corresponds to 0.5ms to 2.5ms pulse width at 50Hz
    # Adjusting the range to fit 0-180 degrees:
    duty = int(40 + (angle / 180) * 80)
    servo.duty(duty)

# Sweep the servos back and forth
try:
    while True:
        # Sweep from 0 to 180 degrees
        for angle in range(0, 181, 1):
            set_angle(servo1, angle)
            set_angle(servo2, angle)
            time.sleep(0.03)  # Small delay between steps

        # Sweep from 180 to 0 degrees
        for angle in range(180, -1, -1):
            set_angle(servo1, angle)
            set_angle(servo2, angle)
            time.sleep(0.03)  # Small delay between steps

except KeyboardInterrupt:
    # Clean up on exit
    servo1.deinit()
    servo2.deinit()
