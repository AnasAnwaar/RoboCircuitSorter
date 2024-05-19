import RPi.GPIO as GPIO
from time import sleep

# Suppress GPIO warning messages
GPIO.setwarnings(False)

# Set the GPIO mode and define pins connected to the SG90 servo signal wires
GPIO.setmode(GPIO.BCM)

servo_pins = {
    1: 17,   # M1   
    2: 5,   # M2 
    3: 6,   # M3    
    4: 16,   # M4   
    5: 26    # M5    
}

# Initialize PWM objects for each servo
pwm_objects = {}
for pin in servo_pins.values():
    GPIO.setup(pin, GPIO.OUT)
    pwm_objects[pin] = GPIO.PWM(pin, 40)  # PWM frequency 50Hz
    pwm_objects[pin].start(0)  # Start PWM with 0% duty cycle

# Map the angle range (0-180 degrees) to the PWM duty cycle range (2-12)
angle_min = 0
angle_max = 180
duty_min = 2
duty_max = 10

# Define motor ranges (min and max angles)
motor_ranges = {
    1: (0, 180),    # M1   
    2: (0, 180),     # M2 
    3: (0, 180),     # M3    
    4: (0, 180),     # M4   
    5: (0, 180)     # M5    
}

# Dictionary to store current angles
current_angles = {motor: 0 for motor in motor_ranges}

# Function to set angle for a servo with smoothness
def setAngleSmoothly(angle, motor):
    try:
        min_angle, max_angle = motor_ranges[motor]
        # Ensure the angle is within the specified range
        angle = max(min_angle, min(max_angle, angle))
        # Get current angle
        current_angle = current_angles[motor]
        # Smoothly move from current angle to desired angle
        duty_cycle = (angle / angle_max) * (duty_max - duty_min) + duty_min
        pwm_objects[servo_pins[motor]].ChangeDutyCycle(duty_cycle)
        current_angles[motor] = angle
        print(f"Servo {motor} turns {angle} deg smoothly")
    except ValueError:
        print(f"Invalid angle for Motor {motor}. Please enter a valid angle within the specified range.")

# Function to control hand movement with speed control
def roboarmSmoothly(angle1, angle2, angle3, angle4, angle5, speed=0.4):
    angles = [angle1, angle2, angle3, angle4, angle5]
    for i, angle in enumerate(angles):
        setAngleSmoothly(angle, i + 1)   # Motors are indexed from 1
        sleep(speed)

# Dictionary of robot postures
robopostures = {
    "pos1": [(0, 0, 90, 90, 180),  
             (30, 30, 90, 90, 180),  
             (60, 20, 90, 90, 180),
             (90, 30, 90, 90, 180)],

    # Define other postures here...
}

# Loop to execute the movements for the specified posture
try:
    while True:
        try:
            selected_pos = int(input("Enter the position (1-8): "))
            posture_key = f"pos{selected_pos}"
            if posture_key in robopostures:
                print(f"Running pos {posture_key}...")
                for movement in robopostures[posture_key]:
                    roboarmSmoothly(*movement[:5], speed=1)  # Adjust speed as needed
                    sleep(2)
                sleep(5)  # Delay between postures
            else:
                print("Invalid position. Please enter a number between 1 and 10.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

except KeyboardInterrupt:
    # Clean up GPIO resources
    for pwm in pwm_objects.values():
        pwm.stop()
    GPIO.cleanup()
