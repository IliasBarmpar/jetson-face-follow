import cv2

# Replace with the correct sensor ID for your camera
sensor_id = 0

# Configure camera resolution and framerate (optional)
width = 640
height = 480
framerate = 30

# Create a VideoCapture object
cap = cv2.VideoCapture("nvarguscamerasrc sensor_id=%d ! video/x-raw(memory:NVMM), width=%d, height=%d, framerate=%d/1 ! nvvidconv flip-method=0 ! appsink" % (sensor_id, width, height, framerate))

if not cap.isOpened():
    print("Error opening camera")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Check if frame is read correctly
    if not ret:
        print("Can't receive frame (stream end?). Exiting...")
        break

    # Display the frame
    cv2.imshow('Camera', frame)

    # Press 'q' to quit
    if cv2.waitKey(1) == ord('q'):
        break

# Release the capture and close all windows
cap.release()
cv2.destroyAllWindows()