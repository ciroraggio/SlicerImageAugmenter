import os

def collectImagesAndMasksList(imagesInputPath, imgPrefix, maskPrefix):
    imgs, masks = [], []
    for dir in os.listdir(imagesInputPath):
        for content in os.listdir(f"{imagesInputPath}/{dir}"):
                if(not os.path.isdir(f"{imagesInputPath}/{dir}/{content}")): # if the path is a new directory I ignore it
                    if(imgPrefix in content):
                        imgs.append(f"{imagesInputPath}/{dir}/{content}")
                    elif(maskPrefix in f"{imagesInputPath}/{dir}/{content}"):
                        masks.append(f"{imagesInputPath}/{dir}/{content}")
    return imgs, masks