from tkinter import *
import numpy as np
from PIL import Image
from PIL import ImageTk
import time
import copy

#----------------------------------------------------------------------

class MainWindow():

    #----------------

    def __init__(self,main,pix,changes,filename):

        # canvas for image
        self.canvas = Canvas(main, width=424, height=424)
        self.canvas.grid(row=0, column=0)
        self.filename=filename

        # images
        self.im=Image.fromarray(pix.astype('uint8'))
        self.photo = ImageTk.PhotoImage(image=self.im)
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor = NW,image = self.photo )
        self.depth=0
        self.bounds=[]
        main.after(10,self.onButton,main,pix,changes)
        #main.after(1,self.onButton,main,pix)# button to change image
        main.update()
    #----------------
    def quitter(self,main):
        #SAVES FILE
        # self.canvas.postscript(file="tk"+self.filename, colormode='color')
        main.destroy()

    def onButton(self,main,pix,changes):
        if len(changes[0])>0:
            pix_copy=copy.copy(pix)
            now=changes[0].pop(0)
            if self.depth in changes[1].keys():
                for i in changes[1][self.depth]:
                    self.bounds.append(i)
            for i in now:
                x1,y1=i
                pix_copy[x1][y1]=(0,0,0)
            for i in self.bounds:
                x1,y1=i
                pix_copy[x1][y1]=(255,0,0)
            self.im=Image.fromarray(pix_copy.astype('uint8'))
            self.photo = ImageTk.PhotoImage(image=self.im)
            self.canvas.itemconfig(self.image_on_canvas, image = self.photo)
            self.depth+=1
            main.after(10,self.onButton,main,pix,changes)
        else:
            main.after(500,self.quitter,main)

#----------------------------------------------------------------------
"""
root = Tk()
pix=np.array([[(i,j,255) for i in range(256)] for j in range(255,-1,-1)])
x=MainWindow(root,pix)
root.mainloop()
"""
