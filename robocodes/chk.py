import RPi.GPIO as GPIO
import time

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Set the pin number for the servo motor

import RPi.GPIO as GPIO
import time

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Set pin 17 as output
servo_pin = 23
GPIO.setup(servo_pin, GPIO.OUT)

# Create PWM instance
pwm = GPIO.PWM(servo_pin, 50)  # 50 Hz (20 ms PWM period)

# Initialize PWM
pwm.start(0)

def set_angle(angle):
    duty = angle / 18 + 2
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(servo_pin, False)
    pwm.ChangeDutyCycle(0)

try:
    while True:
        angle = input("Enter desired angle (0 to 180): ")
        angle = int(angle)
        if 0 <= angle <= 180:
            set_angle(angle)
        else:
            print("Angle must be between 0 and 180 degrees.")

except KeyboardInterrupt:
    # Clean up
    pwm.stop()
    GPIO.cleanup()
