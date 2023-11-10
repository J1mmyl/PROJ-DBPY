# Training (INFO05)
# JCY oct 23
# PRO DB PY
import math
import tkinter as tk
from tkinter.messagebox import showinfo          # Les alertes
import random
from math import cos, sin, pi
from colorsys import hsv_to_rgb, rgb_to_hsv
from math import sqrt
import time
import database
import datetime
from tkinter.messagebox import *

# Main window
# graphical variables
l = 850 # canvas length
height = 350 # canvas height
xmed=250 #middle of 2 color rectangles


#important data (to save)
pseudo="Gaston" #provisory pseudo for user
exercise="INFO05"
nbtrials=0 #number of total trials
nbsuccess=0 #number of successfull trials

#exercise data
rgb=[100,150,200]  #random color as list
rgb_response=[127,127,127] #grey at start, response color as list
rect_rgb=None #2 rectangles (200x200)
rect_response=None
rect_mini_rgb=None #min black rectangle on colorwheel
line_hor_response=None #little horizontal line for response cross on colorwheel
line_vert_response=None #little vertical line for response cross on colorwheel
lbl_distance=None #to display the distance between the 2 colors


#next color
def next_color(event):
    #random color to choose
    window.configure(bg=hex_color)
    entry_response.delete(0,tk.END)
    entry_response.insert(0,"#")
    global rgb
    rgb = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
    display();


#display the exercise and response
def display():
    global rect_rgb, rect_response,rect_mini_rgb, lbl_distance
    # 2 rectangles with color
    canvas.itemconfig(rect_rgb, fill=h_color(rgb))
    canvas.itemconfig(rect_response, fill=h_color(rgb_response))

    # black rectangle for random color in color wheel
    hsv=rgb_to_hsv(rgb[0],rgb[1],rgb[2]) #conversion rgb random in hsv (0-1)
    x = 3 * l / 4 + hsv[1] * 150 * cos(hsv[0]  * pi * 2)
    y = height / 2 + hsv[1] * 150 * sin(hsv[0]  * pi * 2)
    canvas.coords(rect_mini_rgb,  x - 2, y - 2,  x + 2, y + 2)

    # little cross for user color in color wheel
    hsv_response=rgb_to_hsv(rgb_response[0],rgb_response[1],rgb_response[2]) #conversion rgb_response random in hsv (0-1)
    x = 3 * l / 4 + hsv_response[1] * 150 * cos(hsv_response[0]  * pi * 2)
    y = height / 2 + hsv_response[1] * 150 * sin(hsv_response[0]  * pi * 2)
    canvas.coords(line_vert_response, x, y-8, x, y+8)
    canvas.coords(line_hor_response, x-8, y, x + 8, y)

    canvas.itemconfig(lbl_distance,text=f"Distance between the 2 colors: {dist_color(rgb,rgb_response)}")


# only called at the beginning
def display_wheel_color():

    global rect_mini_rgb, rect_rgb, rect_response, line_hor_response, line_vert_response, lbl_distance
    canvas.create_text(200, 20, text="Essayez de reproduire la couleur de gauche", fill="black", font=("Arial", 15))
    lbl_distance=canvas.create_text(200, 320, fill="black", font=("Arial", 15))

    # 2 rectangles with color (gray at beginning)
    rect_rgb = canvas.create_rectangle(xmed-200,height/2-100,xmed,height/2+100, fill="#888888",width=0)
    rect_response = canvas.create_rectangle(xmed,height/2-100,xmed+200,height/2+100, fill="#888888",width=0)

    #display the color wheel
    for s in range(0, 100, 2): #50 steps in s (radius)
        for h1 in range(0,200,1+int((100-s)/40)):#200 steps in h, optimization 6500 rectangles vs 10000
            h=h1/2
            rgbW=hsv_to_rgb(h/ 100, s/ 100, 1) #hsw avec v=100
            x=3 * l/ 4+ s/ 100 * 150 * cos(h/ 100 * pi * 2)
            y=height / 2 + s / 100 * 150 * sin(h / 100 * pi * 2)
            canvas.create_rectangle(x-3,y-3 , x+3, y+3, fill=h_color_float(rgbW),width=0)
    #display 3 lines (120° = 2*pi/3)
    for angle in range(3):
        anglerad = angle * pi * 2 / 3
        canvas.create_line(3 * l/ 4, height/ 2 , 3 * l/ 4+ 160 * cos(anglerad),height/ 2 +160 * sin(anglerad) )

    #display a black rectangle at the middle (will be repositionned by display())
    rect_mini_rgb=canvas.create_rectangle(0, 0, 0, 0, fill="#000000", width=0)
    line_hor_response = canvas.create_line(0, 0, 0, 0)  # little horizontal line for response cross on colorwheel
    line_vert_response = canvas.create_line(0, 0, 0, 0)  # little vertical line for response cross on colorwheel

#converts rgb (ex:[128,128,128]) in hex color (ex: #808080)
def h_color(rgb_color):
    return '#{:02x}{:02x}{:02x}'.format(rgb_color[0], rgb_color[1], rgb_color[2])


#converts rgb (ex:[0.5,0.5,0.5]) in hex color (ex: #808080)
def h_color_float(rgb_color_float):
    rgb_color=[0,0,0] # temp list
    for i,v in enumerate(rgb_color_float): #0-1 => 0-255
        rgb_color[i]=int(v*255)
    return h_color(rgb_color)


#converts hex color (ex: #808080) in rgb ([128,128,128])
def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    if lv==6 :
        return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
    else :
        return (-1,-1,-1) #if not 3 colors


#distance between 2 colors (Pythagore on 3 dimensions)
def dist_color(c1,c2):
    return int(sqrt( (c1[0]-c2[0])**2 +  (c1[1]-c2[1])**2 + (c1[2]-c2[2])**2 ) )


#check if the color given in hex is near (max dist=5)
def test(event):
    global nbsuccess, nbtrials
    # Fonction pour tester si la valeur est juste
    txt_color = entry_response.get().replace(" ", "") #delete spaces
    rgb_entry=hex_to_rgb(txt_color)
    success= (dist_color(rgb_entry,rgb) <=5 )
    nbtrials +=1
    if success:
        nbsuccess += 1
        window.configure(bg="green")
        window.update()
        time.sleep(1)  # delai 1s
        next_color(event=None)
    else:
        window.configure(bg="red")
        window.update()
    lbl_result.configure(text=f"{pseudo} Essais réussis : {nbsuccess} / {nbtrials}")


# change the value of r in rgb_response
def sl_r(value):
    global rgb_response
    rgb_response[0]=int(value)
    maxi = int(max(rgb_response[0], rgb_response[1], rgb_response[2]) / 2.55)
    slider_v.set(maxi)
    display()


# change the value of g in rgb_response
def sl_g(value):
    global rgb_response
    rgb_response[1] = int(value)
    maxi=int (max(rgb_response[0],rgb_response[1],rgb_response[2]) /2.55)
    slider_v.set(maxi)
    display()


# change the value of b in rgb_response
def sl_b(value):
    global rgb_response
    rgb_response[2] = int(value)
    maxi = int(max(rgb_response[0], rgb_response[1], rgb_response[2]) / 2.55)
    slider_v.set(maxi)
    display()


#change the value of v (hsv) in rgb_response
def sl_v(event):
    global rgb_response
    value=slider_v.get()
    hsv=rgb_to_hsv(rgb_response[0],rgb_response[1],rgb_response[2])
    rgb_response_tuple=hsv_to_rgb(hsv[0],hsv[1],int(value)/100)
    rgb_response[0]=int(rgb_response_tuple[0]*255)
    rgb_response[1]=int(rgb_response_tuple[1]*255)
    rgb_response[2]=int(rgb_response_tuple[2]*255)
    slider_r.set(rgb_response[0])
    slider_g.set(rgb_response[1])
    slider_b.set(rgb_response[2])
    display()


def save_game(event):
    print("dans save")
    #TODO


def display_timer():
    duration=datetime.datetime.now()-start_date #elapsed time since beginning, in time with decimals
    duration_s=int(duration.total_seconds()) #idem but in seconds (integer)
    #display min:sec (00:13)
    lbl_duration.configure(text="{:02d}".format(int(duration_s /60)) + ":" + "{:02d}".format(duration_s %60))
    window.after(1000,display_timer) #recommencer après 15 ms


window = tk.Tk()
window.title("La couleur perdue")
window.geometry("1100x900")

# color définition
rgb_color = (139, 201, 194)
hex_color = '#%02x%02x%02x' % rgb_color # translation in hexa
window.configure(bg=hex_color)

# Canvas creation
lbl_title = tk.Label(window, text=f"{exercise} : La couleur perdue", font=("Arial", 15))
lbl_title.grid(row=0,column=1, ipady=5, padx=10,pady=10)

lbl_duration = tk.Label(window, text="0:00", font=("Arial", 15))
lbl_duration.grid(row=0,column=2, ipady=5, padx=10,pady=10)

tk.Label(window, text='Pseudo:', font=("Arial", 15)).grid(row=1, column=0, padx=5, pady=5,sticky='E')
entry_pseudo = tk.Entry(window, font=("Arial", 15))
entry_pseudo.grid(row=1, column=1,sticky='W')

lbl_result = tk.Label(window, text=f"Essais réussis : 0/0", font=("Arial", 15))
lbl_result.grid( row=1, column=2, ipady=5, padx=20,pady=10)

canvas = tk.Canvas(window, width=l, height=height, bg="#f9d893")
canvas.grid( row=2, column=0, columnspan=3, ipady=5, padx=20,pady=5)

#frae
frame_response = tk.Frame(window)
frame_response.grid( row=3, column=0, columnspan=3, padx=20,pady=10)
lbl_response =tk.Label(frame_response, text="Couleur en hexa:", font=("Arial", 15))
lbl_response.grid( row=0, column=0, ipady=5, padx=10,pady=5,sticky='E')
entry_response = tk.Entry(frame_response,font=("Arial", 15))
entry_response.grid( row=0, column=1, ipady=5, padx=10,pady=5,sticky='W')

#sliders
slider_r = tk.Scale(window, from_=0, to=255, length=600, orient=tk.HORIZONTAL, troughcolor="red", command=sl_r)
slider_r.set(128)
slider_r.grid(row=4, column=0, columnspan=3, padx=10, pady=0)
slider_g = tk.Scale(window, from_=0, to=255,  length=600, orient=tk.HORIZONTAL, troughcolor="green",command=sl_g)
slider_g.set(128)
slider_g.grid(row=5,column=0,columnspan=3, padx=10,pady=0)
slider_b = tk.Scale(window, from_=0, to=255, length=600, orient=tk.HORIZONTAL, troughcolor="blue",command=sl_b)
slider_b.set(128)
slider_b.grid(row=6,column=0,columnspan=3, padx=10,pady=0)
slider_v = tk.Scale(window, from_=0, to=100, length=600, orient=tk.HORIZONTAL, troughcolor=h_color([127,127,127]))
slider_v.set(128)
slider_v.grid(row=7,column=0,columnspan=3, padx=10,pady=0)

btn_next =tk.Button(window, text="Suivant", font=("Arial", 15))
btn_next.grid( row=8, column=1, ipady=5, padx=20,pady=10)

btn_finish = tk.Button(window, text="Terminer", font=("Arial", 15))
btn_finish.grid(row=8, column=2)


# first call of next_point
display_wheel_color()
next_color(event=None)
start_date = datetime.datetime.now()
display_timer()

# Association de la fonction au clic sur le canvas
btn_next.bind("<Button-1>", next_color)
entry_response.bind("<Return>", test)
slider_v.bind("<ButtonRelease-1>", sl_v)
btn_finish.bind("<Button-1>", save_game)

# main loop
window.mainloop()
