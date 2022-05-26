# Snake
from tkinter import*
from random import*
from tkinter.messagebox import showerror
from time import time
from constants import *


class Serpent(Tk):
    def __init__(self):
        """
        """
        super().__init__()
        self.debut = time()
        #self.title("SNAKE Version 1.2")

        self.init_menu()
        self.photo_images = {direction: PhotoImage(
            file=f'images/v1/{direction}.gif') for direction in IMAGES}

        self.init_data()
        main_frame = Frame(self)
        self.board_canvas = Canvas(main_frame, width=BOARD_WIDTH,
                          height=BOARD_HEIGHT, bg='pink')
        self.set_result_section()
        self.set_level()
        self.init_board()
        self.init_snake()
        self.board_canvas.pack(side=TOP)

        Label(main_frame, text="Duration : ", font=FONT).pack(side=LEFT)
        self.barre = Canvas(main_frame, width=1, height=15, bg='green')
        self.barre.pack(side=LEFT)

        main_frame.pack(side=BOTTOM)
        self.board_canvas.focus_set()
        self.bind_events()
        self.mainloop()

    def bind_events(self):

        self.board_canvas.bind('<Up>', self.move)
        self.board_canvas.bind('<Down>', self.move)
        self.board_canvas.bind('<Left>', self.move)
        self.board_canvas.bind('<Right>', self.move)
        self.board_canvas.bind('<space>', self.pause)

    def init_menu(self):

        menu_frame = Frame(borderwidth=2)
        menu_frame.pack(side=TOP)
        self.config_menu_button = Menubutton(
            menu_frame, text='Configuration', font=FONT)
        self.config_menu = Menu(self.config_menu_button)
        self.config_menu.add_command(
            label='Board', font=FONT, command=self.select_level)
        self.config_menu_button.configure(menu=self.config_menu)
        self.config_menu_button.pack(side=LEFT)
        

    def init_data(self):
        """
        
        """

        with open(file="board.txt") as data_file:
            self.board_names = []
            self.board_data = [[]]
            data = data_file.readlines()
            current_board = -1  # will be set to 0 on the first loop
            for row in data:
                if "Terrain" in row:
                    self.board_names.append(row)
                    current_board += 1
                    self.board_data.append([])  # and new empty board
                    continue

                self.board_data[current_board].append(row.strip())


    def init_snake(self):
        """
        initialise les anneaux du serpent
        """

        self.game_state = INIT
        self.body_size = 4

        self.food_image = self.board_canvas.create_image(-50, -50,
                                                image=self.photo_images['food'])
        self.life_image = self.board_canvas.create_image(
            -50, -50, image=self.photo_images['life'])
        self.power_image = self.board_canvas.create_image(-50, -50, image=self.photo_images['power'])
        self.head = self.board_canvas.create_image(
            70, GRID_SIZE, image=self.photo_images['right'])
        self.board_canvas.create_image(56, GRID_SIZE, image=self.photo_images['body'])
        self.board_canvas.create_image(42, GRID_SIZE, image=self.photo_images['body'])
        self.board_canvas.create_image(28, GRID_SIZE, image=self.photo_images['body'])
        self.board_canvas.create_image(GRID_SIZE, GRID_SIZE,
                              image=self.photo_images['body'])

        self.body_items = list(range(self.head, self.head+5))

        self.lbscore.configure(text='Score : Null')
        self.dirige = False  # verifie si le serpent est deja orienté

    def select_level(self):
        """
        """

        self.select_level_window = Toplevel()
        self.select_level_window.title("Board")
        menu_frame = Frame(self.select_level_window)
        Label(menu_frame, text="Boards", font="Andalus 14").pack(side=TOP)
        self.board_list = Listbox(menu_frame, font="Andalus 14")

        self.preview_canvas = Canvas(
            self.select_level_window, width=BOARD_WIDTH, height=BOARD_HEIGHT)
        self.preview_canvas.pack(side=RIGHT)
        self.board_list.bind('<Button-1>', self.preview_board)
        for t in self.board_names:
            self.board_list.insert(END, t)
        self.board_list.pack(side=LEFT)
        Button(self.select_level_window, text="Charger", fon="Andalus 14",
               command=self.update_board).pack(side=BOTTOM)
        menu_frame.pack(side=LEFT)
        self.select_level_window.mainloop()

    def set_result_section(self):
        """

        """

        frame = Frame(self)
        self.lbscore = Label(frame, text='Score : Null',  font=FONT)
        Button(frame, text='Start', font=FONT,
               command=self.start).pack()
        Button(frame, text='Restart', font=FONT,
               command=self.recommencer).pack()
        Button(frame, text='Pause',  font=FONT,
               command=self.pause).pack()
        Button(frame, text='Exit', font=FONT,
               command=self.quitter).pack()

        self.lblife = Label(frame, text="Life : 3", font="Andalus 14")
        self.lblevel = Label(frame, text="Level : 0", font="Andalus 14")
        self.lbscore.pack()
        self.lblife.pack()
        self.lblevel.pack()

        frame.pack(side=LEFT)

    def quitter(self, event):
        """

        """
        pass


    def init_board(self):
        """
        """
        self.bricks_coords = []
        self.set_bricks(self.board_canvas, self.current_level)     


    def set_bricks(self, canvas, level_selected, preview=False):
        """
        """

        canvas.delete(ALL)

        for y, col in enumerate(self.board_data[level_selected]):
            for x, lign in enumerate(col):
                if lign == '1':
                    if not preview:
                        self.bricks_coords.append((x, y))
                    canvas.create_image(
                        x*GRID_SIZE, y*GRID_SIZE, image=self.photo_images['bric'])
                        

    def preview_board(self, event):
        """
        Affiche le terrain choisi dans la liste au Canvas
        """
        level_selected = self.board_list.curselection()
        if level_selected != ():
            self.set_bricks(self.preview_canvas, level_selected[0])

    def update_board(self):
        """
        """
        level_selected = self.board_list.curselection()
        if level_selected != ():
            self.current_level = level_selected[0]
            self.init_board()
            self.init_snake()
            self.select_level_window.destroy()

    def start(self):
        """

        """
        if self.game_state == INIT:
            self.game_state = PLAYING
            self.play()

    def recommencer(self):
        """

        """
        self.initialiser()

    def set_level(self, level=0):
        """

        """

        self.point = 0
        self.life = 3
        self.speed = 150 + 50*level
        self.bonus_active = False
        self.current_level = level + 1
        self.x = GRID_SIZE
        self.y = 0

    def play(self):
        """
        Deplacer les anneaux
        """

        head = self.board_canvas.coords(self.body_items[0])
        head_x, head_y = head[0]+self.x, head[1]+self.y
        # check if the head overlaps with any other item
        found = self.board_canvas.find_overlapping(head_x, head_y, head_x, head_y)
    
        if self.game_state == PLAYING:
            for i, body_item in enumerate(self.body_items):
                # on the first loop, the head takes the position incremented y self.x and self.y
                # the rest of the iterations, each body item takes the position of the item right in front of them
                hold_position = self.board_canvas.coords(self.body_items[i])
                self.board_canvas.coords(body_item,  head_x, head_y)
                head_x, head_y = hold_position[0], hold_position[1]

            self.dirige = False
            self.board_canvas.after(self.speed, self.play)
            if self.bonus_active == True:
                self.bonus_time += 2.5  # incremente le temps à chaque deplacement du serpent

                self.barre.configure(width=self.bonus_time*2)
                if self.bonus_time > 100:
                    self.bonus_active = False
                    self.barre.configure(width=1)
                    self.board_canvas.coords(2, -50, -50)
                    self.board_canvas.coords(3, -50, -50)

        if found == ():
            pass
        elif found == self.food_image:
            self.manger()

        elif found == self.life_image:
            self.board_canvas.coords(self.life_image, -50, -50)  # life
            self.life += 1
            self.lblife.configure(text="Life : " + str(self.life))
            self.bonus_active = False
            self.barre.configure(width=1)

        elif found == (3,):
            self.board_canvas.coords(3, -50, -50)  # cache le bonus
            self.point += BONUS_POINT
            self.lbscore.configure(text="Score : " + str(self.point))
            self.bonus_active = False  # stop la progression de la barre
            self.barre.configure(width=0)  # remet la barre à 0

        elif found == ():
            # ne touve rien, il avance
            pass

        else:
            # il trouve autre chose, il meurt!!!
            self.echec()
            self.game_state = FAILED

        head_cords = self.board_canvas.coords(self.body_items[0])
        # entre dans les bordures(sans mur)
        if head_cords[0] < 0:  # entre à gauche
            self.board_canvas.coords(self.body_items[0], BOARD_WIDTH, head_cords[1])
        elif head_cords[0] > BOARD_WIDTH:
            # entre à droite d canvas
            self.board_canvas.coords(self.body_items[0], 0, head_cords[1])

        if head_cords[1] < 0:  # entre en haut
            self.board_canvas.coords(self.body_items[0], head_cords[0], BOARD_HEIGHT)
        elif head_cords[1] > BOARD_HEIGHT:  # entre en bas
            self.board_canvas.coords(self.body_items[0], head_cords[0], 0)

        if self.point > MAXIMUM_POINT:  # new level
            self.current_level += 1
            self.game_state = INIT
            self.body_size = 4
            # TODO: logic to reset snake size should be same is setting snake at the beggining
            self.body_items = [self.body_size, self.body_size+1, self.body_size +
                               2, self.body_size+3, self.body_size+4]
            self.set_level(1)
            self.init_board()
            i = 5
            self.board_canvas.coords(4, 70, GRID_SIZE)
            self.board_canvas.itemconfig(self.head, image=self.photo_images['right'])
            for x in range(56, 0, -GRID_SIZE):
                self.board_canvas.coords(i, x, GRID_SIZE)
                i += 1

    def move(self, event):

        key = event.keysym.lower()

        if getattr(self, DIRECTION[key]['condition']) != GRID_SIZE:
            # Update the head's direction
            self.board_canvas.itemconfig(self.head, image=self.photo_images[key])
            self.x = DIRECTION[key]['x_change']*GRID_SIZE
            self.y = DIRECTION[key]['y_change']*GRID_SIZE

    def pause(self, event):

        if self.game_state == PLAYING:
            self.game_state = PAUSE
        elif self.game_state == PAUSE:
            self.game_state = PLAYING
            self.play()

    def score(self):

        self.lbscore.configure(text='Score :' + str(self.point))

    def echec(self):
        """

        """
        if self.game_state == True:
            if self.life == 0:
                self.game_state = FAILED
                showerror("Game over", "Vous avez echoué !!!")
                self.destroy()
            else:
                self.life -= 1
                self.lblife.configure(text="Life : " + str(self.life))

    def get_random_free_position(self):
        """
        returns an x, y position that don't collide with the walls or the snake body
        """
        x = randint(1, BOARD_WIDTH)//GRID_SIZE
        y = randint(1, BOARD_HEIGHT)//GRID_SIZE

        while (x, y) in self.bricks_coords:  # liste terrain contient les coords des murs
            x = randint(1, BOARD_WIDTH)//GRID_SIZE
            y = randint(1, BOARD_HEIGHT)//GRID_SIZE

        return x * GRID_SIZE, y * GRID_SIZE

    def manger(self):
        """
        """
        x, y = self.get_random_free_position()

        self.board_canvas.coords(self.food_image, x, y)
        self.point += FOOD_POINT
        d = self.board_canvas.coords(self.body_items[self.body_size])

        if self.point % 2 == 0:  # the snake grows by one unit every 2 points
            self.body_size += 1
            s = self.board_canvas.create_image(
                d[0]+self.x, d[1]+self.y, image=self.photo_images['body'])
            self.body_items.insert(self.body_size, s)

        if self.point % 11 == 0:
            x, y = self.get_random_free_position()
            self.board_canvas.coords(self.life_image, x, y)
            self.bonus_active = True
            self.bonus_time = 0

        if self.point % 7 == 0:
            x, y = self.get_random_free_position()
            self.board_canvas.coords(3, x, y)
            self.bonus_active = True
            self.bonus_time = 0
            self.speed -= 10
        
        self.lbscore.configure(text='Score : ' + str(self.point))

app = Serpent()
