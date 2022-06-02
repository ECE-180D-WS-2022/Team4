#from asyncio.windows_events import NULL
from pickle import FALSE, TRUE
import cv2
import mediapipe as mp
from typing import NamedTuple
import pygame

def camera(WIN, str_length, keyboard_size):
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_hands = mp.solutions.hands

    TIME_TO_COUNT = 30

    answer = ""
    arr = []
    prev_key_count = 0
    prev_num = -1
    key_touched = False
    saved_left = -1
    saved_right = -1

    # For webcam input:
    cap = cv2.VideoCapture(0)
    with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
        while cap.isOpened():
            WIN.fill([0,0,0])
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue

            hand_image = image
            
            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            hand_image.flags.writeable = False
            hand_image = cv2.cvtColor(hand_image, cv2.COLOR_BGR2RGB)
            results = hands.process(hand_image)

            # Draw the hand annotations on the image.
            hand_image.flags.writeable = True
            hand_image = cv2.cvtColor(hand_image, cv2.COLOR_RGB2BGR)
            
            h = len(image)
            w = len(image[1])
            #w: 540-740, h:260-460
            #print("Box Coords: w: ", w//2 - 100, "h: ", h//2 - 100)
        
            #mid_w = w // 7
            mid_w = w // keyboard_size
            
            i = 0
            while i < w:
                cv2.rectangle(image,(i,h//2-100),(i+mid_w,h//2+100),(255,255,255),cv2.FILLED)
                cv2.rectangle(image,(i,h//2-100),(i+mid_w,h//2+100),(0,0,255),2)
                
                #add black background
                cv2.rectangle(image,(0,h//2+100),(w,h),(0,0,0),cv2.FILLED)
                cv2.rectangle(image,(0,0),(w,h//2-100),(0,0,0),cv2.FILLED)

                crop = image[h//2 - 100 : h//2 + 100, i : i  + mid_w]   
                img = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB) 
                img = crop.reshape((crop.shape[0] * crop.shape[1],3))
                i += mid_w

            if key_touched:
                cv2.rectangle(image,(saved_left,h//2-100),(saved_right,h//2+100),(0,0,255),2)

            #Get the pointer finger coordinates
            p_x = 0.0
            p_y = 0.0
            p_z = 0.0
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                            image,
                            hand_landmarks,
                            mp_hands.HAND_CONNECTIONS,
                            mp_drawing_styles.get_default_hand_landmarks_style(),
                            mp_drawing_styles.get_default_hand_connections_style())
                    i = 0
                    for landmark in enumerate(hand_landmarks.landmark):  
                        if i == 8:
                            p_x = landmark[1].x
                            p_y = landmark[1].y
                            p_z = landmark[1].z
                            break
                        i += 1

            #print("x: ", p_x*w, "y: ", p_y*h)
            '''
            key = 'C'
            in_h = False
            if p_y*h < (h//2 + 100) and p_y*h > (h//2 - 100):
                in_h = True
                p_x *= w
                if p_x < mid_w*2 and p_x > mid_w:
                    key = 'A'
                if p_x < mid_w*3 and p_x > mid_w*2:
                    key = 'G'
                if p_x < mid_w*4 and p_x > mid_w*3:
                    key = 'F'
                if p_x < mid_w*5 and p_x > mid_w*4:
                    key = 'E'
                if p_x < mid_w*6 and p_x > mid_w*5:
                    key = 'D'
                print(key)
            '''
            key = 'd'
            num = 0
            if p_y*h < (h//2 + 100) and p_y*h > (h//2 - 100):
                p_x *= w
                q = 0
                left = 0
                right = mid_w
                while left < w:
                    if p_x < right and p_x > left:
                        #key = 'f'
                        num = q
                        break
                    q += 1
                    left = right
                    right += mid_w
                    
                
                if prev_num == -1:
                    prev_num = num
                    prev_key_count = 1
                elif num == prev_num:
                    prev_key_count = prev_key_count + 1
                elif num != prev_num:
                    cv2.rectangle(image,(left,h//2-100),(right,h//2+100),(0,0,255),2)
                    key_touched = False
                    prev_key_count = 1
                    prev_num = num

                if prev_key_count >= TIME_TO_COUNT:
                    #change the color of the key box
                    #answer  = answer + key
                    cv2.rectangle(image,(left,h//2-100),(right,h//2+100),(0,255,0),2)
                    if key_touched == False:
                        arr.append(num)
                    key_touched = True
                    saved_left = left
                    saved_right = right
                    #prev_key_count = 0
            else:
                key_touched = False
                prev_key_count = -1
            
            if str_length == len(arr):
                break

            # Flip the image horizontally for a selfie-view display.
            #cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
            if cv2.waitKey(5) & 0xFF == 27:
                break

            #image = cv2.flip(image, 1)
            surf = pygame.surfarray.make_surface(image)

            new_surf = pygame.transform.rotate(surf, 270)
            #new_rect = new_surf.get_rect(center = surf.get_rect(topleft = (0,0)).center)
            WIN.blit(new_surf, (0,0))
            pygame.display.update()

    ans = ''
    for i in range(len(arr)):
        ans += str(6 - arr[i])

    return ans

    cap.release()
