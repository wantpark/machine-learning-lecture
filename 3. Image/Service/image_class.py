from tensorflow.keras.preprocessing import image

import numpy as np
import tensorflow as tf
print(tf.__version__)

model = tf.keras.models.load_model('transfer.h5')
print(model.summary())


class_names = ['cat', 'dog']


def run(img):
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)

    preds = model.predict(x)

    # Apply a sigmoid since our model returns logits
    preds = tf.nn.sigmoid(preds)
    preds = tf.where(preds < 0.5, 0, 1)
    preds = preds[0][0]

    return class_names[preds]
