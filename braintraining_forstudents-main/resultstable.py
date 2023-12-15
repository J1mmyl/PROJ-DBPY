"""
Author      : Jimmy LAM
Date        : 24.11.2023
Version     : v1
"""

from tkinter import *
from database import get_database_infos
import tkinter.font
import datetime
import mysql.connector
import pathlib
import csv

# identifiants mysql
config = {
  'user': 'root',
  'host': '127.0.0.1',
  'database': 'mygame',
  'raise_on_warnings': True,
  'autocommit': True,
  'buffered': True
}

# variables
num_lines = 0
total_time = None
num_ok = 0
num_total = 0
pourcent_total = 0
last_row_count = 0

# window's start
window = Tk()

# window's parameters
window.title("Affichage braintraining")
window.geometry("1100x900")

# color définition pour bg
rgb_color = (139, 201, 194)
hex_color = '#%02x%02x%02x' % rgb_color # translation en hexa
window.configure(bg=hex_color)

# function to show the results
def show_results():
    global results, num_lines, lvtot_lines, lvtot_pourcent_total, lvtot_num_ok, lvtot_num_total, lvtot_time, pseudo
    pseudo_value = e_pseudo.get()  # Get the value from the Entry widget
    results_infos = get_database_infos(pseudo_value)
    total_pourcentages = 0
    total_ok = 0
    total_trials = 0
    dates = datetime.timedelta(seconds=0)


    # vider labels
    for widget in results.winfo_children():
        widget.grid_forget()

    # Réafficher colonne
    l_column_id.grid(row=0, column=0, padx=(0, 10))
    l_column_student.grid(row=0, column=1, padx=(0, 10))
    l_column_date_hour.grid(row=0, column=2, padx=(0, 10))
    l_column_time.grid(row=0, column=3, padx=(0, 10))
    l_column_exo.grid(row=0, column=4, padx=(0, 10))
    l_column_num_ok.grid(row=0, column=5, padx=(0, 10))
    l_column_num_total.grid(row=0, column=6, padx=(0, 10))
    l_column_ok_ratio.grid(row=0, column=7, padx=(0, 10))

    # Obtention du nombre de colonnes afin de créer le tableau selon celle ci
    num_rows = len(results_infos)
    num_columns = len(results_infos[0])

    # Creation du tableau vide
    blank_results = [[None for _ in range(num_rows)] for _ in range(num_columns)]

  # Create a Label to display the entered pseudo
    pseudo_label = Label(results, text=f"Temps: {pseudo_value}", pady=3, font=("Arial", 11), bg="white")
    pseudo_label.grid(row=0, column=0, columnspan=7, pady=10)

    for line in range(len(results_infos[0])):
        for col in range(6):
            # Création label
            blank_results[line] = tkinter.Label(results, text=str(results_infos[col][line][0]), pady=3, width=14, bg="white", height=1, font=("Arial", 11))

            # Placement du label dans la fenêtre par un grid
            blank_results[line].grid(row=line + 1, column=col)

            # Placement du label dans la fenêtre par un grid
            blank_results[line].grid(row=line + 1, column=col)

        # choix de la largeur de la box selon son % de réussi
        if int(results_infos[-2][line][0]) == 0:
            width_pourcent = 1
        else:
            width_pourcent = round(20*(int(results_infos[-2][line][0])/int(results_infos[-1][line][0])))

        total_pourcentages += width_pourcent

        total_ok += results_infos[-2][line][0]
        total_trials += results_infos[-1][line][0]

        dates += results_infos[-4][line][0]

        # changer la couleur selon son %
        color = "orange"
        if width_pourcent <= 5:
            color = "red"
        if width_pourcent >= 15:
            color = "green"

        text_label = Label(results, width=width_pourcent, bg=color, height=1, font=("Arial", 11))
        text_label.grid(row=line+1, column=6, sticky=W)

    total_lines = len(results_infos[0])

    color = "orange"
    if total_lines !=0:
        if round(total_ok/total_lines) <= 5:
            color = "red"
        if round(total_ok/total_lines) >= 15:
            color = "green"
        lvtot_pourcent_total["width"] = round((total_ok / total_lines) / 4)
    else:
        color = "red"
        lvtot_pourcent_total["width"] = 1

    lvtot_pourcent_total["bg"] = color

    lvtot_lines["text"] = total_lines

    lvtot_num_ok["text"] = total_ok

    lvtot_num_total["text"] = total_trials

    lvtot_time["text"] = dates

    last_row_count = (len(results_infos[0]))


# window's content
title = Label(text="TRAINING AFFICHAGE", font=("Arial, 15")).place(x=1100/2-109,y=10)

# filters part
filters = Frame(bg="white", padx=10)
l_pseudo = Label(filters, text="Temps :", bg="white", padx=40, font=("Arial,11"))
e_pseudo = Entry(filters)

l_filter = Label(filters, text="Exercice :", bg="white", padx=40, font=("Arial,11"))
e_filter = Entry(filters)

l_start_date = Label(filters, text="Date début :", bg="white", padx=40, font=("Arial,11"))
e_start_date = Entry(filters)

l_end_date = Label(filters, text="Date fin :", bg="white", padx=40, font=("Arial,11"))
e_end_date = Entry(filters)

b_show_result = Button(filters, text="Voir résultats", font=("Arial,11"), command=show_results)

# results part
results = Frame(bg="white", padx=10)

l_column_id = Label(results, text="ID", bg="white", padx=40, font=("Arial", 11))
l_column_student = Label(results, text="Élève", bg="white", padx=40, font=("Arial", 11))
l_column_date_hour = Label(results, text="Date heure", bg="white", padx=40, font=("Arial",11))
l_column_time = Label(results, text="Temps", bg="white", padx=40, font=("Arial",11))
l_column_exo = Label(results, text="Exercice", bg="white", padx=40, font=("Arial",11))
l_column_num_ok = Label(results, text="nb OK", bg="white", padx=40, font=("Arial",11))
l_column_num_total = Label(results, text="nb Total", bg="white", padx=40, font=("Arial",11))
l_column_ok_ratio = Label(results, text="% réussi", bg="white", padx=40, font=("Arial",11))


# totals part (partie du bas avec les totaux)
l_title_total = Label(text="Total", bg="white", font=("Arial", 11), width=10)

totals = Frame(bg="white", padx=10, pady=4)

ltot_lines = Label(totals, text="NbLignes", bg="white", padx=40, font=("Arial", 11))
ltot_time = Label(totals, text="Temps total", bg="white", padx=40, font=("Arial", 11))
ltot_num_ok = Label(totals, text="Nb OK", bg="white", padx=40, font=("Arial", 11))
ltot_num_total = Label(totals, text="Nb Total", bg="white", padx=40, font=("Arial", 11))
ltot_pourcent_total = Label(totals, text="% Total", bg="white", padx=40, font=("Arial", 11))

lvtot_lines = Label(totals, text=num_lines, bg="white", padx=40, font=("Arial", 11))
lvtot_time = Label(totals, text=total_time, bg="white", padx=40, font=("Arial", 11))
lvtot_num_ok = Label(totals, text=num_ok, bg="white", padx=40, font=("Arial", 11))
lvtot_num_total = Label(totals, text=num_total, bg="white", padx=40, font=("Arial", 11))
lvtot_pourcent_total = Label(totals, bg="white", padx=40, font=("Arial", 11))

# placing elements
# filters part
filters.pack()
filters.place(y=50)

l_pseudo.grid(row=0, column=0, padx=(0, 10))
e_pseudo.grid(row=0, column=1)

l_filter.grid(row=0, column=2, padx=(0, 10))
e_filter.grid(row=0, column=3)

l_start_date.grid(row=0, column=4, padx=(0, 10))
e_start_date.grid(row=0, column=5)

l_end_date.grid(row=0, column=6, padx=(0, 10))
e_end_date.grid(row=0, column=7)

b_show_result.grid(row=1, column=0, pady=5)

# results part
results.pack()
results.place(y=150)

# columns part
l_column_id.grid(row=0, column=0, padx=(0, 10))
l_column_student.grid(row=0, column=1, padx=(0, 10))
l_column_date_hour.grid(row=0, column=2, padx=(0, 10))
l_column_time.grid(row=0, column=3, padx=(0, 10))
l_column_exo.grid(row=0, column=4, padx=(0, 10))
l_column_num_ok.grid(row=0, column=5, padx=(0, 10))
l_column_num_total.grid(row=0, column=6, padx=(0, 10))
l_column_ok_ratio.grid(row=0, column=7, padx=(0, 10))


# totals part
totals.pack(side="bottom")
l_title_total.pack(side="bottom")

ltot_lines.grid(row=0, column=0, padx=(0, 10))
ltot_time.grid(row=0, column=1, padx=(0, 10))
ltot_num_ok.grid(row=0, column=2, padx=(0, 10))
ltot_num_total.grid(row=0, column=3, padx=(0, 10))
ltot_pourcent_total.grid(row=0, column=4, padx=(0, 10))

lvtot_lines.grid(row=1, column=0, padx=(0, 10))
lvtot_time.grid(row=1, column=1, padx=(0, 10))
lvtot_num_ok.grid(row=1, column=2, padx=(0, 10))
lvtot_num_total.grid(row=1, column=3, padx=(0, 10))
lvtot_pourcent_total.grid(row=1, column=4, padx=(0, 10), sticky=W)

def delete_from_id():
    cursor = mydb.cursor()
    id = id_entry.get()
    sql = "DELETE FROM results WHERE id = %s"
    cursor.execute(sql, (id,))
    cursor.close()

    print("Data supprimé")
    show_results()

def update_from_id():
    global fenetre_ouverte
    
    if id_entry.get() == "":
        print("Veuillez entrer un ID")

    else:

        # Création d'une fenêtre avec la classe Tk :
        fenetre = Tk()
        # Affichage de la fenêtre créée :
        fenetre.title("Modifier un résultat")
        fenetre.geometry("300x200")
        fenetre.minsize(300, 300)
        fenetre.maxsize(300, 300)

        # Création du label et de l'entrée pour le pseudo.
        student_name_label = Label(fenetre, text="Eleve :")
        student_name_label.pack()
        student_name_entry = Entry(fenetre, width=30)
        student_name_entry.pack()

        date_hour_label = Label(fenetre, text="Date et heure (yyyy-mm-dd 00:00:00) :")
        date_hour_label.pack()
        date_hour_entry = Entry(fenetre, width=30)
        date_hour_entry.pack()


        time_label = Label(fenetre, text="Temps (00:00:00) :")
        time_label.pack()
        time_entry = Entry(fenetre, width=30)
        time_entry.pack()

        exo_label = Label(fenetre, text="Exercice :")
        exo_label.pack()
        exo_entry = Entry(fenetre, width=30)
        exo_entry.pack()

        nb_ok_label = Label(fenetre, text="nb OK :")
        nb_ok_label.pack()
        nb_ok_entry = Entry(fenetre, width=30)
        nb_ok_entry.pack()

        nb_total_label = Label(fenetre, text="nb OK :")
        nb_total_label.pack()
        nb_total_entry = Entry(fenetre, width=30)
        nb_total_entry.pack()


        def update_sql():
            # SQL
            print(date_hour_entry.get())
            cursor = mydb.cursor()
            sql = """
                    UPDATE results
                    SET results.pseudo = %s,
                    results.date_hour = %s,
                    results.during = %s,
                    results.exercise = %s,
                    results.nb_ok = %s,
                    results.nb_trials = %s,
                    WHERE results.id = %s;
                    """
        
            cursor.execute(sql, (student_name_entry.get(), date_hour_entry.get(), time_entry.get(), exo_entry.get(), nb_ok_entry.get(), nb_total_entry.get(), id_entry.get()[0]))
            cursor.close()
            show_results()
 

        validation_button = Button(fenetre, text="Valider", command=update_sql)
        validation_button.pack(side=BOTTOM, padx=5, pady=5)
        fenetre.mainloop()

def create_new_player():
    global fenetre_ouverte

    # Création d'une fenêtre avec la classe Tk :
    fenetre = Tk()
    # Affichage de la fenêtre créée :
    fenetre.title("Créer un résultat")
    fenetre.geometry("300x200")
    fenetre.minsize(300, 300)
    fenetre.maxsize(300, 300)

    # Création du label et de l'entrée pour le pseudo.
    student_name_label = Label(fenetre, text="Eleve :")
    student_name_label.pack()
    student_name_entry = Entry(fenetre, width=30)
    student_name_entry.pack()

    date_hour_label = Label(fenetre, text="Date et heure (yyyy-mm-dd 00:00:00) :")
    date_hour_label.pack()
    date_hour_entry = Entry(fenetre, width=30)
    date_hour_entry.pack()

    time_label = Label(fenetre, text="Temps (00:00:00) :")
    time_label.pack()
    time_entry = Entry(fenetre, width=30)
    time_entry.pack()

    exo_label = Label(fenetre, text="Exercice :")
    exo_label.pack()
    exo_entry = Entry(fenetre, width=30)
    exo_entry.pack()

    nb_ok_label = Label(fenetre, text="nb OK :")
    nb_ok_label.pack()
    nb_ok_entry = Entry(fenetre, width=30)
    nb_ok_entry.pack()
    
    nb_total_label = Label(fenetre, text="nb OK :")
    nb_total_label.pack()
    nb_total_entry = Entry(fenetre, width=30)
    nb_total_entry.pack()

    def update_sql():
        # SQL
        cursor = mydb.cursor()
        sql ="""
                INSERT INTO results(pseudo, date_hour, during, exercise, nb_ok, nb_trials)
                VALUES (%s, %s, %s, %s, %s, %s);
            """
    
        cursor.execute(sql, (student_name_entry.get(), date_hour_entry.get(), time_entry.get(), exo_entry.get(), nb_ok_entry.get(), nb_total_entry.get()))
        cursor.close()
        show_results()


    validation_button = Button(fenetre, text="Valider", command=update_sql)
    validation_button.pack(side=BOTTOM, padx=5, pady=5)
    fenetre.mainloop()

        
        


# Create, delete, update data
id_entry = Entry(window, width=5)
id_entry.pack(side="left", padx=10, pady=10)

delete_btn = Button(window, text="Delete", font=("Arial", 11), command=delete_from_id)
delete_btn.pack(side="left", padx=10, pady=10)

update_btn = Button(window, text="Update", font=("Arial", 11), command=update_from_id)
update_btn.pack(side="left", padx=10, pady=10)

create_btn = Button(window, text="Create", font=("Arial", 11), command=create_new_player)
create_btn.pack(side="left", padx=10, pady=10)

# start connection
mydb = mysql.connector.connect(**config)

# window's end
window.mainloop()