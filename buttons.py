import tkinter as tk
import pyperclip
from prediction import predict_character

def create_buttons(button_frame, text,points, previous_tip, blackboard, result_entry, history, model, letters, text_var):
    buttons = {
        'r': ('Confirmer', '#cceeff'),  
        'c': ('Continuer', '#cceeff'),  
        'a': ('Annuler', '#cceeff'),    
        ' ': ('Espace', '#cceeff'),     
        's': ('Retour', '#cceeff'),  
        'p': ('Copier le résultat', '#cceeff'),  
        'h': ('Afficher historique', '#cceeff'),
        'q': ('Quitter', '#cceeff') 
    }

    for action, (label, color) in buttons.items():
        button = tk.Button(button_frame, text=label, command=lambda action=action: on_button_press(action,text,points, previous_tip, blackboard, result_entry, history, model, letters, text_var), width=15, height=2, bg=color, font=('Arial', 12))
        button.pack(side=tk.LEFT, padx=5)
def on_button_press(action, text, points, previous_tip, blackboard, result_entry, history, model, letters, text_var):
    if action == 'q':
        exit()
    elif action == 'a':
        points.clear()
        previous_tip = None
        text = ''
        result_entry.delete("1.0", tk.END)
        text_var.set("Prediction: ")
    elif action == ' ':
        points.clear()
        text += ' '
        result_entry.insert(tk.END, ' ')
        text_var.set("Prediction: " + text)
    elif action == 'c':
        points.clear()
    elif action == 'r':
        text+=predict_character(blackboard, points, text, result_entry, history, model, letters, text_var)
    elif action == 's':
        text = text[:-1]  # Supprimer le dernier caractère
        current_text = result_entry.get("1.0", tk.END)
        result_entry.delete("1.0", tk.END)
        result_entry.insert(tk.END, current_text[:-2])
        text_var.set("Prediction: " + text)
    elif action == 'p':
        pyperclip.copy(result_entry.get("1.0", tk.END))  # Copier le texte dans le presse-papiers
    elif action == 'h':
        show_history(history)

def show_history(history):
    history_window = tk.Toplevel()
    history_window.title("Historique des prédictions")
    history_text = tk.Text(history_window, height=10, width=50)
    history_text.pack(pady=10)
    history_text.insert(tk.END, "\n".join(history))
    history_text.config(state=tk.DISABLED)  # Rendre le texte non modifiable

    def copy_history():
        pyperclip.copy("\n".join(history))

    copy_button = tk.Button(history_window, text="Copier l'historique", command=copy_history, bg="#cceeff", fg="black", font=('Arial', 12), relief='raised', bd=2, padx=10, pady=5)
    copy_button.pack(pady=5)