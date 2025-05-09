import cv2
import numpy as np
import sys
import json
import time  # To get current timestamp

def detect_balls(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise Exception(f"Failed to load image from path: {image_path}")

    output = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)

    circles = cv2.HoughCircles(
        gray,
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=30,
        param1=50,
        param2=20,
        minRadius=12,
        maxRadius=20
    )

    results = []

    balls_template = [
        {"id": i, "x": 0, "y": 0} for i in range(1, 16)
    ] + [{"id": "cue", "x": 0, "y": 0}]

    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        cue_assigned = False
        ball_num = 1

        for (x, y, r) in circles:
            margin = int(r * 1.2)
            roi = image[y - margin:y + margin, x - margin:x + margin]
            if roi.size == 0 or roi.shape[0] == 0 or roi.shape[1] == 0:
                continue

            # Convert ROI to HSV and calculate average hue, saturation, value
            hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
            avg_h, avg_s, avg_v = np.mean(hsv[:,:,0]), np.mean(hsv[:,:,1]), np.mean(hsv[:,:,2])

            # Heuristic: cue ball is low in saturation and high in brightness
            if not cue_assigned and avg_s < 30 and avg_v > 200:
                results.append({"id": "cue", "x": int(x), "y": int(y)})
                cue_assigned = True
            elif ball_num <= 15:
                color, avg_h, avg_s, avg_v = identify_ball_color(hsv)
                #print(f"ball id {ball_name}, color {color}, h {avg_h}, s {avg_s}, v {avg_v}")
                results.append({"id": ball_num, "x": int(x), "y": int(y)})
                ball_num += 1

    # Match detected balls with their IDs
    for ball in balls_template:
        for detected in results:
            if ball["id"] == detected["id"]:
                ball["x"] = detected["x"]
                ball["y"] = detected["y"]
                break

    # Return the table state with the timestamp and ball positions
    table_state = {
        "balls": balls_template,
        "timestamp": int(time.time() * 1000)  # Convert to milliseconds for Firebase
    }

    return table_state

def identify_ball_color(hsv):
    # Print the average HSV values for debugging
    avg_h, avg_s, avg_v = np.mean(hsv[:,:,0]), np.mean(hsv[:,:,1]), np.mean(hsv[:,:,2])

    # Define the color ranges for the pool balls in HSV space
    if 0 <= avg_h < 10:
        color = "red"
    elif 10 <= avg_h < 30:
        color = "yellow"
    elif 30 <= avg_h < 50:
        color = "green"
    elif 50 <= avg_h < 70:
        color = "blue"
    elif 70 <= avg_h < 100:
        color = "purple"
    elif 100 <= avg_h < 140:
        color = "orange"
    elif 140 <= avg_h < 170:
        color = "brown"
    elif 170 <= avg_h < 200:
        color = "black"
    elif avg_h > 200:
        color = "white"  # cue ball
    else:
        color = "unknown"
        
    return color, avg_h, avg_s, avg_v

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ball_tracker.py <image_path>")
        sys.exit(1)

    print("Received args:", sys.argv)

    image_path = sys.argv[1]

    try:
        table_state = detect_balls(image_path)
        print(json.dumps(table_state, indent=2))  # Indented for readability
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)