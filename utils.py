import numpy as np

def normalize_image(image):
    return image.astype('float32') / 255.0

def preprocess_image(image, input_shape):
    image = cv2.resize(image, input_shape[:2])
    image = normalize_image(image)
    image = np.expand_dims(image, axis=-1)
    return image