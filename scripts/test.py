from PIL import Image
import os

newScale = 2
ogScale = 20
scaleIncrease = 0.1

if os.path.isdir(f"FinalImages\\Scale{ogScale*scaleIncrease}"): # Check if the folder already exists.
    scale = ogScale * scaleIncrease
    finalImagePath = f"FinalImages\\Scale{scale}\\"

# If the folder does not exist, we can create it.
fileNames = os.listdir(f"FinalImages\\Scale{ogScale}")
images = []
for name in fileNames:
    images.append(Image.open(f"FinalImages\\Scale{ogScale}\\{name}"))

os.mkdir(f"FinalImages\\Scale{int(ogScale*scaleIncrease)}")
for x in range(len(images)):
    #resize
    n_size=(int(images[x].size[0]*scaleIncrease),int(images[x].size[1]*scaleIncrease))
    print(n_size) #output size
    res=images[x].resize(n_size,Image.Resampling.NEAREST)

    #save image
    res.save(f"FinalImages\\Scale{int(ogScale*scaleIncrease)}\\{fileNames[x]}") # Scale is relative to 48 * 27 pixels