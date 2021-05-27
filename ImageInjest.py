from tkinter import *
from PIL import Image, ImageTk

# --- functions ---

def on_click(widget):
    print('clicked')
    widget['image'] = img2

# --- main ---
root = tk()
root.geometry('1000x1000')
canvas = Canvas(root,width=999,height=999)
canvas.pack()
pilImage = Image.open("ball.jpg")
image = ImageTk.PhotoImage(pilImage)
imagesprite = canvas.create_image(400,400,image=image)
root.mainloop()