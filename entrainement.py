import pandas as pd
from sklearn.model_selection import train_test_split
import tensorflow as tf 
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.callbacks import ModelCheckpoint
#tensorflow 2.15.0 && keras 2.3.1
def train_model():
    # Charger les données d'entraînement et de test
    train_data = pd.read_csv('emnist-letters-train.csv')
    test_data = pd.read_csv('emnist-letters-test.csv')

    # Charger la correspondance entre les étiquettes et les lettres
    label_mapping = {}
    with open('emnist-letters-mapping.txt', 'r') as f:
        for line in f:
            parts = line.strip().split()
            label = int(parts[0])
            letter = parts[1]
            label_mapping[label] = letter

    # Extraire les étiquettes pour les données d'entraînement
    train_labels = train_data.iloc[:, 0].values
    train_letters = [label_mapping[label] for label in train_labels]

    # Extraire les étiquettes pour les données de test
    test_labels = test_data.iloc[:, 0].values
    test_letters = [label_mapping[label] for label in test_labels]

    # Charger les pixels des images de train et de test et les adapter pour le CNN
    X_train = train_data.iloc[:, 1:].values.reshape(-1, 28, 28, 1).astype('float32') / 255.0
    X_test = test_data.iloc[:, 1:].values.reshape(-1, 28, 28, 1).astype('float32') / 255.0

    # Convertir les étiquettes en format one-hot
    num_classes = 26
    y_train = tf.keras.utils.to_categorical(train_labels - 1, num_classes=num_classes)
    y_test = tf.keras.utils.to_categorical(test_labels - 1, num_classes=num_classes)

    # Définir le modèle CNN
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
        MaxPooling2D((2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(num_classes, activation='softmax')
    ])
    model.summary()
    # Compiler le modèle
    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    # Entraîner le modèle
    checkpointer = ModelCheckpoint(filepath='my_model.keras', verbose=1, save_best_only=True)
    model.fit(X_train, y_train, batch_size=128, epochs=10, validation_split=0.2,
             
             callbacks=[checkpointer])

    # Évaluer le modèle sur les données de test
    test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
    print("Test accuracy:", test_accuracy*100)

    # Sauvegarder le modèle
    model.save('best_model.keras')