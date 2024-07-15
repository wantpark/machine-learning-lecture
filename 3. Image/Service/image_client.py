from skimage.io import imread
from skimage.transform import resize
from skimage.util import img_as_ubyte
import socket


HOST = "192.168.55.1"  # The server's hostname or IP address
PORT = 8000  # The port used by the server

IMG_SIZE = 160

image_url = \
    'https://images.immediate.co.uk/production/volatile/sites/23/2014/10/GettyImages-172050389-8ab8710.jpg'
# 'https://www.zooplus.ie/magazine/wp-content/uploads/2020/01/Female-Dogs-in-Heat-IE-1024x683.jpeg'
# 'https://static01.nyt.com/images/2021/11/16/well/11Well-NL-DOG-SLEEP/11Well-NL-DOG-SLEEP-superJumbo.jpg'
# 'https://icatcare.org/app/uploads/2018/07/Thinking-of-getting-a-cat.png'
# 'https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/dog-puppy-on-garden-royalty-free-image-1586966191.jpg'

img = imread(image_url)
img = resize(img, (IMG_SIZE, IMG_SIZE))
img = img_as_ubyte(img)
img = img.tobytes()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(img)
    data = s.recv(1024)

    print(data.decode('utf-8'))
