import cv2
import numpy as np
import mediapipe as mp
from collections import deque

# Constants and setup
MAX_POINTS = 1024
COLORS = [(255, 255, 255), (0, 255, 0), (0, 0, 255), (0, 0, 0)]
COLOR_NAMES = ["WHITE", "GREEN", "RED", "BLACK"]
WINDOW_WIDTH, WINDOW_HEIGHT = 600, 471

# Initialize Mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Initialize color points
color_points = {color: [deque(maxlen=MAX_POINTS)] for color in COLORS}
color_indices = {color: 0 for color in COLORS}
current_color = COLORS[0]

# Set up canvas
canvas = np.ones((WINDOW_HEIGHT, WINDOW_WIDTH, 3), dtype=np.uint8) * 255
def draw_ui(frame):
    frame = cv2.rectangle(frame, (40, 1), (140, 65), (0, 0, 0), 2)
    frame = cv2.rectangle(frame, (160, 1), (255, 65), COLORS[0], 2)
    frame = cv2.rectangle(frame, (275, 1), (370, 65), COLORS[1], 2)
    frame = cv2.rectangle(frame, (390, 1), (485, 65), COLORS[2], 2)
    frame = cv2.rectangle(frame, (505, 1), (600, 65), COLORS[3], 2)
    cv2.putText(frame, "CLEAR", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    for i, name in enumerate(COLOR_NAMES):
        x = 185 + 115 * i
        cv2.putText(frame, name, (x, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    return frame

canvas = draw_ui(canvas)

def process_frame(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(frame_rgb)
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            return hand_landmarks.landmark
    return None

def clear_canvas():
    global color_points, color_indices
    color_points = {color: [deque(maxlen=MAX_POINTS)] for color in COLORS}
    color_indices = {color: 0 for color in COLORS}
    canvas[67:, :, :] = 255

def update_points(finger_tip):
    global current_color
    if current_color:
        color_points[current_color][color_indices[current_color]].appendleft(finger_tip)

def draw_lines(frame):
    for color, points_list in color_points.items():
        for points in points_list:
            for i in range(1, len(points)):
                if points[i - 1] is None or points[i] is None:
                    continue
                cv2.line(frame, points[i - 1], points[i], color, 2)
                cv2.line(canvas, points[i - 1], points[i], color, 2)

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture image.")
        break

    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (WINDOW_WIDTH, WINDOW_HEIGHT))
    frame = draw_ui(frame)
    landmarks = process_frame(frame)

    if landmarks:
        finger_tip = (int(landmarks[8].x * WINDOW_WIDTH), int(landmarks[8].y * WINDOW_HEIGHT))
        thumb_tip = (int(landmarks[4].x * WINDOW_WIDTH), int(landmarks[4].y * WINDOW_HEIGHT))
        cv2.circle(frame, finger_tip, 8, (0, 255, 0), -1)
        cv2.circle(canvas, finger_tip, 8, (0, 255, 0), -1)

        if abs(thumb_tip[1] - finger_tip[1]) < 30:
            for color in COLORS:
                color_points[color].append(deque(maxlen=MAX_POINTS))
                color_indices[color] += 1
        elif finger_tip[1] <= 65:
            if 40 <= finger_tip[0] <= 140:
                clear_canvas()
            else:
                for i, color in enumerate(COLORS):
                    if 160 + 115 * i <= finger_tip[0] <= 255 + 115 * i:
                        current_color = color
        else:
            update_points(finger_tip)

    draw_lines(frame)
    cv2.imshow('Frame', frame)
    cv2.imshow('Paint', canvas)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
