#Import Libraries
from PIL import Image
import matplotlib.pyplot as plt

#Read image
ogScale = 2
scaleIncrease = 10
fromRelativePath = "SourceImages\\IdeaImages"
toRelativePath = "FinalImages\\Scale"
ogimg=[
        Image.open(f'{fromRelativePath}\\OptionsMenu{ogScale}.png'), 
       ]

finNames = ["OptionMenu"]

for x in range(len(ogimg)):
    #resize
    n_size=(ogimg[x].size[0]*scaleIncrease,ogimg[x].size[1]*scaleIncrease) #output size
    res=ogimg[x].resize(n_size,Image.Resampling.NEAREST)

    #save image
    res.save(f"{toRelativePath}{ogScale*scaleIncrease}\\{finNames[x]}.png") # Scale is relative to 48 * 27 pixels
