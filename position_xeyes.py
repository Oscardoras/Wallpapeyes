# ~/scripts/position_xeyes.py
import sys
import cv2
import subprocess


res = subprocess.check_output("xrandr | grep '*' | awk '{print $1}'", shell=True).decode().strip()
screen_w, screen_h = map(int, res.split('x'))
print(f"Screen: {screen_w}x{screen_h}")


img_path = sys.argv[1]
img = cv2.imread(img_path)
img_h, img_w = img.shape[:2]
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
    eye_x = sum(c[0] for c in centers) // len(centers)
    eye_y = sum(c[1] for c in centers) // len(centers)
else:
    eye_x, eye_y = centers[0]

print(eye_x, eye_y)


screen_ratio = screen_w / screen_h
image_ratio = img_w / img_h

if image_ratio > screen_ratio:
    # Image is "wider" than the screen → black bars on top/bottom
    scale = screen_w / img_w
    scaled_w = screen_w
    scaled_h = img_h * scale
    offset_x = 0
    offset_y = (screen_h - scaled_h) / 2
else:
    # Image is "taller" than the screen → black bars on sides
    scale = screen_h / img_h
    scaled_h = screen_h
    scaled_w = img_w * scale
    offset_y = 0
    offset_x = (screen_w - scaled_w) / 2

screen_eye_x = int(offset_x + eye_x * scale)
screen_eye_y = int(offset_y + eye_y * scale)

print(screen_eye_x, screen_eye_y)

# Move or launch xeyes to that position
# You can move xeyes with wmctrl or xdotool
subprocess.run(["xdotool", "search", "--name", "xeyes", "windowmove", str(screen_eye_x), str(screen_eye_y)])
