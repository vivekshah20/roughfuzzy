#Converst Image to pixel data
from __future__ import print_function
import Image
log = open("sample.txt", "w")
im=Image.open('brainmri.gif')
Imv=im.load()
x,y=im.size
l_pixel=[]
for i in range(y):
	for j in range(x):
		l_pixel.append(Imv[j,i])
	print ( str(l_pixel).strip('[]') , file = log)
	l_pixel = []
