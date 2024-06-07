import cv2
from PIL import Image, ImageTk
import mediapipe as mp
import numpy as np

# Initialiser Mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)

def setup_video_capture():
    cap = cv2.VideoCapture(0)
    return cap

def update_video(window, video_label, cap, points, previous_tip, blackboard, model, letters, text):
    ret, frame = cap.read()
    if not ret:
        return

    frame = cv2.flip(frame, 1)
    # Convertir l'image en niveaux de gris
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Effacer le blackboard
    blackboard.fill(0)

    # Détecter les mains avec Mediapipe
    results = hands.process(frame)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Dessiner la partie détectée de la main
            mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            # Enregistrer les coordonnées du bout du doigt
            tip = hand_landmarks.landmark[8]  # Le bout du doigt est le 8ème landmark
            h, w, _ = frame.shape
            cx, cy = int(tip.x * w), int(tip.y * h)
            points.append((cx, cy))
            previous_tip = (cx, cy)

    # Dessiner les points sur le blackboard
    for i in range(1, len(points)):
        if points[i - 1] is None or points[i] is None:
            continue
        cv2.line(frame, points[i - 1], points[i], (0, 0, 0), 2)
        cv2.line(blackboard, points[i - 1], points[i], (255, 255, 255), 8)
    
    # Ajouter le texte à l'image
    #cv2.putText(frame, "Prediction: " + text, (20, frame.shape[0] - 20),
                #cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    
    # Convertir l'image en RGB (Tkinter utilise le format RGB)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Convertir l'image en PIL Image
    image = Image.fromarray(frame)

    # Convertir l'image PIL en PhotoImage (Tkinter utilise le format PhotoImage)
    photo = ImageTk.PhotoImage(image)

    # Mettre à jour le label avec la nouvelle image
    video_label.config(image=photo)
    video_label.image = photo

    # Appeler cette fonction à nouveau après 15 millisecondes
    window.after(15, update_video, window, video_label, cap, points, previous_tip, blackboard, model, letters, text)
