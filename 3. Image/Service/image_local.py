from tensorflow.keras.preprocessing import image

import os
import tensorflow as tf

import image_class


IMG_SIZE = 160

image_url = \
    'https://images.immediate.co.uk/production/volatile/sites/23/2014/10/GettyImages-172050389-8ab8710.jpg'
# 'https://www.zooplus.ie/magazine/wp-content/uploads/2020/01/Female-Dogs-in-Heat-IE-1024x683.jpeg'
# 'https://static01.nyt.com/images/2021/11/16/well/11Well-NL-DOG-SLEEP/11Well-NL-DOG-SLEEP-superJumbo.jpg'
# 'https://icatcare.org/app/uploads/2018/07/Thinking-of-getting-a-cat.png'
# 'https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/dog-puppy-on-garden-royalty-free-image-1586966191.jpg'

image_path = tf.keras.utils.get_file('court', origin=image_url)
img = image.load_img(image_path, target_size=(IMG_SIZE, IMG_SIZE))
os.remove(image_path)  # Remove the cached file

result = image_class.run(img)
print(result)
