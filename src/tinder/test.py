import tensorflow as tf
import keras
from tensorflow.keras.models import load_model
print("Keras Version", keras.__version__)
print("Tf version", tf.__version__)
model = load_model('./retrain2pt2.keras')
print("Model comp details", model.get_compile_config())  # Shows compilation details, which sometimes include versioning metadata

