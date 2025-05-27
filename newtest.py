import cv2
from adafruit_servokit import ServoKit

# Initialize ServoKit and servos
kit = ServoKit(channels=16)
servo_pan = kit.servo[4]
servo_tilt = kit.servo[5]


import time
def test_servo():
    try:
        while True:
            print('hi')
            sweep = range(0,180)
            for degree in sweep :
                kit.servo[0].angle=degree
            time.sleep(0.5)    
            # # Move pan servo from 0 to 180 degrees
            # for angle in range(0, 181, 1):
            #     servo_pan.angle = angle
            #     time.sleep(0.01)  # Small delay to observe the movement
            
            # # Move pan servo from 180 to 0 degrees
            # for angle in range(180, -1, -1):
            #     servo_pan.angle = angle
            #     time.sleep(0.01)
            
            # # Move tilt servo from 0 to 180 degrees
            # for angle in range(0, 181, 1):
            #     servo_tilt.angle = angle
            #     time.sleep(0.01)
            
            # # Move tilt servo from 180 to 0 degrees
            # for angle in range(180, -1, -1):
            #     servo_tilt.angle = angle
            #     time.sleep(0.01)
    
    except KeyboardInterrupt:
        print("Test stopped by user")

if __name__ == "__main__":
    test_servo()