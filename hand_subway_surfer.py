import cv2
import pyautogui
import mediapipe as mp
import time

pyautogui.FAILSAFE = False

try:
    from mediapipe.python.solutions import hands as mp_hands
    from mediapipe.python.solutions import drawing_utils as mp_draw
except ImportError:
    import mediapipe.solutions.hands as mp_hands
    import mediapipe.solutions.drawing_utils as mp_draw

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0)

current_gesture = "NONE"
last_gesture = "NONE"

print("Starting in 3 seconds... Click your Subway Surfers browser window now!")
time.sleep(3)

while cap.isOpened():
    success, img = cap.read()
    if not success:
        continue


    img = cv2.flip(img, 1)
    h, w, _ = img.shape
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    current_gesture = "NONE"

    
    center_x = w // 2
    center_y = h // 2
    threshold_x = int(w * 0.15)  
    threshold_y = int(h * 0.15)  

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            
            index_tip_x = int(hand_landmarks.landmark[8].x * w)
            index_tip_y = int(hand_landmarks.landmark[8].y * h)
            
            dx = index_tip_x - center_x
            dy = index_tip_y - center_y

            
            if abs(dy) > abs(dx):
                
                if dy < -threshold_y:
                    current_gesture = "UP"
                elif dy > threshold_y:
                    current_gesture = "DOWN"
            else:
               
                if dx < -threshold_x:
                    current_gesture = "LEFT"
                elif dx > threshold_x:
                    current_gesture = "RIGHT"

            
            if current_gesture != last_gesture and current_gesture != "NONE":
                if current_gesture == "UP":
                    pyautogui.press("up")
                elif current_gesture == "DOWN":
                    pyautogui.press("down")
                elif current_gesture == "LEFT":
                    pyautogui.press("left")
                elif current_gesture == "RIGHT":
                    pyautogui.press("right")
                
                last_gesture = current_gesture
            elif current_gesture == "NONE":
                last_gesture = "NONE"

    # Display Text Status
    cv2.putText(img, f"GESTURE: {current_gesture}", (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    
    cv2.rectangle(img, 
                  (center_x - threshold_x, center_y - threshold_y), 
                  (center_x + threshold_x, center_y + threshold_y), 
                  (0, 255, 255), 2)

    cv2.imshow("Subway Surfers Gesture Controller", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()