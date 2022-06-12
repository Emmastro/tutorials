# Snake
from tkinter import*
from random import*
from tkinter.messagebox import showerror
from time import time

FICHIER = open(file="data/board.txt")


class Fichier(Frame):
    def __init__(self, terrain, lst_terrain, mur, fterrain):
        self.mur = mur
        self.fterrain = fterrain
        self.terrain = terrain  # contient les noms des terrains
        self.lst_terrain = lst_terrain
        Frame.__init__(self, borderwidth=2)
        self.flmenu = Menubutton(self, text='Fichier', font='Andalus 14')
        self.men = Menu(self.flmenu)
        a = [0, 1, 2]
        a = self.men.add_command(
            label='Terrain', font='Andalus 14', command=self.auChoix)
        self.flmenu.configure(menu=self.men)
        self.flmenu.pack(side=LEFT)
        self.pack(side=TOP)
       # print(dir(self.men))

    def save(self):
        1

    def auChoix(self):
        """Ouvre une boite de dialoque permetant au joueur de choisir un terrain"""
        self.fen1 = Toplevel()
        self.fen1.title("Terrain")
        frame1 = Frame(self.fen1)
        Label(frame1, text="Liste des terrains",
              font="Andalus 14").pack(side=TOP)
        self.terrains = Listbox(frame1, font="Andalus 14")
        # Le canvas qui affiche le terrain selectionné
        self.can1 = Canvas(self.fen1, width=378, height=378)
        self.can1.pack(side=RIGHT)
        self.terrains.bind('<Button-1>', self.montrer)
        for t in self.terrain:
            self.terrains.insert(END, t)
        self.terrains.pack(side=LEFT)
        Button(self.fen1, text="Charger", fon="Andalus 14",
               command=self.charger).pack(side=BOTTOM)
        frame1.pack(side=LEFT)
        self.fen1.mainloop()

    def montrer(self, event):
        """Affiche le terrain choisi dans la liste au Canvas"""
        c = self.terrains.curselection()
        if c != ():
            c = c[0]
            self.can1.delete(ALL)
            x, y = 0, 0
            for col in self.lst_terrain[c]:
                x = 0
                for lign in col:
                    if lign == '1':
                        self.can1.create_image(x*14, y*14, image=self.mur)
                    x += 1
                y += 1
        self.c = c

    def charger(self):
        self.fterrain(self.c)
        self.fen1.destroy()


class Serpent:
    def __init__(self):

        self.fen = Tk()
        self.debut = time()
        self.n = 1  # si c'est un jeu qui change de terrain terrain, on commence par le 2e terrain
        self.fen.title("SNAKE Version 1.2")
        self.LEFT = PhotoImage(file="images/v1/Left.gif")  # initialisation des photos
        self.RIGHT = PhotoImage(file="images/v1/Right.gif")
        self.UP = PhotoImage(file="images/v1/Up.gif")
        self.DOWN = PhotoImage(file="images/v1/Down.gif")
        self.CORPS = PhotoImage(file="images/v1/Body.gif")
        self.POMME = PhotoImage(file="images/v1/Goody.gif")
        self.LIFE = PhotoImage(file='images/v1/newLife.gif')
        self.POWER = PhotoImage(file="images/v1/PowerUp.gif")
        self.GOODY = PhotoImage(file='images/v1/Goody.gif')
        self.BRIC = PhotoImage(file='images/v1/bric1.GIF')
        self.nbric1, self.nbric2 = 9, 0  # contiendrons les id des brics
        FICHIER.seek(0)
        a = FICHIER.readline()
        self.terrain = [a]  # contient les noms des terrains
        # contient les terrains (sous forme brut ==> '000101001')
        self.lst_terrain = [[]]
        i = 0  # compteur
        while a[0] == 'T':
            for el in range(27):
                self.lst_terrain[i].append(FICHIER.readline())
            a = FICHIER.readline()
            self.terrain.append(a)
            i += 1
            self.lst_terrain.append([])
        FICHIER.seek(0)
        frame = Frame(self.fen)
        self.can = Canvas(frame, width=364, height=364, bg='pink')
        self.resultat()  # place les Buttons et Labels
        self.initialiser()  # place le serpent
        self.terrain1()  # place le terrain
        men = Fichier(self.terrain, self.lst_terrain, self.BRIC, self.terrain1)
        self.can.pack(side=TOP)

        # Barre de progression
        Label(frame, text="Durré : ", font='Andalus 14').pack(side=LEFT)
        self.barre = Canvas(frame, width=1, height=15, bg='green')
        self.barre.pack(side=LEFT)
        a = 8
        frame.pack(side=BOTTOM)
        self.can.focus_set()
        self.x, self.y = 14, 0
        self.can.bind('<Up>', self.haut)
        self.can.bind('<Down>', self.bas)
        self.can.bind('<Left>', self.gauche)
        self.can.bind('<Right>', self.droite)
        self.can.bind('<space>', self.pause)
        self.fen.mainloop()

    def initialiser(self):
        """initialise les anneaux du serpent"""
        self.can.delete(ALL)
        self.anim = False
        self.nbrAnneau = 4
        self.anneau = [self.nbrAnneau, self.nbrAnneau+1, self.nbrAnneau +
                       2, self.nbrAnneau+3, self.nbrAnneau+4]  # ADN du Serpent!!!
        self.point = 0
        self.ajout = 1
        self.vie = 3
        self.vitesse = 150
        self.Vbonus = False
        # place la pomme et prend le ID 1
        self.can.create_image(-50, -50, image=self.POMME)
        self.can.create_image(-50, -50, image=self.LIFE)
        self.can.create_image(-50, -50, image=self.POWER)
        self.tete = self.can.create_image(70, 14, image=self.RIGHT)
        print(self.tete)
        # place le 1er anneau qui prend ID 5
        self.can.create_image(56, 14, image=self.CORPS)
        self.can.create_image(42, 14, image=self.CORPS)
        self.can.create_image(28, 14, image=self.CORPS)
        # place le corps et prend les ID qui suivent
        self.can.create_image(14, 14, image=self.CORPS)
        self.lbscore.configure(text='Score : Null')
        self.dirige = False  # verifie si le serpent est deja orienté
        self.anim = False
        # b = self.terrain()#place le terrain

    def resultat(self):

        frame = Frame(self.fen)
        self.lbscore = Label(frame, text='Score : Null',  font='Andalus 14')
        Button(frame, text='Start', font='Andalus 14',
               command=self.commencer).pack()  # start
        Button(frame, text='Restart', font='Andalus 14',
               command=self.recommencer).pack()
        Button(frame, text='Pause',  font='Andalus 14',
               command=self.pause).pack()
        Button(frame, text='Exit', font="Andalus 14",
               command=self.quitter).pack()

        self.lblife = Label(frame, text="Life : 3", font="Andalus 14")
        self.lblevel = Label(frame, text="Level : 0", font="Andalus 14")
        self.lbscore.pack()
        self.lblife.pack()
        self.lblevel.pack()
        frame.pack(side=LEFT)

    def terrain1(self, n=1):  # param n is the nth board to open
        for b in range(self.nbric1, self.nbric2):
            self.can.delete(b)

        b = 0  # last brick
        self.liste_terrain = []  # contains bricks coordinates
        y = 0
        for lign in self.lst_terrain[n]:
            x = 0
            for col in lign:
                if col == "1":
                    self.liste_terrain.append((x, y))
                    self.nbric2 = self.can.create_image(
                        x*14, y*14, image=self.BRIC)  # at the end, it will hold the last brick set
                x += 1
            y += 1

        x, y = int(randint(1, int(self.can.cget('width'))) /
                   14), int(randint(1, int(self.can.cget('height')))/14)
        while (x, y) in self.liste_terrain:
            x, y = int(randint(1, int(self.can.cget('width'))) /
                       14), int(randint(1, int(self.can.cget('height')))/14)
        x, y = x*14, y*14
        self.can.coords(1, x, y)

    def commencer(self):
        if self.anim == False:
            self.anim = True
            self.deplacer()

    def recommencer(self):

        self.initialiser()

    def quitter(self):
        1

    def deplacer(self):
        """Deplacer les anneaux"""

        # coordonnées de l'anneau devant etre deplacé en 1er(le tete)#self.p le nbr de fois qu'il as tourné
        c1 = self.can.coords(self.anneau[0])
        # print(self.anneau[0])
        # print(c1)
        # self.X et Y contiennent les coords de la tete à la queue à la fin de la fonction
        X, Y = c1[0]+self.x, c1[1]+self.y
        found = self.can.find_overlapping(
            X, Y, X, Y)  # objet heurté par la tete
        n = 0  # compteur
        if self.anim == True:
            for a in self.anneau:
                c = self.can.coords(self.anneau[n])
                self.can.coords(a,  X, Y)  # deplacement
                X, Y = c[0], c[1]
                n += 1
            self.dirige = False
            self.can.after(self.vitesse, self.deplacer)
            if self.Vbonus == True:
                self.Tbonus += 2.5  # incremente le temps à chaque deplacement du serpent
               # print(self.Tbonus)
                self.barre.configure(width=self.Tbonus*2)
                if self.Tbonus > 100:  # ***CODE A ADAPTER AU CHANGEMENT DE TAILLE DE L'ECRAN***
                    self.Vbonus = False
                    self.barre.configure(width=1)
                    self.can.coords(2, -50, -50)
                    self.can.coords(3, -50, -50)
        if found == (1,):  # le tag 1 est la nourriture. il le mange
            self.manger()
        elif found == (2,):  # si il trouve la vie, il la mange(remet à -50,-50 pour qu'il soit invisible)
            self.can.coords(2, -50, -50)  # cache le bonus
            self.vie += 1
            # met à jour la vie
            self.lblife.configure(text="Life : " + str(self.vie))
            self.Vbonus = False  # stop la progression de la barre
            self.barre.configure(width=1)  # remet la barre à 0
        elif found == (3,):  # il troule le bonus, +5pts
            self.can.coords(3, -50, -50)  # cache le bonus
            self.point += 5
            self.lbscore.configure(
                text="Score : " + str(self.point))  # met à jour la vie
            self.Vbonus = False  # stop la progression de la barre
            self.barre.configure(width=0)  # remet la barre à 0

        elif found == ():  # ne touve rien, il avance
            1
        else:  # il trouve autre chose, il meurt!!!
            print(found[0])
            self.echec()
            self.anim = False
        c1 = self.can.coords(self.anneau[0])
        # entre dans les bordures(sans mur)
        x = int(int(self.can.cget('width'))/14)*14
        if c1[0] < 0:  # entre à gauche
            self.can.coords(self.anneau[0], x, c1[1])
        elif c1[0] > x:  # entre à droite d canvas
            self.can.coords(self.anneau[0], 0, c1[1])

        y = int(int(self.can.cget('height'))/14)*14
        if c1[1] < 0:  # entre en haut
            self.can.coords(self.anneau[0], c1[0], y)
        elif c1[1] > y:  # entre en bas
            self.can.coords(self.anneau[0], c1[0], 0)
        if self.point > 50:
            self.n += 1
            self.anim = False
            self.nbrAnneau = 4
            self.anneau = [self.nbrAnneau, self.nbrAnneau+1, self.nbrAnneau +
                           2, self.nbrAnneau+3, self.nbrAnneau+4]  # ADN du Serpent!!!
            self.point = 0
            self.ajout = 1
            self.vie = 3
            self.vitesse = 200
            self.Vbonus = False
            print(self.can.find_all())
            self.terrain1(self.n)
            i = 5
            self.can.coords(4, 70, 14)
            self.x = 14
            self.y = 0
            self.can.itemconfig(self.tete, image=self.RIGHT)
            for x in range(56, 0, -14):
                self.can.coords(i, x, 14)
                i += 1

    def gauche(self, event):

        if self.dirige == False:
            if self.x != 14:
                self.x = -14
                self.y = 0
                # modifie l'image
                self.can.itemconfig(self.tete, image=self.LEFT)
                self.dirige = True

    def droite(self, event):

        if self.dirige == False:
            if self.x != -14:
                self.can.itemconfig(self.tete, image=self.RIGHT)
                self.x = 14
                self.y = 0
                self.dirige = True

    def haut(self, event):

        if self.dirige == False:
            if self.y != 14:
                self.can.itemconfig(self.tete, image=self.UP)
                self.y = -14
                self.x = 0
                self.dirige = True

    def bas(self, event):

        if self.dirige == False:
            if self.y != -14:
                self.x = 0
                self.y = 14
                self.can.itemconfig(self.tete, image=self.DOWN)
                self.dirige = True

    def pause1(self):
        if self.anim == True:
            self.anim = False
        else:
            self.anim = True
            self.deplacer()

    def pause(self, event):

        self.pause1()

    def score(self):

        self.lbscore.configure(text='Score :' + str(self.point))

    def echec(self):

        if self.anim == True:
            if self.vie == 0:
                self.anim = "Echec"
                showerror("Game over", "Vous avez echoué !!!")
                self.fen.destroy()
            else:
                self.vie -= 1
                self.lblife.configure(text="Life : " + str(self.vie))

    def manger(self):
        """ Le serpent mange la pomme = +1pt, vie = +1vie , powerup = +5pts ..."""
        x, y = int(randint(1, int(self.can.cget('width'))) /
                   14), int(randint(1, int(self.can.cget('height')))/14)
        while (x, y) in self.liste_terrain:
            x, y = int(randint(1, int(self.can.cget('width'))) /
                       14), int(randint(1, int(self.can.cget('height')))/14)
        x, y = x*14, y*14
        self.can.coords(1, x, y)  # ID 1 est la pomme rouge
        self.point += self.ajout
        d = self.can.coords(self.anneau[self.nbrAnneau])
        if self.point % 2 == 0:
            self.nbrAnneau += 1
            s = self.can.create_image(
                d[0]+self.x, d[1]+self.y, image=self.CORPS)
            # on ajoute à la liste des anneaux la nouvelle queue à la fin de la liste
            self.anneau.insert(self.nbrAnneau, s)
        if self.point % 11 == 0:
            x, y = int(randint(1, int(self.can.cget('width'))) /
                       14), int(randint(1, int(self.can.cget('height')))/14)
            while (x, y) in self.liste_terrain:
                x, y = int(randint(1, int(self.can.cget('width'))) /
                           14), int(randint(1, int(self.can.cget('height')))/14)
            x, y = x*14, y*14
            self.can.coords(2, x, y)
            self.Vbonus = True
            # le temps que fera le bonus (le nbr de pas"poussé" que doit faire le serpent durant ce temps)
            self.Tbonus = 0
        if self.point % 7 == 0:
            x, y = int(randint(1, int(self.can.cget('width'))) /
                       14), int(randint(1, int(self.can.cget('height')))/14)
            while (x, y) in self.liste_terrain:  # liste terrain contient les coords des murs
                x, y = int(randint(1, int(self.can.cget('width'))) /
                           14), int(randint(1, int(self.can.cget('height')))/14)
            x, y = x*14, y*14
            self.can.coords(3, x, y)
            self.Vbonus = True
            # le temps que fera le bonus (le nbr de pas"poussé" que doit faire le serpent durant ce temps)
            self.Tbonus = 0
            self.vitesse -= 10
        self.lbscore.configure(text='Score : ' + str(self.point))
        print(self.point)
        self.nbric2 += 1  # on considere le que ajouté comme bric car elle seras enlevée lors du changement de stage


app = Serpent()
