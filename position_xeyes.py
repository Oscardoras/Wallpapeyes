# ~/scripts/position_xeyes.py
import sys
import cv2
import subprocess

img_path = sys.argv[1]
img = cv2.imread(img_path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

eye_cascade = cv2.CascadeClassifier('/usr/share/opencv4/haarcascades/haarcascade_eye.xml')
eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)

if len(eyes) == 0:
    print("Not found")
    sys.exit(0)

# Find the center of detected eyes
centers = [(x + w//2, y + h//2) for (x, y, w, h) in eyes]

# Example: if two eyes, average vertical position
if len(centers) >= 2:
    avg_x = sum(c[0] for c in centers) // len(centers)
    avg_y = sum(c[1] for c in centers) // len(centers)
else:
    avg_x, avg_y = centers[0]

print(avg_x, avg_y)

# Move or launch xeyes to that position
# You can move xeyes with wmctrl or xdotool
# subprocess.run(["xdotool", "search", "--name", "xeyes", "windowmove", str(avg_x), str(avg_y)])
