import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import mediapipe as mp
import numpy as np
from tensorflow.keras.models import load_model
import pyperclip
from prediction import predict_character
from video import update_video
from buttons import on_button_press, show_history,create_buttons
from entrainement import train_model
def start_training_process():
    train_model()

model = load_model('best_model.keras')

letters = {i: chr(i + 97) for i in range(26)}

blackboard = np.zeros((480, 640, 3), dtype=np.uint8)
points = []
previous_tip = None

window = tk.Tk()
window.title("Alphabet Recognition System")

window.geometry("800x600")
window.configure(bg="#f0f0f0")

welcome_frame = tk.Frame(window, bg="#f0f0f0")
welcome_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Message de bienvenue
welcome_label = tk.Label(welcome_frame, text="You finger it, we got it!", font=('Arial', 18), bg="#f0f0f0", fg="#333")
welcome_label.pack(pady=10)

# un bouton pour démarrer la prédiction
def start_prediction():
    welcome_frame.pack_forget()  
    video_frame.pack(pady=10)    
    button_frame.pack(pady=10)   
    result_frame.pack(pady=10)   
    messagebox.showinfo("Information", "La prédiction a démarré!")
    text_var.set("Prediction: ")
    update_video(window, video_label, cap, points, previous_tip, blackboard, model, letters, text_var)

start_button = tk.Button(welcome_frame, text="Explorer", command=start_prediction, width=15, height=2, bg="#cceeff", font=('Arial', 12))
start_button.pack()

video_frame = tk.Frame(window, bg="#f0f0f0")
video_frame.pack_forget()

video_label = tk.Label(video_frame)
video_label.pack()

button_frame = tk.Frame(window, bg="#f0f0f0")
button_frame.pack_forget()

result_frame = tk.Frame(window, bg="#f0f0f0")
result_frame.pack_forget()

result_entry = tk.Text(result_frame, font=('Arial', 14), width=100, height=3, bd=3, highlightbackground="#ddcc00", highlightthickness=4)
result_entry.pack(pady=10)

text_var = tk.StringVar()
text_var.set("Prediction: ")

prediction_label = tk.Label(video_frame, textvariable=text_var, font=('Arial', 14), bg="#f0f0f0", fg="#333")
prediction_label.pack()


cap = cv2.VideoCapture(0)
global text
text = ''
history = []

create_buttons(button_frame, text, points, previous_tip, blackboard, result_entry, history, model, letters, text_var)

def on_key_press(event):
    key = event.char.lower()  
    if key in ['a', 'r', 's', ' ', 'c', 'p', 'h','q']:
        on_button_press(key, text, points, previous_tip, blackboard, result_entry, history, model, letters, text_var)
window.bind('<KeyPress>', on_key_press)

# Lancer la boucle principale de Tkinter
window.mainloop()

# Libérer la webcam
cap.release()
cv2.destroyAllWindows()