#Import Libraries
from PIL import Image
import matplotlib.pyplot as plt

#Read image
img=Image.open('ship4HP.png')

#resize
o_size=(40,160) #output size
res=img.resize(o_size,Image.NEAREST)

#save image
res.save('ship4HP_US.png')

#display image
plt.imshow(res)
plt.show()