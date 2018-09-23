from PIL import Image
import os
from multiprocessing import Pool

size=(28,28)
INPUT_FOLDER = "localized_images/"
OUTPUT_FOLDER = "l_resized_images/"

def resize(start):
	files = os.listdir(INPUT_FOLDER)
	files_out = os.listdir(OUTPUT_FOLDER)
	total_count = len(files)
	count = 0
	#Pooling hardcoded for 4 processes
	for index in range(start,len(files),4):
		f = files[index]
		count += 1
		print(str(start)+": "+str(count)+" of "+str(total_count), end='\r', flush=True)
		if f in files_out:
			continue
		im = Image.open(INPUT_FOLDER+f)
		im = im.convert("L")
		im.thumbnail(size)
		path = OUTPUT_FOLDER+f
		im.save(path)

if __name__ == '__main__':
    p = Pool(4)
    output=p.map(resize, [0,1,2,3])