import cv2
from adafruit_servokit import ServoKit

# Define servo pins (replace with your actual pin numbers)
servo_pan_pin = 17
servo_tilt_pin = 27

# Initialize ServoKit and servos
kit = ServoKit(channels=16)
servo_pan = kit.servo[0]
servo_tilt = kit.servo[1]

"""
... Rest of the gstreamer_pipeline function remains the same ...
"""

def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1920,
    capture_height=1080,
    display_width=960,
    display_height=540,
    framerate=30,
    flip_method=0,
):
    return (
        "nvarguscamerasrc sensor-id=%d ! "
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )


def face_detect():
    window_title = "Face Detect"
    face_cascade = cv2.CascadeClassifier(
        "/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml"
    )
    video_capture = cv2.VideoCapture(gstreamer_pipeline(flip_method=2), cv2.CAP_GSTREAMER)
    if video_capture.isOpened():
        try:
            cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)
            while True:
                ret, frame = video_capture.read()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)

                center_x = 0
                center_y = 0
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

                    center_x = int(x + w / 2)
                    center_y = int(y + h / 2)

                    # Calculate servo angles based on center position
                    pan_angle = map_range(center_x, 0, frame.shape[1], 0, 180)
                    tilt_angle = map_range(center_y, 0, frame.shape[0], 0, 180)

                    # Set servo positions
                    servo_pan.angle = pan_angle
                    servo_tilt.angle = tilt_angle

                    print(f"Center: ({center_x}, {center_y}) - Pan: {pan_angle}, Tilt: {tilt_angle}")

                # Check for window closing
                if cv2.getWindowProperty(window_title, cv2.WND_PROP_AUTOSIZE) >= 0:
                    cv2.imshow(window_title, frame)
                else:
                    break

                # Check for exit key
                keyCode = cv2.waitKey(10) & 0xFF
                if keyCode == 27 or keyCode == ord("q"):
                    break

        finally:
            video_capture.release()
            cv2.destroyAllWindows()
    else:
        print("Unable to open camera")


def map_range(value, in_min, in_max, out_min, out_max):
    """Maps a value from one range to another."""
    return int((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


if __name__ == "__main__":
    face_detect()