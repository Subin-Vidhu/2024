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



# Path: Personal/Hand_Gesture_Recognition_with_Mediapipe.py
"""
 the code enables interactive finger painting on a canvas using real-time hand gestures detected by a webcam, 
 allowing users to draw lines in different colors and clear the canvas as needed
# """
# import cv2
# import numpy as np
# import mediapipe as mp
# from collections import deque

# # Giving different arrays to handle color points of different color
# white_points = [deque(maxlen=1024)]
# green_points = [deque(maxlen=1024)]
# red_points = [deque(maxlen=1024)]
# black_points = [deque(maxlen=1024)]

# # These indexes will be used to mark the points in particular arrays of specific color
# white_idx = 0
# green_idx = 0
# red_idx = 0
# black_idx = 0

# # The kernel to be used for dilation purpose
# dilation_kernel = np.ones((5, 5), np.uint8)

# # Colors: white, green, red, black
# color_palette = [(255, 255, 255), (0, 255, 0), (0, 0, 255), (0, 0, 0)]
# current_color_index = 0

# # Setup the paint window
# canvas_width = 600
# canvas_height = 471  # Keep the same as original
# paint_canvas = np.zeros((canvas_height, canvas_width, 3), dtype=np.uint8) + 255
# paint_canvas = cv2.rectangle(paint_canvas, (40, 1), (140, 65), (0, 0, 0), 2)
# paint_canvas = cv2.rectangle(paint_canvas, (160, 1), (255, 65), (255, 255, 255), 2)
# paint_canvas = cv2.rectangle(paint_canvas, (275, 1), (370, 65), (0, 255, 0), 2)
# paint_canvas = cv2.rectangle(paint_canvas, (390, 1), (485, 65), (0, 0, 255), 2)
# paint_canvas = cv2.rectangle(paint_canvas, (505, 1), (600, 65), (0, 0, 0), 2)

# cv2.putText(paint_canvas, "CLEAR", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
# cv2.putText(paint_canvas, "WHITE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
# cv2.putText(paint_canvas, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
# cv2.putText(paint_canvas, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
# cv2.putText(paint_canvas, "BLACK", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

# # Initialize mediapipe
# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
# mp_draw = mp.solutions.drawing_utils

# # Initialize the webcam
# cap = cv2.VideoCapture(0)

# if not cap.isOpened():
#     print("Error: Could not open webcam.")
#     exit()

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         print("Error: Failed to capture image.")
#         break

#     frame_height, frame_width, _ = frame.shape
#     key = cv2.waitKey(1) & 0xFF
#     if key == ord('q'):
#         break

#     # Flip the frame vertically
#     frame = cv2.flip(frame, 1)
#     frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#     # Resize frame to match paint_canvas width
#     frame = cv2.resize(frame, (canvas_width, canvas_height))

#     frame = cv2.rectangle(frame, (40, 1), (140, 65), (0, 0, 0), 2)
#     frame = cv2.rectangle(frame, (160, 1), (255, 65), (255, 255, 255), 2)
#     frame = cv2.rectangle(frame, (275, 1), (370, 65), (0, 255, 0), 2)
#     frame = cv2.rectangle(frame, (390, 1), (485, 65), (0, 0, 255), 2)
#     frame = cv2.rectangle(frame, (505, 1), (600, 65), (0, 0, 0), 2)
#     cv2.putText(frame, "CLEAR", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
#     cv2.putText(frame, "WHITE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
#     cv2.putText(frame, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
#     cv2.putText(frame, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
#     cv2.putText(frame, "BLACK", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

#     # Get hand landmark prediction
#     result = hands.process(frame_rgb)

#     # Post process the result
#     if result.multi_hand_landmarks:
#         landmarks = []
#         for hand_landmarks in result.multi_hand_landmarks:
#             for lm in hand_landmarks.landmark:
#                 lmx = int(lm.x * canvas_width)  # Scale to canvas width
#                 lmy = int(lm.y * canvas_height)  # Scale to canvas height
#                 landmarks.append([lmx, lmy])

#             # Drawing landmarks on frames
#             mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        
#         forefinger_pos = (landmarks[8][0], landmarks[8][1])
#         finger_tip = forefinger_pos
#         dot_radius = 8  # Increase the size of the dot for better visibility

#         # Draw a large dot (or circle) at the finger tip
#         cv2.circle(frame, finger_tip, dot_radius, (0, 255, 0), -1)  # Draw dot on frame
#         cv2.circle(paint_canvas, finger_tip, dot_radius, (0, 255, 0), -1)

#         thumb_tip = (landmarks[4][0], landmarks[4][1])
        
#         if (thumb_tip[1] - finger_tip[1] < 30):
#             white_points.append(deque(maxlen=512))
#             white_idx += 1
#             green_points.append(deque(maxlen=512))
#             green_idx += 1
#             red_points.append(deque(maxlen=512))
#             red_idx += 1
#             black_points.append(deque(maxlen=512))
#             black_idx += 1

#         elif finger_tip[1] <= 65:
#             if 40 <= finger_tip[0] <= 140:  # Clear Button
#                 white_points = [deque(maxlen=512)]
#                 green_points = [deque(maxlen=512)]
#                 red_points = [deque(maxlen=512)]
#                 black_points = [deque(maxlen=512)]

#                 white_idx = 0
#                 green_idx = 0
#                 red_idx = 0
#                 black_idx = 0

#                 paint_canvas[67:, :, :] = 255
#             elif 160 <= finger_tip[0] <= 255:
#                 current_color_index = 1  # White
#             elif 275 <= finger_tip[0] <= 370:
#                 current_color_index = 2  # Green
#             elif 390 <= finger_tip[0] <= 485:
#                 current_color_index = 3  # Red
#             elif 505 <= finger_tip[0] <= 600:
#                 current_color_index = 4  # Black
#         else:
#             if current_color_index == 1:
#                 white_points[white_idx].appendleft(finger_tip)
#             elif current_color_index == 2:
#                 green_points[green_idx].appendleft(finger_tip)
#             elif current_color_index == 3:
#                 red_points[red_idx].appendleft(finger_tip)
#             elif current_color_index == 4:
#                 black_points[black_idx].appendleft(finger_tip)
#     else:
#         white_points.append(deque(maxlen=512))
#         white_idx += 1
#         green_points.append(deque(maxlen=512))
#         green_idx += 1
#         red_points.append(deque(maxlen=512))
#         red_idx += 1
#         black_points.append(deque(maxlen=512))
#         black_idx += 1

#     # Draw lines of all the colors on the canvas and frame
#     point_groups = [white_points, green_points, red_points, black_points]
#     for i in range(len(point_groups)):
#         for j in range(len(point_groups[i])):
#             for k in range(1, len(point_groups[i][j])):
#                 if point_groups[i][j][k - 1] is None or point_groups[i][j][k] is None:
#                     continue
#                 # Scale points to frame size
#                 pt1 = (int(point_groups[i][j][k - 1][0] * (frame.shape[1] / canvas_width)), 
#                        int(point_groups[i][j][k - 1][1] * (frame.shape[0] / canvas_height)))
#                 pt2 = (int(point_groups[i][j][k][0] * (frame.shape[1] / canvas_width)), 
#                        int(point_groups[i][j][k][1] * (frame.shape[0] / canvas_height)))
#                 cv2.line(frame, pt1, pt2, color_palette[i], 2)
#                 cv2.line(paint_canvas, point_groups[i][j][k - 1], point_groups[i][j][k], color_palette[i], 2)

#     # Show frames
#     cv2.imshow('Frame', frame)
#     cv2.imshow('Paint', paint_canvas)

# cap.release()
# cv2.destroyAllWindows()
