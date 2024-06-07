import cv2
import numpy as np
import tkinter as tk

def predict_character(blackboard, points, text, result_entry, history, model, letters, text_var):
    if len(points) > 0:
        # Convertir l'image en niveaux de gris
        alphabet_gray = cv2.cvtColor(blackboard, cv2.COLOR_BGR2GRAY)
        
        # Redimensionner l'image à la taille attendue par le modèle
        img = cv2.resize(alphabet_gray, (28, 28))
        
        # Trouver la zone de texte sur le blackboard
        contours, _ = cv2.findContours(alphabet_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(contour)
            
            # Extraire la zone de texte
            text_region = alphabet_gray[y:y+h, x:x+w]
            
            # Redimensionner la zone de texte à la taille attendue par le modèle
            text_region = cv2.resize(text_region, (28, 28))
            
            # Rotation de 90 degrés
            text_region = cv2.rotate(text_region, cv2.ROTATE_90_CLOCKWISE)
            
            # Inversion horizontale
            text_region = cv2.flip(text_region, 1)
            
            # Normaliser image
            text_region = text_region.astype('float32') / 255
            
            # Ajouter une dimension de canal
            text_region = np.expand_dims(text_region, axis=-1)
            
            # Faire la prédiction avec le modèle
            prediction = model.predict(text_region.reshape(1, 28, 28, 1))
            predicted_class = np.argmax(prediction)
            text += letters[predicted_class]
            result_entry.insert(tk.END, letters[predicted_class])
            
            # Ajouter la prédiction à l'historique et mettre à jour le texte de prédiction
            history.append(text)
            text_var.set("Prediction: " + text)
            return letters[predicted_class]