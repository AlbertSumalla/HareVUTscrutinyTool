from math import factorial
from itertools import permutations
from decimal import Decimal, getcontext
import tkinter as tk
from tkinter import ttk
import cv2
import math
from PIL import Image, ImageTk
from collections import defaultdict
import time
import random

# S'ha decidit realitzar tot el codi en un sol fitxer per el disseny estructural propi que té la llibreria tkinter

# Use pip install auto-py-to-exe si vols instalar la nova versio del programa al terminal
# Per obrir l'aplicatiu de conversio a exe, posa al terminal "python -m auto_py_to_exe" sense les cometes

# Aquest codi preten realitzar l'escrutini de una votació amb vot uinic transferible amb quocient hare
#de forma automàtica i en temps real. Es pot executar tant ronda per ronda com tot de cop.
#El codi inclou un formulari d'inici, un selector de paperetes interactiu i la finestra de l'algoritme.
#S'ha utilitzat tkinter com a framework per treballar sobre finestres per ser """"senzill""""" i prou potent.

# Millores: Falta completar el codi necessari per a que es pugui resetejar una papereta en el selector un cop ha estat escollida.
# Faltarien codis d'error en el selector de paperetes, de moment no n'hi ha cap
#Bugs: En el primer formulari, el frame contingut dins la scrollbar no es mou al redimensionar la finestra. Al sortir algun codi d'error
# es desplaça el frame a la esquerra.

def carregar_imatge(): #Carrega una imatge alla on se li demani
    imagen = cv2.imread("logoCdErelleno.png")
    imagen_mod = cv2.resize(imagen,(350,220))
    # Convertir la imagen a formato RGB
    imagen_rgb = cv2.cvtColor(imagen_mod, cv2.COLOR_BGR2RGB)
    # Crear una imagen de Pillow desde la matriz RGB
    imagen_pil = Image.fromarray(imagen_rgb)
    # Convertir la imagen de Pillow a un objeto de imagen Tkinter
    imagen_tk = ImageTk.PhotoImage(imagen_pil)
    # Mostrar la imagen en un widget de etiqueta
    image_plot.config(image=imagen_tk)
    image_plot.image = imagen_tk


def executar_programa(vent): # S'inicia el programa despres de la finestra principal
    global can,vac,pap, pap_ratll 

    def finalitzar_formulari():
        global lista_candidats,lista_genere,counter1,counter2,boto_avansar2,boton_continuar,frame
        counter1 =0
        counter2 = 0
        comprovar_gen = False
        for ele in lista_candidats_prov:
            if ele.get() != "":
                counter1 += 1
        for ele in genere_prov:
            if ele.get() != "":
                counter2 += 1
            if ele.get() != "m" and ele.get() != "f" and ele.get() != "NB": #No s'entrarà a l'if següent si el genere no es un d'aquests.
                comprovar_gen = True
        # En cas que hi hagin entrys de genere i de candidats == a el nombre de candidats indicat anteriorment, entrem
        if counter1 == can and counter2 == can and comprovar_gen == False:
            boto_avansar2.destroy()
            lista_candidats = []
            lista_genere = []
            for i in range(can): # Omplim les llistes provisionals de generes i candidats
                lista_candidats.append(lista_candidats_prov[i].get())
                lista_genere.append(genere_prov[i].get())
            # Amb aquest boto, iniciem el selector de paperetes
            boton_continuar = tk.Button(frame, text = "Escollir Paperetes" ,font = ("Helvetica",11), bg = "lightgoldenrod1", width= 15, height = 1, command= lambda: seleccionar_paperetes(wind1))
            boton_continuar.pack(anchor="n") 

    def comprovar_info():
        global count, can, vac, pap, comprov, error,boto_avansar2,cand_frame,frame
        can_input = num_can.get() # Fer el .get() es obtenir el valor en str de la entry
        vac_input = num_vac.get()
        pap_input = num_pap.get()
        done = 0
        # En cas que no hi hagin entrys en blanc, i #candidats >= #vacants, entrem a l'if.
        if can_input and vac_input and pap_input and int(can_input) >= int(vac_input): 
            can = int(can_input)
            vac = int(vac_input)
            pap = int(pap_input)
            done = 1
            espaiat = tk.Label(wind1, text = " ")
            espaiat.pack() 
            boto_avansar.destroy()
            def on_scroll(*args):
                canvas.yview(*args)
            # Crear el widget Canvas
            canvas = tk.Canvas(wind1)  # EDeclarem canvas com una variable global
            canvas.pack(side="left", fill="both")
            # Agregar scrollbar
            scrollbar = ttk.Scrollbar(wind1, orient="vertical", command=on_scroll)
            scrollbar.pack(side="right", fill="y")
            canvas.configure(yscrollcommand=scrollbar.set)
            # Colocar un widget Frame dentro del Canvas
            frame = tk.Frame(canvas)
            # Configure canvas
            canvas.create_window((canvas.winfo_width() / 2 + 15050, canvas.winfo_height() / 2), window=frame, anchor="center")
            canvas.configure(
                yscrollcommand=scrollbar.set,
                highlightthickness=0)
            frame.bind('<Configure>',lambda event: canvas.configure(scrollregion=canvas.bbox(tk.ALL)))
            canvas.bind('<Configure>', lambda event: frame.config(width=event.width,))
            opcions = ["m", "f", "NB"] # generes disponibles

            for i in range(can): # Segons els candidats que hi hagin, es mostraran x caselles per omplir
                cand_nom = tk.Label(frame, text="Candidat numero: " + str(i+1) + "           Gènere")
                cand_nom.pack(side="top")
                cand_frame = tk.Frame(frame)
                cand_frame.pack(anchor="center", padx=2, pady=4,side= "top", fill="both")
                lista_candidats_prov.append(tk.StringVar())  # Crear una StringVar para cada candidato
                genere_prov.append(tk.StringVar())
                cand_ent = tk.Entry(cand_frame, width="20", textvariable=lista_candidats_prov[i])
                cand_ent.pack(side= "left")
                space = tk.Label(cand_frame, text="   ", font=("Helvetica", 2, "bold"))
                space.pack(side ="left")
                desplegable = ttk.Combobox(cand_frame, values=opcions,width=2,textvariable=genere_prov[i],justify="center")
                desplegable.pack(side= "right")
                space = tk.Label(frame, text=" ", font=("Helvetica", 2, "bold"))
                space.pack()
            boto_avansar2 = tk.Button(frame, text="Acceptar", command=finalitzar_formulari) # Comprovem els valors anteriors i finalitzem
            boto_avansar2.pack()
            # Configurar el scroll para el Canvas
            frame.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))
        else:
            if count == 0:
                error = tk.Label(wind1, text="Error. Ingresa un valor a totes les caselles. \n Avís. Nombre de vacants ha de ser igual o inferior al de canidats", fg="red")
                error.pack()
                count += 1
        if count == 1 and done == 1:
            error.destroy()
            count = 2

    vent.destroy() #Destruim la finestra d'inici
    wind1 = tk.Tk()
    wind1.title(" Forulari Inicial. VUT amb Quocient Hare")
    wind1.geometry("550x650")
    # Inicialitzem valors de les Entry de tkinter
    num_can = tk.StringVar()
    num_vac = tk.StringVar()
    num_pap = tk.StringVar()
    
    space1 = tk.Label(wind1, text=" ", font = ("Helvetica",7))
    space1.pack()
    titol_form = tk.Label(wind1, text="Inrodueixi els paràmetres de la votació", font = ("Helvetica",13,"bold"),fg = "steelblue")
    titol_form.pack()
    # Iniciem el formulari primer
    space2 = tk.Label(wind1, text=" ", font = ("Helvetica",7,"bold"))
    space2.pack()
    et_vac = tk.Label(wind1, text="Introdueix el nombre de Vacants")
    et_vac.pack()
    entrada_vac = tk.Entry(wind1, width= "10", justify= "center", textvariable = num_vac)
    entrada_vac.pack()
    space2 = tk.Label(wind1, text=" ", font = ("Helvetica",2,"bold"))
    space2.pack()
    et_can = tk.Label(wind1, text="Introdueix el nombre de Candidats")
    et_can.pack()
    entrada_can = tk.Entry(wind1, width= "10", justify= "center", textvariable = num_can)
    entrada_can.pack()
    space2 = tk.Label(wind1, text=" ", font = ("Helvetica",2,"bold"))
    space2.pack()
    et_pap = tk.Label(wind1, text="Introdueix el nombre de Paperetes")
    et_pap.pack()
    entrada_pap = tk.Entry(wind1, width= "10", justify= "center", textvariable = num_pap)
    entrada_pap.pack()
    space2 = tk.Label(wind1, text=" ", font = ("Helvetica",2,"bold"))
    space2.pack()
    # Boto per avançar a la seguent secció del forumlari i comprovar que la info sigui correcta
    boto_avansar = tk.Button(wind1, text = "Acceptar", command= comprovar_info)
    boto_avansar.pack()

    def seleccionar_paperetes(vent):
        global matriu_paperetes, papereta_actual, ini,entry, num_entry, current_row, botons_verds, botons_vermells, num_pap_restants, genere,second_round,pap_ratll
        vent.destroy()        
        # creació del nou ordre en verd
        def seleccionar_candidat(ord):
            global current_row, mostrar, papereta_actual
            
            candidat_ordenat = tk.Button(wind2, text = candidats[ord], bg="lightgreen")
            candidat_ordenat.grid(row=current_row, column = 1)
            botons_verds.append(candidat_ordenat)  # afegim els botons verds a la llista
            papereta_actual.append(candidats[ord])
            
            current_row += 1
            botons_vermells[ord].grid_remove()
            mostrar = True
            mostrar_reset()

        # condicionem l'aparició del reset
        def mostrar_reset():
            global mostrar
            if mostrar:
                reset_button.grid(row = j+3, column = 1)
            else:
                reset_button.grid_remove()

        # configurem el reset
        def reset_botons():
            global current_row, mostrar, botons_vermells, papereta_actual
            current_row = 1
            mostrar = False
            reset_button.grid_remove()

            # borrem els vermells
            for boton in botons_vermells:
                boton.grid_remove()

            # borrem els verds i netejem la llista
            for boton in botons_verds:
                boton.grid_remove()
            botons_verds.clear()

            # tornem a crear els botons vermells
            botons_vermells = list()
            for k in range(len(candidats)):
                botons_candidats[k].grid(row=k + 1, column=0)
                botons_vermells.append(botons_candidats[k])
            
            # borrem la llista provisional
            papereta_actual.clear()
        '''
        def reset_papereta(reset_p): # Func inactiva
            global second_round,num_pap_restants,matriu_paperetes
            reset_position = int(reset_p.get())
            long_labels = len(matriu_paperetes)
            if reset_p.get() != "":
                for i,lista in enumerate(matriu_paperetes):
                    if i == reset_position:
                        num_pap_restants += lista[:-1]
                        matriu_paperetes.pop(i)
                        break
                for posi in range(long_labels):
                    if posi == reset_position:
                        # trobar manera de borrar una posició (llistat labels, selector posicio grid, etc)
                        break # Per que compili
        '''
        def acceptar_entrada():
            global num_pap_restants, num_entry, entry, papereta_actual, count, ini, matriu_paperetes, pap_ratll, can,second_round, pos_ini_labels
            num_entry = int(entry.get()) # Fem el get del nombre
            pos = ini + j
            pos_ini_labels = pos
            num_ordre_pap.delete(0, tk.END)
            if 0 < num_entry <= num_pap_restants and papereta_actual:  # Si s'ha seleccionat algun ordre i el num paperetes introduit >0
                num_pap_restants -= num_entry
                posicio = len(matriu_paperetes)+1
                registre1 = tk.Label(wind2, text = str(posicio) + ".  " + f"{num_entry} paperetes amb l'ordre següent:", font=("Arial", 9, "bold"))
                registre1.grid(row=pos, column=0)
                registre2 = tk.Label(wind2, text = papereta_actual)
                registre2.grid(row=pos, column=1)
                papereta_actual.append(num_entry)
                matriu_paperetes.append(list(papereta_actual))
                reset_botons()
                ini += 1

                # Actualizar num_pap_actualitz con el nuevo valor de num_pap_restants
                num_pap_actualitz.config(text =str(num_pap_restants))
                if num_pap_restants == 0:
                    for candis in list_pap_ratll:
                        pap_ratll = candis.get()
                    # espaiat i info barra lateral
                    if second_round == False: # Ignorar aquest if, sempre s'hi entra (es per el projecte de resetejar paperetes)
                        espaiat = tk.Label(wind2, text=" ")
                        espaiat.grid(row=6, column=3)
                        espaiat = tk.Label(wind2, text=" ")
                        espaiat.grid(row=7, column=3)
                        info_ratll = tk.Label(wind2, text =                          "Introdueixi les paperetes ratllades \n de cada candidat en TOTAL", font=("Arial", 11, "bold"), fg = "Seagreen3")
                        info_ratll.grid(row=8, column=3)
                        # Paperetes ratllades. Si no s'introdueix res, valor == 0 si no s'hi escriu res. 
                        curr_row = 10
                        iterer = 0
                        for candis in candidats:
                            list_pap_ratll.append(tk.StringVar())
                            info_rat = tk.Label(wind2, text= candis + ":", font=("Arial", 10, "bold") )
                            info_rat.grid(row=curr_row, column=3)
                            num_ratt = tk.Entry(wind2, width=5, textvariable = list_pap_ratll[iterer], justify = "center")
                            num_ratt.grid(row= curr_row, column=4)
                            curr_row += 1
                            iterer += 1
                        second_round = True
                    accept_button.grid_remove()
                    epsai = tk.Label(wind2, text= " ")
                    epsai.grid(row= pos+1, column=0)
                    #La fase ha finalitzat, executem el programa.
                    boto_final_fase = tk.Button(wind2, text="Confirmar Paperetes", bg="Seagreen2", command = lambda: ini_algoritme_hare(wind2,candidats,genere,can,vac,pap,list_pap_ratll))
                    boto_final_fase.grid(row=pos+2, column=0)
                    
                    ''' # Projecte de boto de reset de posicions  
                    #Creem el boto de reset per les posicions
                    res_pos = tk.StringVar()
                    res_entry = tk.Entry(wind2, textvariable = res_pos,width=5,justify="center")
                    res_entry.grid(row=pos+2, column=1,sticky="E")
                    res_button = tk.Button(wind2, text= "Reset Papereta: ",bg="lightgoldenrod", command = lambda reset_p=res_pos: reset_papereta(reset_p))
                    res_button.grid(row=pos+2, column=1,sticky="W")
                    '''
            else:
                print("error")

        # creem la finestra
        wind2 = tk.Tk()
        wind2.geometry("900x500")
        wind2.title("Escrutini Vot Unic Transferible amb Quocient Hare")

        # inicialitzem llistes i parámetres 
        botons_candidats = list()
        matriu_paperetes = []
        list_pap_ratll = list()
        pap_ratll = list()
        entry= None
        botons_vermells = list()
        botons_verds = list()
        papereta_actual = list()
        num_entry = 0
        entry= tk.StringVar()
        num_pap_restants = pap
        second_round = False
        ini = 8
        candidats = lista_candidats
        genere = lista_genere

        # Text de la finestra inicial
        titol = tk.Label(wind2, text="Selecciona un nou ordre de papereta", fg="red")
        titol.grid(row=0, column=0)
        subtitol = tk.Label(wind2, text="Aquí apareixerà el ordre escollit", fg="green")
        subtitol.grid(row=0, column=1)
        subsubtitol = tk.Label(wind2, text="                        Informació votació actual", fg = "steelblue")
        subsubtitol.grid(row=0, column=3)

        # Informació barra lateral
        info_vacants = tk.Label(wind2, text="Vacants:")
        info_vacants.grid(row=1, column=3)
        info_candidats = tk.Label(wind2, text="Candidats:")
        info_candidats.grid(row=2, column=3)
        info_paperetes = tk.Label(wind2, text="Paperetes:")
        info_paperetes.grid(row=3, column=3)

        info_pap_actualitz = tk.Label(wind2, text="Paperetes restants:",font=("Arial", 10),fg = "steelblue4")
        info_pap_actualitz.grid(row=5, column=3)

        num_vacants = tk.Label(wind2, text=vac, font=("Arial", 11, "bold"))
        num_vacants.grid(row=1, column=4)
        num_candidats = tk.Label(wind2, text=can, font=("Arial", 11, "bold"))
        num_candidats.grid(row=2, column=4)
        num_paperetes = tk.Label(wind2, text=pap, font=("Arial", 11, "bold"))
        num_paperetes.grid(row=3, column=4)

        num_pap_actualitz = tk.Label(wind2, text = str(num_pap_restants), font=("Arial", 13, "bold"), fg = "steelblue4")
        num_pap_actualitz.grid(row=5, column=4)
        
        list_pap_ratll = list()

        # creem el llistat de noms vermells
        for j in range(0,can):
            botons_candidats.append(tk.Button(wind2, text=candidats[j], width=8, height=1))
            botons_candidats[j].grid(row=j + 1, column=0)
            botons_vermells.append(botons_candidats[j])

        # creem espais, botons i entrades de parametres nercessaries
        espai1 = tk.Label(wind2, text=" ")
        espai1.grid(row=j + 2, column=0)
        espai2 = tk.Label(wind2, text=" ")
        espai2.grid(row=j + 3, column=0)
        espai3 = tk.Label(wind2, text=" ")
        espai3.grid(row=j + 4, column=0)
        text_pap = tk.Label(wind2, text="Introdueixi quantes paperetes d'aquest ordre hi han:")
        text_pap.grid(row=j + 5, column=0)
        num_ordre_pap = tk.Entry(wind2, width=5, textvariable = entry, justify = "center")
        num_ordre_pap.grid(row=j + 5, column=1)
        count = 1
        accept_button = tk.Button(wind2, text="Accepta la Entrada", command = acceptar_entrada)
        accept_button.grid(row=j + 6, column=0)
        espai3 = tk.Label(wind2, text=" ")
        espai3.grid(row=j + 7, column=0)

        # boto de reset amagat en primera instància
        reset_button = tk.Button(wind2, text="Reset", command=reset_botons, width = 5, height = 2, bg="lightgoldenrod")
        current_row = 1

        # es gestiona el botó vermell quan és apretat, fent apareixer els botons verds a la dreta i 
        # afegint el ordre desitjat a la llista de paperetes provisionals. 
        for k in range(0,can):
            botons_candidats[k].config(bg="indianred", command=lambda ord=k: seleccionar_candidat(ord))

    def ini_algoritme_hare(vent, candidats,genere,can,vac,pap,list_pap_ratll):
        global boto_comensar, matriu_paperetes, can_auxiliar
        can_auxiliar = can
        vent.destroy()
        logs_wind = tk.Tk()
        logs_wind.geometry("550x650")
        logs_wind.title("Finestra logs Escruitinat")
        getcontext().prec = 4 # Fixem els nombres (decimals i enters) que pot tenir un nombre decimal. (Ex: = 0.113 o 11.22 )

        def algoritme_rondes(): # Inici de l'algoritme que calcula cada ronda
            global round_count, label,end_escrutini,can,vac,pap,i,j,vac_rest, boto_comensar,matriu_paperetes,count_ag,round_count,vac_rest
            global esc_ronda,esc_directe,esc_ronda,esc_directe,vegades,vots_candidats,end_escrutini

            # Finalitzar escrutini
            def kill_winds():
                logs_wind.destroy()
                main_wind.destroy()
            
            #Treiem el boto de començar
            boto_comensar.destroy()
            
            main_wind = tk.Tk()
            main_wind.geometry("1100x650")
            main_wind.title("Algoritme Escrutinat VUT amb Quocient Hare")

            def escrutinat_de_cop(): # Executat al premer el boto. Executa totes les rondes de cop
                while end_escrutini == False:
                    escrutinat_ronda()

            def escrutinat_ronda(): #Algoritme de rondes 
                global end_escrutini,round_count,i,j,can,pap,vac,vac_rest,count_ag,esc_ronda,esc_directe,vegades,confirme,i,j, vots_candidats,label,can_auxiliar
                global doble, vegades_rep, comprovar_escrit, end_escrutini, counter
                global genere_menys_rep, candidat_repartir, can_electes, vots_iguals,gen_eliminats
                global repartiment_vots, can_eliminats, can_eliminats_prov, can_sup_hare
                global can_vots_prov, can_gen_prov, vots_candi_ini, vac_rest, gen_electes,no_masc,no_bin,no_fem
                global gen_eliminats, dic_transf_vots, dic_vot_canviar, dic_pos_canviar,preferencia_papereta,can_electes,can_eliminats,gen_electes
                label.grid_remove() 
                pos_preferencia = 0
                if vegades == 0: # Part de l'algoritme que nomes s'executa un cop
                    #Inicialitzem l'ordre de les preferenceis en les paperetes
                    confirme = False
                    trobat = False
                    pos_preferencia = 0
                    preferencia_papereta = []
                    for _ in matriu_paperetes: # Llista on s'actualitzaran les preferencies de la matriu
                        preferencia_papereta.append(0)
                    # En cas que hi hagin eliminats, actualitzem el valor de can
                    can = can_auxiliar
                    # Posicio grid main_wind 
                    i = 0
                    j = 0
                    #Inicialització de paràmetres
                    round_count = 1
                    doble = False
                    vegades_rep = 0
                    comprovar_escrit = False
                    end_escrutini = False
                    counter = 0
                    genere_menys_rep = "none"
                    candidat_repartir = " "
                    can_electes = []
                    vots_iguals = []
                    repartiment_vots = []
                    can_eliminats = []
                    can_eliminats_prov = []
                    can_sup_hare = []
                    can_vots_prov = []
                    can_gen_prov = []
                    vots_candi_ini = []
                    vac_rest = vac
                    gen_electes = []
                    gen_eliminats = []
                    dic_transf_vots = {}
                    dic_vot_canviar = {}
                    dic_pos_canviar = {}
                    vegades = 1
                    if can < vac: #En cas que s'hagin eliminat a variis candidats i per tal de que es pugui mostrar directament el guanyador
                        end_escrutini = True
                        can_electes = candidats
                    # Espaiat
                    espai = tk.Label(main_wind, text=" ", font=("Helvetica", 12), fg = "steelblue")
                    espai.grid(row=0, column=0)

                    # Imprimeix els candidats al principi de cada columna
                    for i, candid_actual in enumerate(candidats):
                        nom = tk.Label(main_wind, text=candid_actual, font=("Helvetica", 11,"bold"),fg = "steelblue")
                        nom.grid(row=j, column=i+1)
                    titols = tk.Label(main_wind, text="Elegits i Eliminats                 ", font=("Helvetica", 11,"bold"),fg = "gray31")
                    titols.grid(row=j, column=i+2)
                    titols = tk.Label(main_wind, text="        Motiu", font=("Helvetica", 11,"bold"),fg = "gray31")
                    titols.grid(row=j, column=i+2,sticky="E")
                    titols = tk.Label(main_wind, text="Vots a repartir", font=("Helvetica", 11,"bold"),fg = "gray31")
                    titols.grid(row=j, column=i+3,sticky="E")
                    j += 1

                    conteig_pre = [0, 0, 0]
                    # S'esborren els gèneres amb zero vots
                    for gen in genere:
                        if gen == "m":
                            conteig_pre[0] += 1
                        elif gen == "f":
                            conteig_pre[1] += 1
                        elif gen == "NB":
                            conteig_pre[2] += 1
                    no_masc = False
                    no_fem = False
                    no_bin = False
                    if conteig_pre[0] == 0:
                        no_masc = True
                    if conteig_pre[1] == 0:
                        no_fem = True
                    if conteig_pre[2] == 0:
                        no_bin = True
                    count_ag = 0
                count_ag += 1 
                rounds = tk.Label(main_wind, text="Ronda " + str(round_count) + ": ", font=("Helvetica", 11,"bold"))
                rounds.grid(row=j, column=0)
                # Creem llista dels vots en la preferencia corresponent de cada candidat si la ronda és la primera
                if round_count == 1:
                    vots_aux = 0
                    pos_act = 0
                    for cands in candidats:
                        for papereta in matriu_paperetes:
                            if cands == papereta[pos_act]:
                                vots_aux += papereta[-1]
                        vots_candi_ini.append(vots_aux)
                        vots_aux = 0    
                    vots_candidats = [Decimal(numero) for numero in vots_candi_ini]
                    for p, votos in enumerate(vots_candidats):
                        if votos == 0:
                            vots_candidats[p] += Decimal('0.01')
                # Trobem el valor mes petit
                menys_votat = Decimal('1000000000')
                for val in vots_candidats:
                    if val < menys_votat and val > 0:
                        menys_votat = val
                # Enganxa els vots de cada cadidat en la ronda corresponent (primera fase ronda)
                for i, vots in enumerate(vots_candidats):
                    if vots == Decimal('-1') or vots == Decimal('-2'): # Electe o eliminat
                        num_v = tk.Label(main_wind, text=" ", font=("Helvetica", 12))
                        num_v.grid(row=j, column=i+1)
                    else:
                        if vots == Decimal("0.01") and round_count == 1:
                            num_v = tk.Label(main_wind, text="0", font=("Helvetica", 12))
                            num_v.grid(row=j, column=i+1)
                        else:
                            num_v = tk.Label(main_wind, text=str(vots), font=("Helvetica", 12))
                            num_v.grid(row=j, column=i+1)
                        if can != vac_rest: # En cas que encara no sigui la ultima ronda, es configuren els colors del escrutini.
                            if vots == menys_votat: # Els menys votats passaran per aqui
                                num_v.config(fg="indianred")
                                can_eliminats_prov.append(candidats[i])
                                gen_eliminats.append(genere[i])
                            elif vots >= hare: # Els que superin el quocient hare passen per aqui
                                num_v.config(fg="sea green")
                        else:
                            num_v.config(fg = "sea green")

                # S'inicia el repartiment i redistribució de vots aplicant quociet hare.
                electe_per_hare = False
                #Trobem primer el candidat superiuor amb quocient hare. Si n'hi ha més d'un, s'escull
                for posicio, vots_prov in enumerate(vots_candidats):  # Usamos enumerate para obtener índices y valores
                    if vots_prov >= hare:
                        can_sup_hare.append(candidats[posicio])
                        can_vots_prov.append(vots_prov)
                        can_gen_prov.append(genere[posicio])

                if len(can_vots_prov) > 0:
                    vot_max = max(can_vots_prov)

                    # Crear una lista de candidatos con la cantidad máxima de votos
                    candidatos_max_votos = [cand for cand, vots in zip(can_sup_hare, can_vots_prov) if vots == vot_max]

                    if len(candidatos_max_votos) > 1:  # Decidir en caso de empate
                        elegit = random.choice(candidatos_max_votos)
                    else:
                        elegit = candidatos_max_votos[0]
                    #S'assignen posicions i vots al elegit
                    for pos, candis in enumerate(candidats):
                        if elegit == candis:
                            vots = vots_candidats[pos]
                            break
                # Gestió dels vots sobrants i de la finalitzacio de l'escrutini
                if vots >= hare and electe_per_hare == False and end_escrutini == False:
                    electe_per_hare = True # L'elecció d'un candidat per superar el quocient hare només és possible un cop per ronda
                    pos = vots_candidats.index(vots)
                    vac_rest -= 1
                    can_electes.append(candidats[pos])
                    gen_electes.append(genere[pos])
                    # Conteig genere dominant (none si cap)
                    conteig = [0, 0, 0]  # [conteig_m, conteig_f, conteig_NB]
                    for gen in gen_electes:
                        if gen == "m":
                            conteig[0] += 1
                        elif gen == "f":
                            conteig[1] += 1
                        elif gen == "NB":
                            conteig[2] += 1
                    if no_masc and no_fem or no_masc and no_bin or no_fem and no_bin: # Més de dos generes faltants
                        genere_menys_rep = "none"
                    # EN cas que nomes falti un genere
                    elif no_masc:
                        conteig.pop(0)
                        if conteig[0] < conteig[1]:
                            genere_menys_rep = "f"
                        elif conteig[1] < conteig[0]:
                            genere_menys_rep = "NB"
                        else:
                            genere_menys_rep = "none"
                    elif no_fem:
                        conteig.pop(1)
                        if conteig[0] < conteig[1]:
                            genere_menys_rep = "m"
                        elif conteig[1] < conteig[0]:
                            genere_menys_rep = "NB"
                        else:
                            genere_menys_rep = "none"
                    elif no_bin:
                        conteig.pop(2)
                        if conteig[0] < conteig[1]:
                            genere_menys_rep = "m"
                        elif conteig[1] < conteig[0]:
                            genere_menys_rep = "f"
                        else:
                            genere_menys_rep = "none"
                    # En cas que estiugin presents els tres generes
                    elif  not no_masc and not no_fem and not no_bin:
                        if conteig[0] < conteig[1] and conteig[0] < conteig[2]:
                            genere_menys_rep = "m"
                        elif conteig[1] < conteig[0] and conteig[1] < conteig[2]:
                            genere_menys_rep = "f"
                        elif conteig[2] < conteig[0] and conteig[2] < conteig[1]:
                            genere_menys_rep = "NB"
                        else:
                            genere_menys_rep = "none"
                    if vots > hare: # En cas que sobrin vots
                        vots_sobrants = vots - hare
                        for pos_modificar, fila in enumerate(matriu_paperetes):
                            if fila[preferencia_papereta[pos_preferencia]] == candidats[pos] and len(fila) > 1: # Busquem el candidat electe actual         
                                next_preferencia = preferencia_papereta[pos_preferencia] + 1
                                comp = False   
                                for ele in repartiment_vots:
                                    if ele == fila[next_preferencia]: # Comprovem que una persona no estigui dos cops en el repartiment
                                        dic_pos_canviar[pos_modificar] = ele
                                        dic_vot_canviar[ele] += 1
                                        comp = True
                                confirm = False
                                if comp == False: # En cas que no s'hagi ingresat de nou, si el candidat al que se li traspassen vots existeix, s'ingresa
                                    candidat_repartir = fila[next_preferencia]
                                    for ele in fila[:-1]:
                                        if confirm == False and fila.index(ele) > preferencia_papereta[pos_preferencia]:
                                            for candis in candidats:
                                                if ele == candis:
                                                    confirm = True
                                                    candidat_repartir == candis
                                    if confirm == True: # Al candidat actual se li ingresen els vots
                                        repartiment_vots.append(candidat_repartir)
                                        preferencia_papereta[pos_preferencia] += 1
                                        dic_pos_canviar[pos_modificar] = candidat_repartir
                                        dic_vot_canviar[candidat_repartir] = 1
                            pos_preferencia += 1
                        pos_preferencia = 0
                        #Comprovem si algun error ha ficat a algú que no tocava a repartiment_vots[]
                        for can_ele in repartiment_vots:
                            trobat = False
                            for candi in candidats:
                                if can_ele == candi:
                                    trobat = True
                            if trobat == False:
                                repartiment_vots.remove(can_ele)
                        #Repartim els vots segons les persones a les que els hi pertoca
                        if len(repartiment_vots) == 0:
                            vots_sumar_proporcionals = vots_sobrants
                        else:
                            vots_sumar_proporcionals = vots_sobrants/ Decimal(len(repartiment_vots))
                        #Comprovem que la llista de repartir no estigui buida per evitar errors i proceim a buscar el candidat a qui transferir vots
                        if len(repartiment_vots) != 0:
                            for ele in repartiment_vots:
                                pos_rep = candidats.index(ele)                     
                                vots_candidats[pos_rep] += vots_sumar_proporcionals # Es sumen els vots proporcionals a les preferencies seguents
                            
                            #S'asignen els vots sobrants proporcionalment a cada papereta)
                            for pos_canv, candi in dic_pos_canviar.items():
                                vegades_rep = 0
                                for posi, fil in enumerate(matriu_paperetes):
                                    if posi == pos_canv and len(dic_pos_canviar) > 1:
                                        for cand in dic_vot_canviar.keys():
                                            if cand == candi:
                                                vegades_rep = Decimal(dic_vot_canviar[cand])
                                                fil[-1] = vots_sumar_proporcionals / vegades_rep
                                                break
                    pos_preferencia = 0
                    #Mostrem el candidat electe i els vots a repartir
                    if can-1 != vac_rest:
                        elect = tk.Label(main_wind, text="Candidat elegit: "+ candidats[pos]+ ". A repartir: ", font=("Helvetica", 10), fg = "sea green")
                        elect.grid(row=j, column=i+2)
                        if len(repartiment_vots) > 0:
                            repart = tk.Label(main_wind, text= str(vots_sobrants) + " vots entre: ", font=("Helvetica", 10), fg = "DarkOrchid3")
                            repart.grid(row=j, column=i+3)
                            col_in_rep = i+3
                            for candi in repartiment_vots:
                                repart_can = tk.Label(main_wind, text=candi, font=("Helvetica", 10,"bold"), fg = "DarkOrchid3")
                                repart_can.grid(row=j, column=col_in_rep+1)
                                col_in_rep += 1
                    else:
                        elect = tk.Label(main_wind, text="Nombre de vacants igual al de candidats. Tots electes", font=("Helvetica", 10), fg = "sea green")
                        elect.grid(row=j, column=i+2)
                        comprovar_escrit = True
                    # Eliminem el nom del candidat ja electe, menntre el nom estigui per sobre de la preferencia actual enn la papereta (evitant aixi desplaçaments no desitjats)
                    for fila in matriu_paperetes:
                        for ele in fila:
                            if ele == candidats[pos] and fila.index(ele) > round_count-1:
                                fila.remove(ele)
                    insertar = pos
                    vots_candidats.pop(pos)
                    vots_candidats.insert(pos, Decimal('-1'))
                    candidats.pop(pos)
                    candidats.insert(insertar, " ")
                    genere.pop(pos)
                    genere.insert(insertar, " ")
                    can -= 1
                    # Si queda per cobrir una quantitat de places igual o superior a la quantitat de persones candidates restants, les persones candidates restants són declarades electes.
                if vac_rest == can:
                    for cand in candidats:
                        if cand != " ":
                            can_electes.append(cand)
                            vac_rest -= 1
                    end_escrutini = True
                    candidats.clear()
                    can_eliminats_prov.clear()
                # S'aclareix que, en aquesta ronda, ningú ha estat escollit per superar el quocient hare
                if electe_per_hare == False and end_escrutini != True:
                    elect = tk.Label(main_wind, text="Ningú ha arribat al quocient hare        ", font=("Helvetica", 10), fg = "sea green")
                    elect.grid(row=j, column=i+2)
                # S'escolleixen tots els candidats de cop
                if end_escrutini == True and comprovar_escrit != True:
                    elect = tk.Label(main_wind, text="Nombre de vacants igual al de candidats. Tots electes", font=("Helvetica", 10), fg = "sea green")
                    elect.grid(row=j, column=i+2)

                # Es descarta la persona candidata que té el nombre més baix de vots
                # Els empats es resolen per sorteig en cas de no poder-se resoldre segons el genere mes representat o de no existir-n'hi
                if end_escrutini == False:
                    sorteig = False
                    paritat = False
                    decisiu = False
                    comp_gen = False
                    if len(gen_eliminats) > 0:
                        gen_anterior = gen_eliminats[0]
                    if len(can_eliminats_prov) > 1:
                        # Si existeix un genere menys representat, s'entra a l'if
                        if genere_menys_rep != "none":
                            comp_gen = False
                            for gen in gen_eliminats[1:]:
                                if gen == gen_anterior:
                                    comp_gen = True
                            for gen in gen_eliminats:
                                pos_elim = gen_eliminats.index(gen)
                                if gen == genere_menys_rep and paritat == False and comp_gen == False:
                                    gen_eliminats.pop(pos_elim)
                                    can_eliminats_prov.pop(pos_elim)
                                    paritat = True
                        if len(can_eliminats_prov) > 1:
                            sorteig = True
                    # Si no hi ha genere menys representat o es fa sorteig, entra a l'if
                    if len(can_eliminats_prov) != 0:
                        if genere_menys_rep == "none" or sorteig == True: # El sorteig es realitza amb un algoritme propi de random choose
                            deci = ["sum", "rest"]
                            current_time = int(time.time())
                            seed = current_time % 1000 # Creem la seed a partir de l'hora actual
                            a = 1664525
                            b = 1013904223
                            max_num = len(can_eliminats_prov)
                            def generate_random(seed):
                                get_deci = random.choice(deci) # Afegim la participacio d'una llibreria per sumar o restar valors, creant numeros aleatoris encara mes bons
                                if get_deci == "sum":
                                    seed += random.randint(0, 534)
                                elif get_deci == "rest" and seed > 327:
                                    seed -= random.randint(0, 327) 
                                return (a * seed &1000 + b) % max_num

                            itera = (1+ current_time * 15) % 20 # Iterem (0,20] cops aleatoritzant encara mes el valor
                            for _ in range(itera):
                                posi_aleatoria = generate_random(seed)
                            
                            candidat_eliminar = can_eliminats_prov[posi_aleatoria]
                            paritat = False
                        elif end_escrutini != True: # Seleccionem candidat
                            pos_elim = candidats.index(can_eliminats_prov[0])
                            candidat_eliminar = can_eliminats_prov[0]
                    if sorteig == False and paritat == False: # En aquest cas, el motiu de ser eliminat serà "Menys votat"
                        decisiu = True
                    
                    # Si s'h eliminat el/s candidats amb genere menys representat, o si només s'hi havia un, entra a l'if
                    if len(can_eliminats_prov) == 1 or sorteig == True:
                        pos_elim = candidats.index(candidat_eliminar)
                        # Eliminem el nom del candidat eliminat, menntre el nom estigui per sobre de la preferencia actual enn la papereta (evitant aixi desplaçaments no desitjats)
                        can_eliminats.append(candidat_eliminar)
                        # Traspassar els vots de l'eliminat al següent:
                        vots_transf = 0
                        vots_acumulats = 0
                        candidat_sumar = " "
                        pos_preferencia = 0
                        trobat = False
                        verif = 0
                        # Traspassem els vots de l'eliminat al següent:  
                        if len(can_eliminats_prov) != 0: # # Inici del traspas
                            for fila in matriu_paperetes:
                                if len(fila) > preferencia_papereta[pos_preferencia] and candidat_eliminar == fila[preferencia_papereta[pos_preferencia]] and len(fila) > 1:
                                    vots_transf = Decimal(fila[-1]) # Obtenir els vots de la fila actual
                                    verif = 0
                                    candidat_sumar = fila[preferencia_papereta[pos_preferencia] + 1]
                                    for ele in fila[preferencia_papereta[pos_preferencia] + 1:]:
                                        if verif == 0 and len(fila) > preferencia_papereta[pos_preferencia] + 1:
                                            for candi in candidats:
                                                if candidat_sumar == candi:
                                                    candidat_sumar = ele
                                                    preferencia_papereta[pos_preferencia] += 1
                                                    verif = 1
                                                if verif == 1:
                                                    break
                                    if verif == 1:
                                        trobat = False
                                        for clave in dic_transf_vots.keys():
                                            if clave == candidat_sumar:
                                                dic_transf_vots[clave] += vots_transf
                                                trobat = True
                                        if trobat == False:
                                            dic_transf_vots[candidat_sumar] = vots_transf
                                pos_preferencia += 1
                            for candi_transf in dic_transf_vots.keys():
                                for posicio_transf, candi in enumerate(candidats):
                                    if candi_transf == candi:
                                        vots_candidats[posicio_transf] += dic_transf_vots[candi_transf]
                        # Eliminem del tot el candidat
                        for fila in matriu_paperetes:
                            for ele in fila:
                                if ele == candidats[pos_elim] and fila.index(ele) > round_count-1:
                                    fila.remove(ele)
                        pos_suma = pos_elim
                        vots_candidats.pop(pos_elim)
                        vots_candidats.insert(pos_elim, Decimal('-2'))
                        insertar = pos_elim
                        candidats.pop(pos_elim)
                        candidats.insert(insertar, " ")
                        genere.pop(pos_elim)
                        genere.insert(insertar, " ")
                        can -= 1    
                # Enganxa els vots de cada cadidat en la ronda corresponent (segona fase ronda)
                if end_escrutini == False:
                    for i, vots in enumerate(vots_candidats):
                        pos = vots_candidats.index(vots)
                        if vots == Decimal('-1') or vots == Decimal('-2'): # Electe (-1) o eliminat (-2)
                            num_v = tk.Label(main_wind, text=" ", font=("Helvetica", 12))
                            num_v.grid(row=j+1, column=i+1)
                        elif vots == Decimal("0.01"):
                            num_v = tk.Label(main_wind, text="0", font=("Helvetica", 12))
                            num_v.grid(row=j, column=i+1)
                        else:
                            num_v = tk.Label(main_wind, text=str(vots), font=("Helvetica", 12))
                            num_v.grid(row=j+1, column=i+1)
                        doble = False
                        for candi in repartiment_vots: # Si se li han cedit vots es posa de color lila
                            if candi != candidat_eliminar and candidats[pos] == candi:
                                num_v.config(fg = "DarkOrchid3")
                                doble = True
                        for candis in dic_transf_vots.keys():
                            if candidats[pos] == candis:
                                num_v.config(fg = "slate blue")
                                if doble == True:
                                    num_v.config(font=("Helvetica", 12,"bold"))
                    #Informació eliminat
                    if sorteig == True:
                        causa = tk.Label(main_wind, text="Sorteig", font=("Helvetica", 10,"bold"),fg = "indianred")
                        causa.grid(row=j+1, column=i+2, sticky="E")
                    elif paritat == True:
                        causa = tk.Label(main_wind, text="Paritat", font=("Helvetica", 10,"bold"),fg = "indianred")
                        causa.grid(row=j+1, column=i+2, sticky="E")
                    elif decisiu == True:
                        causa = tk.Label(main_wind, text="Menys vots", font=("Helvetica", 10,"bold"),fg = "indianred")
                        causa.grid(row=j+1, column=i+2, sticky="E")
                    elim3 = tk.Label(main_wind, text="Eliminat a " + candidat_eliminar + " per: ", font=("Helvetica", 10),fg = "indianred")
                    elim3.grid(row=j+1, column=i+2)
                    count = 3
                    # Vots transferits de l'eliminat
                    for clave in dic_transf_vots.keys():
                        transfe = tk.Label(main_wind, text= str(dic_transf_vots[clave])+" vots a: " + clave, font=("Helvetica", 10),fg = "slate blue")
                        transfe.grid(row=j+1, column=i+count)
                        count+= 1
                else:
                    espaiats = tk.Label(main_wind, text= " ", font=("Helvetica", 3))
                    espaiats.grid(row=j+2, column=0, sticky="S")
                    end_message = tk.Label(main_wind, text="Els candidats electes en l'escrutini són: ", font=("Helvetica", 11,"bold"),fg = "steelblue")
                    end_message.grid(row=j+3, column=i+2, sticky="W")
                    goteo = 4
                    for candi in can_electes:
                        for posi in range(0,i+1):
                            espaiats = tk.Label(main_wind, text= " ", font=("Helvetica", 1, "bold"))
                            espaiats.grid(row=j+goteo, column=posi, sticky="S")
                        end_electes = tk.Label(main_wind, text= candi, font=("Helvetica", 12, "bold"),fg = "steelblue", bg= "LightBlue2")
                        end_electes.grid(row=j+goteo, column=i+2, sticky="S")
                        goteo += 1
                    

                espaiats = tk.Label(main_wind, text= " ", font=("Helvetica", 3))
                espaiats.grid(row=j+2, column=0, sticky="S")
                j += 4
                espaiat = tk.Label(main_wind, text=" ", font=("Helvetica", 5,"bold"))
                espaiat.grid(row=j, column=0)
                candidat_eliminar = " "
                pos_preferencia = 0
                can_eliminats_prov.clear()
                gen_eliminats.clear()
                repartiment_vots.clear()
                dic_transf_vots.clear()
                dic_vot_canviar.clear()
                dic_pos_canviar.clear()
                can_sup_hare.clear()
                can_vots_prov.clear()
                can_gen_prov.clear()
                round_count += 1
                if end_escrutini == True:
                    esc_ronda.grid_remove()
                    esc_directe.grid_remove()
                    title_def.grid_remove()
                    end = tk.Button(logs_wind, text="Finalitzar Programa", font = ("Helvetica", 11, "bold"), bg = "khaki2",command=kill_winds)
                    end.grid(row = fil_log, column= 2,sticky= "W"+"E")

            # Algoritme per executar les rondes; es proporcionen dos maneres de procedir, ronda a ronda, o de cop
            vegades = 0
            end_escrutini = False
            vots_candidats = list()
            title_def = tk.Label(logs_wind, text="Iniciar Escrutini", font = ("Helvetica", 11, "bold"), fg = "steelblue")
            title_def.grid(row = fil_log, column= 2)
            esc_ronda = tk.Button(logs_wind, text="Ronda a Ronda", font = ("Helvetica", 11, "bold"), bg = "DarkSeaGreen2",command = escrutinat_ronda)
            esc_ronda.grid(row = fil_log+1, column= 2,sticky= "W"+"E")
            label = tk.Label(logs_wind,text = " ",font = ("Helvetica", 11, "bold"))
            label.grid(row=fil_log+1,column=3,sticky="N")
            esc_directe = tk.Button(logs_wind, text="De cop", font = ("Helvetica", 11, "bold"), bg = "tan2",command=escrutinat_de_cop)
            esc_directe.grid(row = fil_log+1, column= 4,sticky= "W")
            label = tk.Label(main_wind,text = "Prem un dels botons per començar l'escrutini :)",font = ("Helvetica", 27, "bold"),fg = "indianred")
            label.grid(row=0,column=0,sticky="N")
        
        for secs in range (0, 20): # Espais a la primera columna de la finestra logs
            espai = tk.Label(logs_wind, text=" ")
            espai.grid(row = secs, column= 0)
        fil_log = 0
        comprov = 0
        # Informació Escriutini actual
        title = tk.Label(logs_wind, text="Registre Escrutinat", font = ("Helvetica", 11, "bold"), fg = "steelblue")
        title.grid(row = fil_log, column= 1)
        fil_log += 1
        info_vacants = tk.Label(logs_wind, text="Vacants:")
        info_vacants.grid(row = fil_log, column= 1)
        num_vacants = tk.Label(logs_wind, text=vac, font=("Helvetica", 11, "bold"))
        num_vacants.grid(row = fil_log, column= 2)
        fil_log +=1
        info_candidats = tk.Label(logs_wind, text="Candidats:")
        info_candidats.grid(row = fil_log, column= 1)
        num_candidats = tk.Label(logs_wind, text=can, font=("Helvetica", 11, "bold"))
        num_candidats.grid(row = fil_log, column= 2)
        fil_log +=1
        info_paperetes = tk.Label(logs_wind, text="Paperetes:")
        info_paperetes.grid(row = fil_log, column= 1)
        num_paperetes = tk.Label(logs_wind, text=pap, font=("Helvetica", 11, "bold"))
        num_paperetes.grid(row = fil_log, column= 2)
        fil_log +=1

        # Fase Inicial

        #Calculem el quocient hare 
        hare = Decimal(pap) / Decimal(vac)

        quocient_hare_inf = tk.Label(logs_wind, text="Quocient Hare")
        quocient_hare_inf.grid(row = fil_log, column= 1)
        quocient_hare = tk.Label(logs_wind, text=hare, font=("Helvetica", 11, "bold"))
        quocient_hare.grid(row = fil_log, column= 2)
        fil_log += 1

        # Espaiat 
        title3 = tk.Label(logs_wind, text="Candidats Eliminats", font = ("Helvetica", 11, "bold"), fg = "steelblue")
        title3.grid(row = fil_log, column= 1)
        fil_log += 1

        # Es descarten les persones que no han estat votades amb cap preferència per ningú.
        no_estan = list()
        for nom in candidats:
            trobat = False
            for fila in matriu_paperetes:
                if nom in fila:
                    trobat = True
                    break
            if not trobat:
                no_estan.append(nom)

        for nom in no_estan:
            pos = candidats.index(nom)
            candidats.remove(nom)
            pap_ratll.pop(pos)
            genere.pop(pos)
            can_auxiliar -= 1
            elim = tk.Label(logs_wind, text="S'ha eliminat el candidat " + nom + " per tenir 0 vots", font = ("Helvetica",9),fg = "tomato")
            elim.grid(row = fil_log, column= 1)
            comprov = 1
            fil_log += 1

        # Quan l'usuari no introdueix paperetes ratllades a un candidat, automaticment es posa un 0
        for val in list_pap_ratll:
            pap_prv = val.get()
            if pap_prv == "":
                pap_ratll.append(0)
            else:
                pap_ratll.append(int(pap_prv))  
        # Es descarten les persones amb més paperetes ratllades que nombre de vots
        for nom_can in candidats:
            pos = candidats.index(nom_can)
            num_rep = 0
            for lista in matriu_paperetes:
                cols = 0
                for nom in lista[:-1]:
                    if nom_can == lista[cols]:
                        num_rep += lista[-1]
                    cols += 1
            if num_rep < pap_ratll[pos]: # SI es troba que el nombre de paperetes ratllades > nombre de vots
                num_ratll = pap_ratll[pos]
                candidats.remove(nom_can)
                pap_ratll.pop(pos)
                genere.pop(pos)
                for fila in matriu_paperetes:
                    for ele in fila:
                        if ele == nom_can:
                            fila.remove(ele)
                can_auxiliar -= 1
                elim2 = tk.Label(logs_wind, text="S'ha eliminat el candidat " + nom_can + " \n per mes vots ratllats que a favor. \n(" + str(num_ratll) + " ratllats vs " + str(num_rep) + " vots)", font = ("Helvetica",9),fg = "tomato")
                elim2.grid(row = fil_log, column= 1)
                comprov = 1
                fil_log += 1
        if comprov == 0: # En cas que no hi hagi eliminats de cap tipus
            elim2 = tk.Label(logs_wind, text="Cap Modificació", font = ("Helvetica",9),fg = "tomato")
            elim2.grid(row = fil_log, column= 1)
            fil_log += 1

        # paperetes despres dels canvis
        title2 = tk.Label(logs_wind, text="Paperetes", font = ("Helvetica", 11, "bold"), fg = "steelblue")
        title2.grid(row = fil_log, column= 1)
        fil_log += 1

        for lista in matriu_paperetes: # Fem el plot de les paperetes en la finestra logs
            reg =  tk.Label(logs_wind, text = str(lista[-1]) + " paperetes amb l'ordre següent:")
            reg.grid(row=fil_log, column=1)
            regL = tk.Label(logs_wind, text = lista[:-1], font=("Helvetica", 9, "bold"))
            regL.grid(row=fil_log, column=2, sticky = "W")
            fil_log +=1

        espaiat = tk.Label(logs_wind, text = " ", font=("Helvetica", 9, "bold"))
        espaiat.grid(row=fil_log, column=2, sticky = "W")
        fil_log +=1
        #Boto per començar l'escrutinat
        boto_comensar = tk.Button(logs_wind, text="Començar escrutinat", font = ("Helvetica", 11, "bold"), bg = "steelblue",fg = "white",command=algoritme_rondes)
        boto_comensar.grid(row = fil_log, column= 2,sticky= "W"+"E")


root = tk.Tk() #Inicialitzem la finestra mare de tots. 
root.title("Inici VUT amb Quocient Hare")
root.geometry("700x700")
count = 0
comprov = 0
candidats = list()
lista_candidats_prov = list()
genere_prov = list()
# Iniciem parametres
# Info set Top
space1 = tk.Label(root, text=" ", font = ("Helvetica",15,"bold"))
space1.pack()
titol_intro = tk.Label(root, text="EINA PER A LA REALITZACIÓ DE L'ESCRUTINI \n D'UNA VOTACIÓ AMB VOT ÚNIC  \nTRANSFERIBLE AMB QUOCIENT HARE", font = ("Helvetica",20,"bold"),fg = "steelblue")
titol_intro.pack()
space2 = tk.Label(root, text=" ", font = ("Helvetica",15))
space2.pack()
space3 = tk.Label(root, text=" ", font = ("Helvetica",15))
space3.pack()

# Carregar imatge a la finestra
image_plot = tk.Label(root)
image_plot.pack()
carregar_imatge()

descript = tk.Label(root, text="Amb aquesta eina s'automatitza el recompte de vots \n i permet la seva visualització en temps real", font = ("Helvetica",15), fg = "grey" )
descript.pack()

# Info set Bottom
space4 = tk.Label(root, text=" ", font = ("Helvetica",15))
space4.pack(side = "bottom") 
caption1 = tk.Label(root, text="by Albert Sumalla. v 1.1", font = ("Helvetica",11), fg = "lightgrey")
caption1.pack(side = "bottom")
caption2 = tk.Label(root, text="CdE-UPC", font = ("Helvetica",11,"bold"), fg = "grey")
caption2.pack(side = "bottom")  
space5 = tk.Label(root, text=" ", font = ("Helvetica",15))
space5.pack(side = "bottom")
space6 = tk.Label(root, text=" ", font = ("Helvetica",15))
space6.pack(side = "bottom")
boton_inicio = tk.Button(root, text = "Començar" ,font = ("Helvetica",15, "bold"), bg = "lightgoldenrod1", width= 12, height = 2, command= lambda: executar_programa(root))
boton_inicio.pack(side = "bottom")
space3 = tk.Label(root, text=" ", font = ("Helvetica",15))
space3.pack()

root.mainloop() # Loop que mante les finestres en funcionament (al eliminar "root" s'hereden les funciona a la següent/s windows)