#Converts Pixel Data to Image
from numpy import genfromtxt
from PIL import Image
import numpy as np
my_data = genfromtxt('foo.csv', delimiter=',')
my_data=np.asarray(my_data,dtype=np.uint8)
w= Image.fromarray(my_data)
w.save('brainmri_no.jpg')
