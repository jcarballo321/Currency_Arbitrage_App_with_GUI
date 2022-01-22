from tkinter import *
from integrate_with_gui import main
from PIL import ImageTk, Image
import os


root = Tk()
root.title("Arbitrage App GUI")
root.iconbitmap()
#root.geometry("500 x 350")
a = main()
output = []

#This function passes the output from main function in integrate.py file
def submit():
    output = main()
   
    print(output)





my_img = Image.open("project_picture.png")

resized = my_img.resize((800, 600), Image.ANTIALIAS)

new_pic = ImageTk.PhotoImage(resized)

#my_img = ImageTk.PhotoImage(Image.open("project_picture.png"))
my_label = Label(root, image = new_pic)
my_label.pack(pady = 20)

#The frame for the output
frame = Frame(root, bg = 'black', bd = 5, name = "test") #08c1ff
frame.place(relx = 0.5, rely = 0.6, relwidth = 0.6, relheight = 0.2, anchor = 'n')


#Lopp that interates each line of output
for each_entry in a:
    label = Label(frame, text = each_entry)
    label.place(relwidth=1, relheight=1)
    label.pack(pady=5)
    



my_notification = Label(root, text = 'Follow the above Arbitrage Cycle', font = ("Helvetica", 12))
my_notification.pack(pady = 22)

#Begins Program
my_button = Button(root, text ="Refresh Program", command = submit())
my_button.pack(pady = 24)

#Ends Program
button_quit = Button(root, text = "Exit Program", command = root.quit)
button_quit.pack(pady = 20)

#Will casue the intigrate.py application to continuously run until stopped.
root.mainloop()

