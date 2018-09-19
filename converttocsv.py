from PIL import Image
import os

def write_header(output_file, size):
    
    with open(output_file,'w') as f:
        data='Filename,Label,'
        for i in range(size):
            for j in range(size):
                data+=str(i)+' '+str(j)+','
        f.write(data[:-1])

def get_input_files(input_folder):
    
    filelist=os.listdir(input_folder)

    for fichier in filelist[:]:
        if not(fichier.endswith(".jpg")):
            filelist.remove(fichier)

    return filelist

def read_labels(label_file):
    data_labels=[]
    label={}
    with open('training_solutions_rev1.csv','r') as f:
        data_labels=f.read()
        data_labels=data_labels.replace('\r','').split('\n')
        data_labels=data_labels[1:-1]
        for i in data_labels:
            i=i.split(',')
            label[int(i[0])]=int(i.index(max(i[1:4])))
    return label

def write_output(output_file, input_folder, label_file, size):
    write_header(output_file, size)
    filelist = get_input_files(input_folder)
    label = read_labels(label_file)
    
    count=0
    total_count = len(filelist)
    for i in filelist:
        count+=1
        print(str(count)+" of "+str(total_count), end='\r', flush=True)
        im=Image.open(input_folder+i)
        pix = im.load()
        x,y=im.size
        data='\n'+str(i.replace('.jpg',''))+','+str(label[int(i.replace('.jpg',''))])+","
        for j in range(0,x*y):
            data+=str(pix[j/x,j%x])+','
        with open(output_file,'a') as f:
            f.write(data[:-1])

write_output("output.csv", "new/", 'training_solutions_rev1.csv', 28)