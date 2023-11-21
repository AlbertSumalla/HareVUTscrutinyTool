# -----HareVUTscrutinyTool-----
# Aquest codi preten realitzar l'escrutini d'una votació amb vot unic transferible amb quocient hare
# de forma automàtica i en temps real. Es pot executar tant ronda per ronda com tot de cop.
# El codi inclou un formulari d'inici, un selector de paperetes interactiu i la finestra de l'algoritme.

# S'ha utilitzat tkinter com a framework per treballar sobre finestres per ser moderadament senzill i prou potent.
# S'ha decidit realitzar tot el codi en un sol fitxer per el disseny estructural propi que té la llibreria tkinter

# Millores: Falta completar el codi necessari per a que es pugui resetejar una papereta en el selector un cop ha estat escollida.
# Faltarien codis d'error en el selector de paperetes, de moment no n'hi ha cap
# Bugs: En el primer formulari, el frame contingut dins la scrollbar no es mou al redimensionar la finestra. Al sortir algun codi d'error
# es desplaça el frame a la esquerra.

# Use pip install auto-py-to-exe si vols instalar la nova versio del programa al terminal
# Per obrir l'aplicatiu de conversio a exe, posa al terminal "python -m auto_py_to_exe" sense les cometes
