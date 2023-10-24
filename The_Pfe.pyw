import tkinter as tk
from tkinter import ttk

# import The_Image
import The_Image_helper
import The_Video_helper

root = tk.Tk()
root.title("Seuillage automatique Image_Video")
root.geometry('860x680+20+10')
tab_control = ttk.Notebook(root)
# Create the first tab
tab_image = ttk.Frame(tab_control)
tab_control.add(tab_image, text="Traitement Image")

# Create the second tab
tab_video = ttk.Frame(tab_control)
tab_control.add(tab_video, text="Traitement Video")
tab_control.pack(expand=1, fill="both")

tab_control.configure(style="style.TNotebook")
style = ttk.Style()
style.theme_create("style", parent="alt", settings={
    "TNotebook": {"configure": {"tabmargins": "auto"}},
    "TNotebook.Tab": {"configure": {"padding": [5, 5], "background": "white","font":("Calibri Bold", 12)},
                        "map": {"background": [("selected", "#084594")],
                        "foreground": [("selected", "white")],
                        "expand": [("selected", [0, 0, 0, 0])]}}})
style.theme_use("style")

# START IMAGE
tab_image = The_Image_helper.ImageProcessor(tab_image)  # Create an instance of The_Image.App within the tab_image frame
tab_image.run()
# END IMAGE

# START VIDEO

tab_video= The_Video_helper.Video(tab_video)

# END VIDEO


root.mainloop()