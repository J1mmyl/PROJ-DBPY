"""
Author      : Jimmy LAM
Date        : 24.11.2023
Version     : v1
"""

import tkinter as tk
import random
from math import pow
import time
import database
import datetime
from database import save_game
from tkinter.messagebox import *

# Important data (to save)
user_pseudo = "Gaston"  # provisional pseudo for the user
exercise_code = "INFO02"
total_trials = 0  # number of total trials
successful_trials = 0  # number of successful trials

# Liaison entre le canvas et le code
units = ["B", "kB", "MB", "GB", "TB"]
value_to_convert = 0  # valeur à convertir
original_unit = units[0]
converted_value = 0  # valeur à convertir
target_unit = units[0]
conversion_ratio = 0
base_results = []

def next_conversion(event):
    global value_to_convert, original_unit, target_unit, conversion_ratio
    window.configure(bg=hex_color)

    value_to_convert = round(random.random(), 3)
    dec = random.randint(0, 3)
    for i in range(dec):
        value_to_convert *= 10
    value_to_convert = round(value_to_convert, 3)
    p1 = random.randint(1, 4)
    original_unit = units[p1]
    p2 = p1
    while p1 == p2:
        p2 = random.randint(0, 4)
    target_unit = units[p2]
    conversion_ratio = pow(10, 3 * (p2 - p1))
    label_value_to_convert.configure(text=f" {value_to_convert} {original_unit} =")
    label_target_unit.configure(text=f" {target_unit} ")
    entry_converted_value.delete(0, 'end')

def insert_results():
    results = [entry_user_pseudo.get(), datetime.datetime.now(), lbl_duration['text'], exercise_code, successful_trials, total_trials]
    save_game(results)

def test(event):
    global converted_value, successful_trials, total_trials
    # Fonction pour tester si la valeur est juste
    converted_value = float(entry_converted_value.get().replace(" ", ""))
    total_trials += 1
    success = (abs(value_to_convert / converted_value / conversion_ratio - 1) < 0.01)  # Tolerance 1%
    if success:
        successful_trials += 1
        window.configure(bg="green")
    else:
        window.configure(bg="red")
    lbl_result.configure(text=f"Essais réussis : {successful_trials} / {total_trials}")
    window.update()
    time.sleep(1)  # Delai 1s
    next_conversion(event=None)

def display_timer():
    duration = datetime.datetime.now() - start_date  # elapsed time since beginning, in time with decimals
    duration_s = int(duration.total_seconds())  # idem but in seconds (integer)
    # display min:sec (00:13)
    lbl_duration.configure(text="{:02d}".format(int(duration_s / 60)) + ":" + "{:02d}".format(duration_s % 60))
    window.after(1000, display_timer)  # recommencer après 15 ms

window = tk.Tk()
window.title("Conversion d'unités")
window.geometry("1100x900")
window.grid_columnconfigure((0, 1, 2), minsize=150, weight=1)

# Color definition
rgb_color = (139, 201, 194)
hex_color = '#%02x%02x%02x' % rgb_color  # Translation in hexa
window.configure(bg=hex_color)

lbl_title = tk.Label(window, text=f"{exercise_code}", font=("Arial", 15))
lbl_title.grid(row=0, column=0, columnspan=3, ipady=5, padx=20, pady=20)
lbl_duration = tk.Label(window, text="0:00", font=("Arial", 15))
lbl_duration.grid(row=0, column=2, ipady=5, padx=10, pady=10)

tk.Label(window, text='Pseudo:', font=("Arial", 15)).grid(row=1, column=0, padx=5, pady=5)
entry_user_pseudo = tk.Entry(window, font=("Arial", 15))
entry_user_pseudo.grid(row=1, column=1)

lbl_result = tk.Label(window, text=f"{user_pseudo}  Essais réussis : 0/0", font=("Arial", 15))
lbl_result.grid(row=1, column=2, columnspan=3, ipady=5, padx=20, pady=20)

label_value_to_convert = tk.Label(window, text="Valeur à convertir:", font=("Arial", 15))
label_value_to_convert.grid(row=2, column=0, ipady=5, padx=20, pady=20, sticky='E')

entry_converted_value = tk.Entry(window, font=("Arial", 15))
entry_converted_value.grid(row=2, column=1, ipady=5, padx=5, pady=20, sticky='E')

label_target_unit = tk.Label(window, text="Unité cible:", font=("Arial", 15))
label_target_unit.grid(row=2, column=2, ipady=5, padx=5, pady=20, sticky='W')

btn_next = tk.Button(window, text="Suivant", font=("Arial", 15))
btn_next.grid(row=3, column=0, columnspan=3, ipady=5, padx=5, pady=5)


def on_finish_button_click():
    insert_results()
    window.destroy()


btn_finish = tk.Button(window, text="Terminer", font=("Arial", 15), command=on_finish_button_click)
btn_finish.grid(row=6, column=0, columnspan=6)

start_date = datetime.datetime.now()
display_timer()
# First call of next_conversion
next_conversion(event=None)

# Binding actions (entry & buttons)
entry_converted_value.bind("<Return>", test)
btn_next.bind("<Button-1>", next_conversion)

# Main loop
window.mainloop()
