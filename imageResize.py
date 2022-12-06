#Import Libraries
from PIL import Image
import matplotlib.pyplot as plt

#Read image
ogimg=[Image.open('IdeaImages\delSoon.png')] #, Image.open('SourceImages\HelpS.png'), Image.open('SourceImages\QuitS.png')]
finNames = ["LoginScreen", "Help", "Quit"]
scale = 2

for x in range(len(ogimg)):
    #resize
    n_size=(ogimg[x].size[0]*scale,ogimg[x].size[1]*scale) #output size
    res=ogimg[x].resize(n_size,Image.NEAREST)

    #save image
    res.save(f"IdeaImages\{finNames[x]}{20/scale}.png") # The number after is scale relative to 1920 * 1080 (e.g. 2 --> 1920/2 = 960)

    #display image
    plt.imshow(res)
    plt.show()