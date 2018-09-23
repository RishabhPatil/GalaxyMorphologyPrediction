from PIL import Image
import os
import matplotlib.pyplot as plt
from multiprocessing import Pool
import numpy as np

INPUT_FOLDER = "l_resized_images/"
OUTPUT_FOLDER = "l_rotated_images/"

files = os.listdir(INPUT_FOLDER)

def rotator(start):
    files_out = os.listdir(OUTPUT_FOLDER)
    count = 0
    total_count = len(files)
    #Pooling hardcoded for 4 processes
    for index in range(start,total_count,4):
        filename = files[index]
        count += 1
        print(str(start)+": "+str(count)+" of "+str(total_count), end='\r', flush=True)
        im = Image.open(INPUT_FOLDER+filename)
        im = im.convert("L")
        pix = np.array(im)
        img_no = 0
        for i in range(4):
            im = np.rot90(im,axes=(-2,-1))
            img = Image.fromarray(im)
            img_no += 1
            img.save(OUTPUT_FOLDER+filename.replace(".jpg","")+"_"+str(img_no)+".jpg")

if __name__ == '__main__':
    p = Pool(4)
    output=p.map(rotator, [0,1,2,3])