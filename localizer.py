from PIL import Image
import os
import matplotlib.pyplot as plt
from multiprocessing import Pool
import copy
import numpy as np

#Original Image Folder
INPUT_FOLDER = "images_training_rev1/images_training_rev1/"
OUTPUT_FOLDER = "localized_images/"

files = os.listdir(INPUT_FOLDER)

def show_threshold(pix,threshold):
    img = Image.open(INPUT_FOLDER+filename)
    img = img.convert('L')
    pix = np.array(img)
    for i in range(len(pix)):
        for j in range(len(pix[i])):
            if pix[i,j]<int(threshold):
                pix[i,j]=0
    return pix

def show_image(img):
    imgplot = plt.imshow(img,cmap='Greys_r')
    plt.show()

def save(pix,filepath):
    im = Image.fromarray(pix)
    im.save(filepath)
    
def cropper(pix, threshold):
    xc = 212
    current_window=50
    while True:
        l = max(0, xc - current_window)
        m = min(423, xc + current_window)
        if l==0 and m==423:
            break
        ins = 0
        count = 0
        for k in [l, m]:
            for i in range(l,m+1):
                ins += pix[i,l]+pix[i,m]+pix[l,i]+pix[m,i]
                count+=4
        ins -= pix[l,l]+pix[m,m]+pix[l,m]+pix[m,l]
        count -= 4
        if ins/count>threshold:
            current_window+=1
        else:
            break
    return pix[l:m+1,l:m+1]

def localize(start):
    count=0
    total_count = len(files)
    files_out = os.listdir(OUTPUT_FOLDER)
    #Pooling hardcoded for 4 processes
    for index in range(start,total_count,4):
        filename = files[index]
        count+=1
        print(str(start)+": "+str(count)+" of "+str(total_count), end='\r', flush=True)
        if filename in files_out:
            continue
        im = Image.open(INPUT_FOLDER+filename)
        im=im.convert("L")
        pix = np.array(im)
        x,y=im.size
        max_intensity=0
        for x in pix:
            for y in x:
                max_intensity = max(max_intensity, y)
        crop_pix = cropper(pix, max_intensity/10)
    #     show_image(crop_pix)
        save(crop_pix, OUTPUT_FOLDER+filename)

if __name__ == '__main__':
    p = Pool(4)
    output=p.map(localize, [0,1,2,3])