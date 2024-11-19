import tensorflow as tf
from tensorflow import keras

# Check TensorFlow version
print("TensorFlow version:", tf.__version__)

# Simple test model
model = keras.Sequential([
    keras.layers.Dense(10, input_shape=(5,), activation='relu'),
    keras.layers.Dense(1, activation='sigmoid')
])

print("Model summary:")
model.summary()