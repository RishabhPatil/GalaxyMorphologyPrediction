from PIL import Image
import os

size=(28,28)

def list_files(folder):
	files= os.listdir(folder)
	return files

def resize(folder,size=size):
	files = list_files(folder)
	total_count = len(files)
	count = 0
	for f in files:
		count+=1
		print(count+" of "+total_count, end='\r', flush=True)
		im = Image.open(folder+f)
		im=im.convert("L")
		im.thumbnail(size)
		path="new/"+f
		im.save(path)
		if count==100:
			break

resize("../GRP64/images_training_rev1/images_training_rev1/")