"""
Author      : Jimmy LAM
Date        : 24.11.2023
Version     : v1
"""

import tkinter as tk
import random
from math import sqrt
import time
import datetime
from database import save_game
from tkinter.messagebox import *

# Main window
# graphical variables
canvas_length = 1000  # canvas length
canvas_height = 500  # canvas height
target_x = 10  # x & y to find
target_y = 10
scale = 47.5  # 100 pixels for x=1
my_circle = None  # object used for the red circle
duration_s = None

# Important data (to save)
user_pseudo = "Gaston"  # provisional pseudo for the user
exercise_code = "GEO01"
total_trials = 0  # number of total trials
successful_trials = 0  # number of successful trials
base_results = []

def insert_results():
    results = [entry_user_pseudo.get(), datetime.datetime.now(), lbl_duration['text'], exercise_code, successful_trials, total_trials]
    save_game(results)

# On canvas click, check if succeeded or failed
def canvas_click(event):
    global my_circle, total_trials, successful_trials
    # x and y clicked
    click_x = (event.x - canvas_length / 2) / scale
    click_y = -(event.y - canvas_height / 2) / scale

    # Distance between clicked and (x, y)
    dx = abs(click_x - target_x)
    dy = abs(click_y - target_y)
    d = sqrt((dx) ** 2 + (dy) ** 2)  # Pythagorean theorem

    # Display a red circle where clicked (global variable my_circle)
    my_circle = circle(target_x, target_y, 0.5, "red")

    # Check succeeded or failed
    total_trials += 1
    if d > 0.5:
        window.configure(bg="red")
    else:
        window.configure(bg="green")
        successful_trials += 1
    lbl_result.configure(text=f"{user_pseudo} Essais réussis : {successful_trials} / {total_trials}")
    window.update()
    time.sleep(1)  # Delay 1s
    next_point(event=None)


def circle(x, y, r, color):
    # Circle, center x & y, r radius, color
    my_circle = canvas.create_oval(
        (x - r) * scale + canvas_length / 2, -(y - r) * scale + canvas_height / 2,
        (x + r) * scale + canvas_length / 2, -(y + r) * scale + canvas_height / 2, fill=color
    )
    return my_circle


def next_point(event):
    global target_x, target_y, my_circle
    window.configure(bg=hex_color)  # Reset color to normal
    print("next_point " + str(event))
    # Clearing the canvas
    canvas.delete('all')

    # x & y axis
    canvas.create_line(0, canvas_height / 2, canvas_length, canvas_height / 2, fill="black")  # x
    canvas.create_line(canvas_length / 2, 0, canvas_length / 2, canvas_height, fill="black")  # y
    # Graduation -10 +10
    for i in range(-10, 11, 5):
        canvas.create_line(canvas_length / 2 + i * scale, canvas_height / 2 - 10,
                           canvas_length / 2 + i * scale, canvas_height / 2 + 10, fill="black")  # on x
        canvas.create_text(canvas_length / 2 + i * scale, canvas_height / 2 + 20, text=i, fill="black",
                           font=("Helvetica 15"))
    for i in range(-5, 6, 5):
        canvas.create_line(canvas_length / 2 - 10, canvas_height / 2 + i * scale,
                           canvas_length / 2 + 10, canvas_height / 2 + i * scale, fill="black")  # on y
        canvas.create_text(canvas_length / 2 - 20, canvas_height / 2 + i * scale, text=i, fill="black",
                           font=("Helvetica 15"))

    # x & y random
    target_x = round(random.uniform(-10, 10), 0)
    target_y = round(random.uniform(-5, 5), 0)

    # Display x & y, 1 decimal
    lbl_target.configure(text=f"Cliquez sur le point ({round(target_x, 1)}, {round(target_y, 1)}). Echelle x -10 à +10, y-5 à +5")

def display_timer():
    global duration_s
    duration = datetime.datetime.now() - start_date  # elapsed time since beginning, in time with decimals
    duration_s = int(duration.total_seconds())  # idem but in seconds (integer)
    # Display min:sec (00:13)
    lbl_duration.configure(
        text="{:02d}".format(int(duration_s / 60)) + ":" + "{:02d}".format(duration_s % 60))

    window.after(1000, display_timer)  # recommencer après 15 ms
    return duration_s


window = tk.Tk()
window.title("Exercice de géométrie")
window.geometry("1100x900")

# Color definition
rgb_color = (139, 201, 194)
hex_color = '#%02x%02x%02x' % rgb_color  # Translation in hexa
window.configure(bg=hex_color)

# Canvas creation
lbl_title = tk.Label(window, text=f"{exercise_code}", font=("Arial", 15))
lbl_title.grid(row=0, column=1, padx=5, pady=5)

lbl_duration = tk.Label(window, text="0:00", font=("Arial", 15))
lbl_duration.grid(row=0, column=2, ipady=5, padx=10, pady=10)

tk.Label(window, text='Pseudo:', font=("Arial", 15)).grid(row=1, column=0, padx=5, pady=5)
entry_user_pseudo = tk.Entry(window, font=("Arial", 15))
entry_user_pseudo.grid(row=1, column=1)

lbl_result = tk.Label(window, text=f"Essais réussis : 0/0", font=("Arial", 15))
lbl_result.grid(row=1, column=3, padx=5, pady=5, columnspan=4)

lbl_target = tk.Label(window, text="", font=("Arial", 15))
lbl_target.grid(row=2, column=0, padx=5, pady=5, columnspan=6)

canvas = tk.Canvas(window, width=canvas_length, height=canvas_height, bg="#f9d893")
canvas.grid(row=4, column=0, padx=5, pady=5, columnspan=6)
btn_next = tk.Button(window, text="Suivant", font=("Arial", 15))
btn_next.grid(row=5, column=0, padx=5, pady=5, columnspan=6)


def on_finish_button_click():
    insert_results()
    window.destroy()


btn_finish = tk.Button(window, text="Terminer", font=("Arial", 15), command=on_finish_button_click)
btn_finish.grid(row=6, column=0, columnspan=6)

next_point(event=None)
start_date = datetime.datetime.now()
display_timer()

# Binding actions 
canvas.bind("<Button-1>", canvas_click)
btn_next.bind("<Button-1>", next_point)

# Main loop
window.mainloop()
