import RPi.GPIO as GPIO
from time import sleep

# Suppress GPIO warning messages
GPIO.setwarnings(False)

# Set the GPIO mode and define pins connected to the SG90 servo signal wires
GPIO.setmode(GPIO.BCM)

servo_pins = {
    1: 17,   # M0   
    2: 27,   # M2 
    3: 22,   # M3    
    4: 23,   # M4   
    5: 24    # M5    
}

# Initialize PWM objects for each servo
pwm_objects = {}
for pin in servo_pins.values():
    GPIO.setup(pin, GPIO.OUT)
    pwm_objects[pin] = GPIO.PWM(pin, 50)  # PWM frequency 50Hz
    pwm_objects[pin].start(0)  # Start PWM with 0% duty cycle

# Map the angle range (0-180 degrees) to the PWM duty cycle range (2-12)
angle_min = 0
angle_max = 180
duty_min = 2
duty_max = 12

# Define motor ranges (min and max angles)
motor_ranges = {
    1: (50, 110),    # M1   Jaw
    2: (0, 100),     # M2 
    3: (90, 160),     # M3    
    4: (70, 150),     # M4   
    5: (0, 180)     # M5    
}

# Function to set angle for a servo
def setAngle(angle, motor):
    try:
        min_angle, max_angle = motor_ranges[motor]
        # Ensure the angle is within the specified range
        angle = max(min_angle, min(max_angle, angle))
        # Map the angle to the PWM duty cycle range
        duty_cycle = (angle / angle_max) * (duty_max - duty_min) + duty_min
        pwm = pwm_objects[servo_pins[motor]]
        pwm.ChangeDutyCycle(duty_cycle)
        print(f"Servo {motor} turns {angle} deg")
    except ValueError:
        print(f"Invalid angle for Motor {motor}. Please enter a valid angle within the specified range.")

        sleep(step_delay)

# Function to control hand movement
def roboarm(angle1, angle2, angle3, angle4, angle5):
    setAngle(angle1, 1)   # M1   
    setAngle(angle2, 2)   # M2 
    setAngle(angle3, 3)   # M3    
    setAngle(angle4, 4)   # M4   
    setAngle(angle5, 5)   # M5    

# Dictionary of robot postures
robopostures = {
    "pos1": [(55,  100,  90,  90,  0),    
             (55,  100,  90,   90,  130), #go towards position
             
             (55,   65, 135,  80,  130),  # towards dwon to pick object
             (110,  65,  135,  80,  130), # jaw close, pick object
             (110,  100, 90,  90,  130),  # move towards upwards  
             
             (110,  100,  90,  90,  0), # go towards dropping point  
             (110,  100, 130, 90,  0),  # go down for dropping objet
             (55,   100, 130, 90,  0),  # open jaw
             (110,  100, 90, 90,  0)],  #final location ready

    "pos2": [(55,  100,  90,  90,  0),    
             (55,  100,  90,   90,  105), #go towards position
             
             (55,   65, 150,  90,  105),  # towards dwon to pick object
             (110,  65,  150,  90,  105), # jaw close, pick object
             (110,  100, 90,  90,  105),  # move towards upwards  
             
             (110,  100,  90,  90,  0), # go towards dropping point  
             (110,  100, 130, 90,  0),  # go down for dropping objet
             (55,   100, 130, 90,  0),  # open jaw
             (110,  100, 90, 90,  0)],  #final location ready


    "pos3": [(55,  100,  90,  90,  0),    
             (55,  100,  90,   90,  75), #go towards position
             
             (55,   65, 150,  90,  75),  # towards dwon to pick object
             (110,  65,  150,  90,  75), # jaw close, pick object
             (110,  100, 90,  90,  75),  # move towards upwards  
             
             (110,  100,  90,  90,  0), # go towards dropping point  
             (110,  100, 130, 90,  0),  # go down for dropping objet
             (55,   100, 130, 90,  0),  # open jaw
             (110,  100, 90, 90,  0)],  #final location ready
    
    
    "pos4": [(55,  100,  90,  90,  0),    
             (55,  100,  90,   90,  55), #go towards position
             (55,   50, 140,  80,  55),  # towards dwon to pick object
             (110,  50,  140,  80,  55), # jaw close, pick object
             (110,  100, 90,  90,  55),  # move towards upwards 
             (110,  100,  90,  90,  0), # go towards dropping point  
             (110,  100, 130, 90,  0),  # go down for dropping objet
             (55,   100, 130, 90,  0),  # open jaw
             (110,  100, 90, 90,  0)],  #final location ready

    "pos5": [(55,  100,  90,  90,  0),    
             (55,  60,   170,  120,  150), #go towards position
             (55,   60,  170, 95,  150),  # towards dwon to pick object
             (110,  60,  170, 95,  150), # jaw close, pick object
             (110,  60,  170,  120,  150),  # move towards upwards 
             (110,  60,  170,  120,  0), # go towards dropping point  
             (110,  100, 130, 90,  0),  # go down for dropping objet
             (55,   100, 130, 90,  0),  # open jaw
             (110,  100, 90, 90,  0)], #final location ready




    "pos6": [(55,  100,  90,  90,  0),    
             (55,  60,   170,  120,  35), #go towards position
             (55,   60,  170, 95,  35),  # towards dwon to pick object
             (110,  60,  170, 95,  35), # jaw close, pick object
             (110,  60,  170,  120,  35),  # move towards upwards 
             (110,  60,  170,  120,  0), # go towards dropping point  
             (110,  100, 130, 90,  0),  # go down for dropping objet
             (55,   100, 130, 90,  0),  # open jaw
             (110,  100, 90, 90,  0)] #final location ready
}

# Loop to execute the movements for the specified posture
try:
    while True:
        try:
            selected_pos = int(input("Enter the position (1-6): "))
            posture_key = f"pos{selected_pos}"
            if posture_key in robopostures:
                print(f"Running pos {posture_key}...")
                for movement in robopostures[posture_key]:
                    roboarm(*movement[:5])  # Only take the first 5 angles
                    sleep(1)
                sleep(1)  # Delay between postures
            else:
                print("Invalid position. Please enter a number between 1 and 10.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

except KeyboardInterrupt:
    # Clean up GPIO resources
    for pwm in pwm_objects.values():
        pwm.stop()
    GPIO.cleanup()
