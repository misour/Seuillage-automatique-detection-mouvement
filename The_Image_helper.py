import cv2
import numpy as np
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

import The_Helper
from The_Helper import ButtonHoverable

# #4584db  #92d3f4  #fad12b


class ImageProcessor:
    file_O=0
    def __init__(self, frame):
        self.frame = frame
        self.frame_layout()
        self.set_frames()
        self.set_widgets()
    def frame_layout(self):
        self.frame.rowconfigure(0, weight=6 ,minsize = 300)   # 50% of the height
        self.frame.rowconfigure(1, weight=4,minsize = 200)   # 50% of the height
        self.frame.columnconfigure(0, weight=1,minsize = 160) # 20% of width
        self.frame.columnconfigure(1, weight=4,minsize = 300) # 40% of width
        self.frame.columnconfigure(2, weight=4,minsize = 300) # 40% of width
    def set_frames(self):
        # Frame of the original image
        self.original_frame = tk.Frame(self.frame,border=1,relief=tk.FLAT)
        self.original_frame.grid(row=0, column=1, sticky='nsew')
        self.filtered_frame = tk.Frame(self.frame, width=150,height=200,border=1,relief=tk.FLAT)
        self.filtered_frame.grid(row=0, column=2, sticky='nsew')
        self.Text_original = tk.Label(self.original_frame,text = "l'image originale",font = "Calibri 18 bold")
        
        # Canvas of the original image
        self.canvas_originale = tk.Canvas(self.original_frame, width=300, height=300, bg='#BDD4F2')
        
        # Frame of histogram
        self.histogram_canva = tk.Canvas(self.frame, width=300, height=300, bg='#A9BED9')
        self.histogram_canva.grid(row=1, column=1, columnspan=2, sticky='nsew')
        # Frame of the filtred image
        self.Text_filtred = tk.Label(self.filtered_frame,text = "l'image filtre",font = "Calibri 18 bold")
        self.canvas_filtered = tk.Canvas(self.filtered_frame, width=300, height=300, bg='#BDD4F2')
    def open_image(self):
        # Open a file dialog to select an image
        global old_file_path
        global file_path
        file_path = filedialog.askopenfilename()
                    
        if file_path!='' and ImageProcessor.file_O==0 :
            ImageProcessor.file_O+=1
            old_file_path=file_path
        if  ImageProcessor.file_O!=0 :
            if file_path!='' :
                old_file_path=file_path 
                # Load the image using OpenCV
                img = cv2.imread(file_path)
                img = The_Helper.resizer(img)
                
                # Convert the OpenCV image to a Tkinter PhotoImage
                img_tk = tk.PhotoImage(data=cv2.imencode('.png', img)[1].tobytes())
                # center + Add image to canvas
                self.canvas_originale.create_image(
                    (int(self.canvas_originale["width"])  - img_tk.width()) // 2, 
                    (int(self.canvas_originale["height"]) - img_tk.height()) // 2, 
                    image=img_tk, 
                    anchor="nw")
                # Display the image on the canvas_originale
                self.canvas_originale.img_tk  = img_tk
                
                # Display the image on the canvas_filtered
                self.canvas_filtered.img_tk = img_tk
                self.canvas_filtered.create_image(
                    (int(self.canvas_originale["width"])  - img_tk.width()) // 2, 
                    (int(self.canvas_originale["height"]) - img_tk.height()) // 2, 
                    image=img_tk, 
                    anchor="nw")
                self.histogram_canva.delete("all")
                
                self.telecharger_button.pack(side="bottom",pady=10, anchor=tk.CENTER)

            else : file_path=old_file_path
        

        # Functions to apply a filter to the image and update the canvas_filtered
    
    def apply_seuille(self):
        if ImageProcessor.file_O!=0 :
            # Get the current image on the canvas
            # img_tk = self.canvas_filtered.img_tk
            
            img = cv2.imread(file_path)
            
            img = The_Helper.resizer(img)
            
            img_tk = The_Helper.seuilag_binaire(img,self.slider.get())

            # Display the filtered image on the canvas
            self.canvas_filtered.img_tk = img_tk
            self.canvas_filtered.create_image(
                    (int(self.canvas_filtered["width"]) - img_tk.width() )// 2, 
                    (int(self.canvas_filtered["height"]) // 2) - img_tk.height() // 2, 
                    image=img_tk, 
                    anchor="nw")
    def symetriser(self):
        if ImageProcessor.file_O!=0 :
            # img_tk = self.canvas_filtered.img_tk
            
            img = cv2.imread(file_path)
            
            # image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
            img = The_Helper.resizer(img)
            
            img_tk = The_Helper.symetrie_image(img)
            self.canvas_filtered.img_tk = img_tk
            self.canvas_filtered.create_image(
                    (int(self.canvas_filtered["width"]) - img_tk.width() )// 2, 
                    (int(self.canvas_filtered["height"]) // 2) - img_tk.height() // 2, 
                    image=img_tk, 
                    anchor="nw")
    def inverser(self):
        if ImageProcessor.file_O!=0 :
            # img_tk = self.canvas_filtered.img_tk
            
            img = cv2.imread(file_path)
            
            img = The_Helper.resizer(img)
            
            img_tk = The_Helper.reverse_pixels(img)
            self.canvas_filtered.img_tk = img_tk
            self.canvas_filtered.create_image(
                    (int(self.canvas_originale["width"]) // 2) - img_tk.width() // 2, 
                    (int(self.canvas_originale["height"]) // 2) - img_tk.height() // 2, 
                    image=img_tk, 
                    anchor="nw")
    def draw_histo(self):
        # Load an image and compute its grayscale histogram
        img = cv2.imread(file_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        hist, bins = np.histogram(gray.ravel(), 256, [0, 256])
        self.histogram_canva.delete("all")
        # Draw the x-axis of the histogram
        self.histogram_canva.create_line(50, 250, 400, 250, width=2)
        for i in range(0, 288, 32):
            x = int(i * 300 / 256) + 50
            self.histogram_canva.create_line(x, 250, x, 260, width=2)
            self.histogram_canva.create_text(x, 270, text=str(i), anchor="n")
        # Draw the y-axis of the histogram
        self.histogram_canva.create_line(50, 250, 50, 50, width=2)
        for i in range(0, 201, 50):
            y = int((1 - i / 200) * 200) + 50
            self.histogram_canva.create_line(40, y, 50, y, width=2)
            self.histogram_canva.create_text(30, y, text=str(i/200), anchor="e")
        # Draw the bars of the histogram with accumulation
        acc_count = 0
        somme=np.sum(hist)
        point_max=0
        list_coordonne=[]
        for i, count in enumerate(hist):
            acc_count += count
            d=y
            x = int(i * 300 / 256) + 50
            y = int((1 - acc_count / somme) * 200) + 50
            d=y-d
            list_coordonne.append((x-50,y-250))
            self.histogram_canva.create_rectangle(x, y, x,y-d, fill="blue")
            d=y
            if acc_count==somme and point_max==0 :
                point_max+=1
                self.histogram_canva.create_line(x,y,50,250, width=2,fill="red")
                self.histogram_canva.create_text(x+30, y+20, text=str("y=a.x"), anchor="e",fill="red")
    def apply_seuille_automatique(self):
    # Get the current image on the canvas
        
        # img_tk = self.canvas_filtered.img_tk
    
        img = cv2.imread(file_path)
        
        img = The_Helper.resizer(img)
        seuil=The_Helper.seuillage_automatique(img)
        img_tk = The_Helper.seuilag_binaire(img,seuil)
        self.canvas_filtered.img_tk = img_tk
        self.canvas_filtered.create_image(
                    (int(self.canvas_originale["width"]) // 2) - img_tk.width() // 2, 
                    (int(self.canvas_originale["height"]) // 2) - img_tk.height() // 2, 
                    image=img_tk, 
                    anchor="nw")
    def save_tkinter_image(self):
        # Prompt the user to select a save location
        file_pa = filedialog.asksaveasfilename(defaultextension=".png",
                                                filetypes=[("PNG Image", "*.png"), ("JPEG Image", "*.jpg")])
        # If the user cancels the save dialog or doesn't provide a file path, return without saving
        if not file_pa:
            return

        # Convert the Tkinter image to a PIL image
        pil_image = ImageTk.getimage(self.canvas_filtered.img_tk)

        # Save the PIL image to the specified file path
        pil_image.save(file_pa)

        print("Image saved successfully at:", file_pa)
    def set_widgets(self):
            # Navigation bar to get the seuille 
        self.nav_bar = tk.Frame(self.frame, width=150,height=200,border=1,relief=tk.RIDGE)
        self.nav_bar.grid(row=0, column=0, rowspan=2, sticky='nsew')

        # self.open_button = tk.Button(self.nav_bar, text='Open Image', command=self.open_image,font = "Calibri 10")
        self.open_button = ButtonHoverable(
            self.nav_bar,
            text='Open Image', 
            command=self.open_image,
            padx=6,
            pady=10,
            bg="#fad12b",
            back_color="lightgray",
            hov_color="#fad12b", 
            font=("Calibri", 12,"bold"))
        self.open_button.pack(pady=10)

        self.seuillage_frame = tk.Frame(
            self.nav_bar, 
            width=150,
            height=200,
            border=2,
            pady=15,
            relief=tk.GROOVE,
            bg='#084594')

        self.Text_seuillage = tk.Label( 
            self.seuillage_frame,
            text= "Seuillage manuel",
            font = "Calibri 18 bold",
            bg= '#084594',
            fg='white')
        self.slider = Scale(
            self.seuillage_frame, 
            from_=1, 
            to=254, 
            orient=HORIZONTAL, 
            length=250, 
            width=10, 
            fg='white',
            sliderlength = 10 , 
            troughcolor = 'white',
            sliderrelief='ridge',
            bg='#084594', 
            font=("Calibri", 12,"bold"))
        self.filter_button = tk.Button(
            self.seuillage_frame, 
            text='Apply seuille', 
            command=self.apply_seuille)
        
        
        # Frame of Options
        self.frame_option=tk.Frame(
            self.nav_bar,
            border=2,
            relief=tk.FLAT,
            borderwidth=2)
        options= [
            'Symetriser',
            'Inverser',
            'Histogramme',
            'Seuiller Auto',
            ]
        self.clicked = StringVar()
        self.clicked.set(options[0])

        self.drop =OptionMenu(
            self.frame_option,
            self.clicked,
            *options)
        self.drop.config(
            font=("Calibri", 12),
            background="#92d3f4",
            pady=8,
            padx=6)
        self.Butoon_apply = ButtonHoverable(
            self.frame_option,
            text="Apply",
            command=self.apply,
            bg="#92d3f4",
            back_color="white",
            hov_color="#92d3f4", 
            font=("Calibri", 12),
            pady=5.5,
            padx=5)
        self.telecharger_button = ButtonHoverable(
            self.nav_bar, 
            text='Telecharger image',
            command=lambda: self.save_tkinter_image(),
            bg="#92d3f4",
            back_color="white",
            hov_color="#92d3f4", 
            font=("Calibri", 12),
            pady=5.5,
            padx=5)
        self.Butoon_apply.config(background="#92d3f4")
        # Function to open an image file and display it on the canvas
    def apply(self):
        if self.clicked.get()=='Histogramme' :
            self.draw_histo()
        elif self.clicked.get()=='Symetriser' :
            self.symetriser()
        elif self.clicked.get()=='Inverser' :
            self.inverser()
        else : self.apply_seuille_automatique()
            

        #packing 
    def run(self):
        #nav_bar.pack()
            self.Text_seuillage.pack()
            self.slider.pack(pady=10)
            self.filter_button.pack(pady=10)
            self.frame_option.pack(fill='both',padx=10)
            # self.drop.grid(row=0,column=1,padx=10,pady=10)
            # self.Butoon_apply.grid(row=0,column=2,padx=10,pady=10)
            self.drop.pack(side="left",padx=10,pady=10)
            self.Butoon_apply.pack(side="right",padx=10,pady=10)
            self.seuillage_frame.pack()
            
            
            #Canvas originale.pack()
            self.Text_original.pack()
            self.canvas_originale.pack()
            #canvas.filtred.pack()
            self.Text_filtred.pack(side='top')
            self.canvas_filtered.pack(side='top')
            # if :


            
            
            






