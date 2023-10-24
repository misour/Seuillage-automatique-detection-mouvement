from tkinter import filedialog, ttk
import cv2
from PIL import Image,ImageTk
import tkinter as tk
import The_Helper
from The_Helper import ButtonHoverable


class Video:
    file_O=0
    def __init__(self, frame):
        self.frame = frame
        self.frame_layout()
        self.set_frames()
        self.set_widgets()
    def frame_layout(self):
        self.frame.rowconfigure(0, weight=5 ,minsize = 300)   # 50% of the height
        self.frame.rowconfigure(1, weight=5,minsize = 300)   # 50% of the height
        self.frame.columnconfigure(0, weight=1,minsize = 160) # 10% of width
        self.frame.columnconfigure(1, weight=9,minsize = 300) # 90% of width
        
    def set_frames(self):   
        # Frame of the originale video
        self.original_frame = tk.Frame(self.frame,border=1,relief=tk.FLAT)
        self.original_frame.grid(row=0, column=1, sticky='nsew')
        self.controlO=The_Helper.VideoPlayer(self.original_frame,"Video Originale")
        # Frame Of The Filtered Video
        self.filtered_frame = tk.Frame(self.frame,border=1,relief=tk.FLAT)
        self.filtered_frame.grid(row=1, column=1, sticky='nsew')
        self.controlF=The_Helper.VideoPlayer(self.filtered_frame,"Video Filtre")
        
        
        
    def set_widgets(self):
            # Navigation bar 
        self.nav_bar = tk.Frame(self.frame,border=1,relief=tk.RIDGE)
        self.nav_bar.grid(row=0, column=0, rowspan=2, sticky='nsew')
        self.open_button = ButtonHoverable(
            self.nav_bar, 
            text='Open Video', 
            command=self.open_image,
            padx=6,
            pady=10,
            bg="#fad12b",
            back_color="lightgray",
            hov_color="#fad12b", 
            font=("Calibri", 12,"bold"))
        self.open_button.pack(pady=10)
        self.filtre_button = ButtonHoverable(
            self.nav_bar, 
            text='Filtrer Video', 
            command=self.filtrer_video,
            bg="#92d3f4",
            back_color="white",
            hov_color="#92d3f4", 
            font=("Calibri", 12))
        self.filtre_button.pack(pady=10)

    def run(self): pass

    def open_image(self):
        # Open a file dialog to select an image
        global old_file_path
        global file_path
        global cap
        file_path = filedialog.askopenfilename()
                    
        if file_path!='' and Video.file_O==0 :
            Video.file_O+=1
            old_file_path=file_path
        if  Video.file_O!=0 :
            if file_path!='' :
                old_file_path=file_path 
                self.controlO.load_video(file_path)
            else : file_path=old_file_path
    def filtrer_video(self):
        if Video.file_O>0:
            self.controlF.filtre_Video(file_path)
       