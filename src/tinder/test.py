import tensorflow as tf

model_path = '/Users/amiyasekhar/Downloads/swipeMate/src/tinder/retrain2pt2.keras'

# Check the model format
try:
    loaded_model = tf.keras.models.load_model(model_path)
    print("Model loaded successfully!")
    print("Model summary:")
    loaded_model.summary()  # Print model architecture if it loads successfully
except Exception as e:
    print("Error loading model:", e)

# Check if it's a SavedModel directory
try:
    if tf.saved_model.contains_saved_model(model_path):
        print("The model is in SavedModel format.")
    else:
        print("The model is NOT in SavedModel format (it might be .keras or .h5).")
except Exception as e:
    print("Error while checking SavedModel format:", e)

model_path = '/Users/amiyasekhar/Downloads/swipeMate/src/tinder/retrain2pt2.keras'

# Load the model and check the version
try:
    loaded_model = tf.keras.models.load_model(model_path)
    print("Model loaded successfully!")
    print(f"Model saved with TensorFlow version: {tf.__version__}")
except Exception as e:
    print("Error loading model:", e)