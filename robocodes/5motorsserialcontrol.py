import RPi.GPIO as GPIO
import time

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Set pin numbers for the servo motors
servo_pins = [17, 27, 22, 23, 24]

# Initialize PWM instances for each motor
pwms = []
for pin in servo_pins:
    GPIO.setup(pin, GPIO.OUT)
    pwm = GPIO.PWM(pin, 50)  # 50 Hz (20 ms PWM period)
    pwm.start(0)
    pwms.append(pwm)

def set_angle(pwm, angle):
    duty = angle / 18 + 2
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    pwm.ChangeDutyCycle(0)

try:
    while True:
        motor = input("Select motor (1 to 5): ")
        motor = int(motor)
        if 1 <= motor <= 5:
            angle = input("Enter desired angle (0 to 180) for motor {}: ".format(motor))
            angle = int(angle)
            if 0 <= angle <= 180:
                set_angle(pwms[motor - 1], angle)
            else:
                print("Angle must be between 0 and 180 degrees.")
        else:
            print("Invalid motor selection. Please select a motor between 1 and 5.")

except KeyboardInterrupt:
    # Clean up
    for pwm in pwms:
        pwm.stop()
    GPIO.cleanup()
