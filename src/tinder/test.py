import tensorflow as tf
import keras
from tensorflow.keras.models import load_model
from keras.models import load_model
print("Keras Version", keras.__version__)
print("Tf version", tf.__version__)
model = load_model('/Users/amiyasekhar/Downloads/swipeMate/src/tinder/retrain2pt2.keras', custom_objects={)
print("Model comp details", model.get_compile_config())  # Shows compilation details, which sometimes include versioning metadata
print("Model Metadata:")
print(model._keras_metadata if hasattr(model, "_keras_metadata") else "No Keras metadata found.")
if model.optimizer:
    print("Optimizer Config:", model.optimizer.get_config())  # Details of optimizer used
else:
    print("No optimizer found.")