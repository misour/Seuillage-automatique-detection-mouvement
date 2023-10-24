import math
import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk


def nbarray_to_tk_image(img_in):
    # Convert NumPy array to PIL Image
    pil_image = Image.fromarray(img_in)    
    # Convert PIL Image to Tkinter PhotoImage
    tk_img = ImageTk.PhotoImage(pil_image)
    return tk_img

def seuilag_binaire(img_in,seuil):
    img = cv2.cvtColor(img_in, cv2.COLOR_BGR2GRAY)
    matrice = img.copy()
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i][j]>seuil :
                matrice[i][j] = 255
            else :  matrice[i][j] = 0
    return nbarray_to_tk_image(matrice)

def reverse_pixels(img):
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img[i][j] = (255 - img[i][j]) 
    return  nbarray_to_tk_image(img)

def symetrie_image(img):
    matrice = img.copy()
    for i in range(img.shape[0]):
        j=0
        while j < img.shape[1] :
            matrice[i][j] = img[i][img.shape[1]-j-1]
            j+=1
    return  nbarray_to_tk_image(matrice)

def Generate_Histo(path):
    
    # Load an image and compute its grayscale histogram
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hist, bins = np.histogram(gray.ravel(), 256, [0, 256])

    # Create a canvas to draw on
    canvas = tk.Canvas(width=300, height=300)

    # Draw the x-axis of the histogram
    canvas.create_line(50, 250, 350, 250, width=2)
    for i in range(0, 256, 32):
        x = int(i * 300 / 256) + 50
        canvas.create_line(x, 250, x, 260, width=2)
        canvas.create_text(x, 270, text=str(i), anchor="n")

    # Draw the y-axis of the histogram
    canvas.create_line(50, 250, 50, 50, width=2)
    for i in range(0, 201, 50):
        y = int((1 - i / 200) * 200) + 50
        canvas.create_line(40, y, 50, y, width=2)
        canvas.create_text(30, y, text=str(i), anchor="e")

    # Draw the bars of the histogram
    max_count = np.max(hist)
    for i, count in enumerate(hist):
        x1 = int(i * 300 / 256) + 50
        x2 = int((i + 1) * 300 / 256) + 50
        y = int((1 - count / max_count) * 200) + 50
        canvas.create_rectangle(x1, y, x2, 250, fill="blue")
    return canvas


def resizer(img):
    height, width, _ = img.shape
    if width < height :
        aspect_ratio = float(width) / float(height)
        new_width = int( aspect_ratio * 300)
        # Resize the image to fit the desired width while keeping the aspect ratio
        img = cv2.resize(img, (new_width, 300))
    else:
        aspect_ratio = float(width) / float(height)
        new_height = int(float(300) / aspect_ratio)
        # Resize the image to fit the desired width while keeping the aspect ratio
        img = cv2.resize(img, (300, new_height))
    return img 

def equation_droite_origine(x1, y1):
    m = y1 / x1
    return m

def distance_droite_point(m, x2, y2):
    distance = abs(y2 - m * x2) / math.sqrt(1 + m**2)
    return distance

def point_max(histogram):
    acc_count=0
    k=()
    max=0
    list=[]
    somme=np.sum(histogram)
    for i, count in enumerate(histogram):
        list.append(acc_count)
        acc_count += count
        if acc_count==somme and max==0:
            k+=(i,acc_count)
            max+=1
    histogram_accumule=np.array(list)
            
    return [k,histogram_accumule]


def seuillage_automatique(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    histogram, _ = np.histogram(gray.ravel(), 256, [0, 256])
    coordonne,histogram_acc=point_max(histogram)
    ma=equation_droite_origine(coordonne[0],coordonne[1])
    max=0
    for i, count in enumerate(histogram_acc):
        if(distance_droite_point(m=ma,x2=max,y2=histogram_acc[max])<distance_droite_point(ma,i,count)):
            max=i 
    return max

def video_to_images(cap):
    images = []
    while True:
        ret, image = cap.read()
        if not ret:
            break
        images.append(image)
    # Release the VideoCapture object
    cap.release()
    
    return images

def array_to_video(image_array,fps):
    height, width,_ = image_array[0].shape
    # Define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video_writer = cv2.VideoWriter("m",fourcc, fps, (width, height))
    for image in image_array:
    # Write the image to the video
        video_writer.write(image)

    # Release the VideoWriter
    video_writer.release()
    return video_writer

def telecharger_viddeo(image_array, output_video_path, fps):
    height, width,_ = image_array[0].shape
    # Define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))
    for image in image_array:
    # Write the image to the video
       video_writer.write(image)

    # Release the VideoWriter
    video_writer.release()
    return video_writer

def calculate_differences_image(array):
    differences = []
    for i in range(len(array) - 1):
        diff =np.abs(array[i+1] - array[i])
        differences.append(diff)
    return differences

class VideoPlayer:
    def __init__(self, parent_frame,titre):
        self.parent_frame=parent_frame
        self.titre=tk.Label(self.parent_frame,text=titre,font = "Calibri 14 bold")
        self.titre.pack(side='top')
        self.canvas_video=tk.Canvas(self.parent_frame,
            width=500,
            height=260)
        self.canvas_video.pack()
        self.control=tk.Frame(self.parent_frame,border=1,height=40,relief=tk.RIDGE)
        self.control.pack(fill='both',side=tk.BOTTOM)
        
        self.play_button = tk.Button(self.control, text="Play",width=5,command=self.play_video)
        self.play_button.pack(side=tk.LEFT)
        
        self.pause_button = tk.Button(self.control, text="Pause", command=self.pause_video)
        self.pause_button.pack(side=tk.LEFT)
        
        
        self.slider = tk.Scale(self.control,length=500, from_=0,bg='white',border=1,activebackground='blue',width=10,borderwidth=0,
                                orient=tk.HORIZONTAL, command=self.update_video)
        self.slider.pack(fill="x")
        
        self.frame_index = 0
        self.is_playing = True
        
    def load_video(self,video_path):
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)
        self.video_fps = int(self.cap.get(cv2.CAP_PROP_FPS))
            
        self.video_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.video_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.slider.config(to=self.total_frames)
        self.update_frame()
        
    def update_frame(self):
        if self.is_playing:
            ret, frame = self.cap.read()
            if ret:
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                photo=nbarray_to_tk_image(image)
                self.canvas_video.create_image(0, 0, image=photo, anchor=tk.NW)
                self.canvas_video.image = photo

                self.frame_index += 1
                if self.frame_index >= self.total_frames:
                    self.frame_index = 0
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                self.slider.set(self.frame_index)

        self.parent_frame.after(int(1000 / self.video_fps), self.update_frame)
        
        
        
    def filtre_Video(self,video_path):
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)
        self.video_fps = int(self.cap.get(cv2.CAP_PROP_FPS))
            
        self.video_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.video_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.slider.config(to=self.total_frames)
        ret,self.image_prec = self.cap.read()
        if ret :
            self.update_frame_filtred()
        
    def update_frame_filtred(self):
        if self.is_playing:
            ret, frame = self.cap.read()
            if ret:
                
                # image = np.abs(frame-self.image_prec)
                image = cv2.absdiff(frame,self.image_prec)
                img=cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                blur = cv2.GaussianBlur(img, (5, 5), 0)
                seuil, thresh = cv2.threshold(blur,seuillage_automatique(blur), 255, cv2.THRESH_BINARY)
                photo=nbarray_to_tk_image(thresh)
                # photo=seuilag_binaire(blur,10)
                self.image_prec=frame
                self.canvas_video.create_image(0, 0, image=photo, anchor=tk.NW)
                self.canvas_video.image = photo
                self.frame_index += 1
                if self.frame_index >= self.total_frames:
                    self.frame_index = 0
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                self.slider.set(self.frame_index)
    
        self.parent_frame.after(int(1000 / self.video_fps), self.update_frame_filtred)
        
    # def update_frame_filtred(self):
        
    #     if self.is_playing:
    #         ret, frame = self.cap.read()
    #         if ret:
    #             image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #             img=np.abs(image-self.image_prec)
    #             photo=nbarray_to_tk_image(img)
    #             self.image_prec=image
    #             self.canvas_video.create_image(0, 0, image=photo, anchor=tk.NW)
    #             self.canvas_video.image = photo
    #             self.frame_index += 1
    #             if self.frame_index >= self.total_frames:
    #                 self.frame_index = 0
    #                 self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    #             self.slider.set(self.frame_index)
    #     self.parent_frame.after(int(1000 / self.video_fps), self.update_frame_filtred)

    def play_video(self):
        if not self.is_playing:
            self.is_playing = True
    
    def pause_video(self):
        self.is_playing = False

    def update_video(self, frame_index):
        self.frame_index = int(frame_index)
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.frame_index)


class ButtonHoverable(tk.Button):
    def __init__(self, master=None, **kwargs):
        # Initialize the ButtonHoverable
        back_color = kwargs.pop('back_color', None)
        hov_color = kwargs.pop('hov_color', None)
        fg_hov = kwargs.pop('fg_hov', None)
        
        tk.Button.__init__(self, master, **kwargs)
        
        # Bind functions to button events
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        
        self.background = back_color
        self.background_hover = hov_color
        self.forground_hover = fg_hov
        self.current_fg = self.cget("fg")
        

    def on_enter(self, event):
        # Change the button background color when hovered
        self.config(bg=self.background)
        self.config(fg=self.forground_hover)

    def on_leave(self, event):
        # Change the button background color back to default
        self.config(bg=self.background_hover)
        self.config(fg=self.current_fg)
