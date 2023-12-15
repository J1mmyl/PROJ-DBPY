"""
Author      : Jimmy LAM
Date        : 24.11.2023
Version     : v1
"""

import tkinter as tk
import subprocess
import resultstable

# identifiants mysql
config = {
  'user': 'root',
  'host': '127.0.0.1',
  'database': 'mygame',
  'raise_on_warnings': True,
  'autocommit': True,
  'buffered': True
}


# Constantes de couleur
COULEUR_BG = (139, 201, 194)
COULEUR_HEX = '#%02x%02x%02x' % COULEUR_BG

# Tableau des exercices
exercices = ["geo01", "info02", "info05"]
etiquettes_images = [None, None, None]  # Tableau de labels (avec images)
images = [None, None, None]  # Tableau d'images
titres = [None, None, None]  # Tableau de titres (ex: GEO01)

def creer_etiquette_et_image(exercice, ligne, colonne):
    """Crée un label et une image pour chaque exercice."""
    etiquette = tk.Label(window, text=exercice, font=("Arial", 15))
    etiquette.grid(row=ligne, column=colonne, padx=40, pady=10)

    chemin_image = f"img/{exercice}.gif"
    image = tk.PhotoImage(file=chemin_image)
    etiquette_image = tk.Label(window, image=image)
    etiquette_image.grid(row=ligne + 1, column=colonne, padx=40, pady=10)
    etiquette_image.bind("<Button-1>", lambda event, ex=exercice: exercice_selectionne(event=None, exercice=ex))

    return etiquette, etiquette_image, image

def afficher_resultats():
    subprocess.run(["python", "resultstable.py"])

def quitter(event):
    window.destroy()

# Fenêtre principale
window = tk.Tk()
window.title("Entraînement cérébral")
window.geometry("1100x900")
window.configure(bg=COULEUR_HEX)
window.grid_columnconfigure((0, 1, 2), minsize=300, weight=1)

# Création du titre
lbl_titre = tk.Label(window, text="MENU D'ENTRAÎNEMENT", font=("Arial", 15))
lbl_titre.grid(row=0, column=1, ipady=5, padx=40, pady=40)

# Création des labels et positionnement à l'aide d'une boucle
for ex_index, ex in enumerate(exercices):
    ligne_position = 1 + 2 * (ex_index // 3)
    colonne_position = ex_index % 3

    titres[ex_index], etiquettes_images[ex_index], images[ex_index] = creer_etiquette_et_image(ex, ligne_position, colonne_position)

# Boutons, affichage des résultats et quitter
btn_afficher = tk.Button(window, text="Afficher les résultats", font=("Arial", 15), command=afficher_resultats)
btn_afficher.grid(row=1 + 2 * len(exercices) // 3, column=1)

btn_quitter = tk.Button(window, text="Quitter", font=("Arial", 15))
btn_quitter.grid(row=2 + 2 * len(exercices) // 3, column=1)
btn_quitter.bind("<Button-1>", quitter)

# Boucle principale
window.mainloop()
