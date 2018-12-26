from tkinter import *
from Tkinter import MainWindow 
from PIL import Image,ImageTk
import os
import matplotlib.pyplot as plt
import numpy
import sys
import gc
import time
# from hello_4 import MainWindow
gc.enable()

def crop(x1,x2,y1,y2,filename,im,count):
    # print x1,y1,x2,y2
    c1,c2=(x1+x2)/2,(y1+y2)/2
    #print c1,c2
    i=min(abs(x2-x1),abs(y2-y1))
    for i in range(min(abs(x2-x1),abs(y2-y1)),max(abs(x2-x1),abs(y2-y1))):
        if c1+(i/2)==423 or c1-(i/2)==0 or c2+(i/2)==423 or c2-(i/2)==0:
            break
    #print i
        # im.crop((c1-(i/2),c2-(i/2),c1+(i/2),c2+(i/2))).save("crops/"+filename+'_crop_'+str(2)+'.png')
        # os.remove("../images_training_rev1/"+filename)
    # print "Saving:",filename+'_crop_'+str(count)+'.png'

def blacken(x1,x2,y1,y2,pix):
    for i in range(x1,x2):
                for j in range(y1,y2):
                        pix[i,j]=0
    return pix

def get_region(visited,x_curr,y_curr,pix,depth,changes):
    stack=[]
    visited,stck=get_neighbours(visited,x_curr,y_curr,pix,depth,changes)
    stack=stack+stck
    while len(stack):
        x,y,d=stack.pop(0)
        if len(changes[0])==d:
            changes[0].append([])
        changes[0][d].append((x,y))
        visited,stck=get_neighbours(visited,x,y,pix,d,changes)
        stack=stack+stck
    return visited
            
def get_neighbours(visited,x_curr,y_curr,pix,depth,changes):
    stack=[]
    if pix[x_curr,y_curr]>20:
        for i in (-1,0,1):
                for j in (-1,0,1):
                    if x_curr+i<424 and x_curr+i>0 and y_curr+j<424 and y_curr+j>0 and visited[x_curr+i][y_curr+j]==0:
                        visited[x_curr+i][y_curr+j]=1
                        stack.append((x_curr+i,y_curr+j,depth+1))
    else:
        if depth not in changes[1].keys():
            changes[1][depth]=[]
        changes[1][depth].append((x_curr,y_curr))
    return visited,stack

def get_window_dimensions(x_curr,y_curr,im,pix,avg_intensity,filename):
    visited=[[0 for i in range(424)]for j in range(424)]
    inside=[[(212,212)]]
    ends={}
    changes=[inside,ends]
    visited=get_region(visited,x_curr,y_curr,pix,0,changes)
    global visualize
    if visualize&4>0:
        root = Tk()
        x=MainWindow(root,numpy.array(im),changes,filename)
        root.mainloop()
    xmin=5000
    xmax=-1000
    ymin=5000
    ymax=-1000
    cntv=0
    for i in range(424):
        for j in range(424):
            if visited[i][j]==1:
                cntv+=1
                xmin=min(xmin,i)
                ymin=min(ymin,j)
                xmax=max(xmax,i)
                ymax=max(ymax,j)
    if cntv!=0:
        return xmin,xmax,ymin,ymax
    else:
        return 100,100,100,100

def cut_window(x_curr,y_curr,filename,im,pix,count,avg_intensity):
    x1,x2,y1,y2=get_window_dimensions(x_curr,y_curr,im,pix,avg_intensity,filename)
    pix=blacken(x1,x2,y1,y2,pix)
    if (x2-x1)*(y2-y1)>=2500:
            count+=1
            #crop(x1,x2,y1,y2,filename,im,count)
            border_pix=numpy.array(im)
            for k in range(y1,y2):
                    border_pix[x1,k] = (255,255,255)
                    border_pix[x2,k] = (255,255,255)
            for k in range(x1,x2):
                    border_pix[k,y1] = (255,255,255)
                    border_pix[k,y2] = (255,255,255)
            global visualize
            if visualize&2>0:
                border_plot = plt.imshow(border_pix)
                plt.show()
                plt.clf()
    return pix,count

def run_beta_run(rem):
    cnt=0
    global avg_intensity,max_intensity,threshold
    files=os.listdir("../images_training_rev1")
    for file_no in range(len(files)):
        cnt+=1
        print(rem,cnt)
        avg_intensity=float(0)
        max_intensity=float(0)
        filename=files[file_no]
        #"243217.jpg"
        im = Image.open("../images_training_rev1/"+filename)
        pix=numpy.array(im.convert("L"))
        x,y=im.size
        dense_bd=10
        max_cb=0
        tot_intensity=0
        for i in range(x):
            for j in range(y):
                    tot_intensity+=pix[i,j]
                    if pix[i,j]>max_intensity:
                            max_intensity=pix[i,j]
        avg_intensity=float(tot_intensity)/(x*y)
        count=0
        print(max_intensity,avg_intensity)
        pix,count=cut_window(212,212,filename,im,pix,count,avg_intensity)
        """
        for i in range(x):
            for j in range(y):
                    if i<x-dense_bd and j<y-dense_bd:
                            current_box=0
                            points=0
                            for k in range(dense_bd):
                                    for l in range(dense_bd):
                                            current_box+=pix[i+k,j+l]
                                            points+=1                       
                            if float(current_box/points)>max_cb:
                                    max_cb=float(current_box/points)
                            if current_box/points>float(3*avg_intensity):
                                    pix,count=cut_window(i+5,j+5,filename,im,pix,,avg_intensity)
                                    global visualize
                                    if visualize&1>0:
                                        imgplot = plt.imshow(pix,cmap='gray')
                                        plt.show()
                                        plt.clf()
        """
        im.close()

visualize=4
run_beta_run(0)
