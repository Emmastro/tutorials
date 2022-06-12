from tkinter import *
from random import randint
from tkinter.messagebox import showinfo, showinfo
from time import time
from constants import *


class Snake(Tk):

    def __init__(self):

        super().__init__()
        self.debut = time()
        self.title("SNAKE Version 2")

        self.init_menu()
        self.photo_images = {image: PhotoImage(
            file=f'images/v2/{image}.gif') for image in IMAGES}

        self.init_data()
        main_frame = Frame(self)
        self.board_canvas = Canvas(main_frame, width=BOARD_WIDTH,
                                   height=BOARD_HEIGHT, bg='pink')
        self.set_result_section()
        self.set_level()
        self.init_board()
        self.init_snake()
        self.board_canvas.pack(side=TOP)

        Label(main_frame, text="Timer : ", font=FONT).pack(side=LEFT)
        self.barre = Canvas(main_frame, width=1, height=15, bg='green')
        self.barre.pack(side=LEFT)

        main_frame.pack(side=BOTTOM)
        self.board_canvas.focus_set()
        self.bind_events()
        self.mainloop()

    def bind_events(self):
        """
        Binds supported keyboard (directions for movement and space for pause) events 
        """
        self.board_canvas.bind('<Up>', self.move)
        self.board_canvas.bind('<Down>', self.move)
        self.board_canvas.bind('<Left>', self.move)
        self.board_canvas.bind('<Right>', self.move)
        self.board_canvas.bind('<space>', self.pause)

    def init_menu(self):
        """
        Initialize the top menu used to select a level
        """
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
        Loads board data from the board.txt file in memory, with the board_data attribute
        """
        with open(file="data/board.txt") as data_file:
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

    def init_board(self):
        """
        Initialize the board with the selected level. 
        """
        self.bricks_coords = []
        self.set_bricks(self.board_canvas, self.current_level)

        x, y = self.get_random_free_position()
        self.food_image = self.board_canvas.create_image(x, y,
                                                         image=self.photo_images['food'])

        self.power_image = self.board_canvas.create_image(
            -50, -50, image=self.photo_images['power'])

    def set_bricks(self, canvas, level_selected, preview=False):
        """Sets the bricks on the board, for a selected level 

        Args:
            canvas (Canvas): the canvas where the bricks will be drawn
            level_selected (int) : the level selected by the user
            preview (Boolean): if True, the bricks will be drawn on the preview canvas, 
            Otherwise on the main canvas (default: False)
        """
        canvas.delete(ALL)

        for y, row in enumerate(self.board_data[level_selected]):
            for x, cell in enumerate(row):
                if cell == '1':
                    if not preview:
                        self.bricks_coords.append((x, y))
                    canvas.create_image(
                        x*GRID_SIZE, y*GRID_SIZE, image=self.photo_images['bric'])

    def init_snake(self):
        """Initialize the snake body on the board
        """
        self.game_state = INIT
        self.body_size = 4

        self.body_items = []
        self.head = self.board_canvas.create_image(
            70, GRID_SIZE, image=self.photo_images['right'])

        self.body_items.append(self.head)
        for i in range(self.body_size, 0, -1):
            self.body_items.append(
                self.board_canvas.create_image(
                    GRID_SIZE*i, GRID_SIZE, image=self.photo_images['body'])
            )

        self.label_score.configure(text='Score : 0')

    def select_level(self):

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
        Button(self.select_level_window, text="Load", fon="Andalus 14",
               command=self.update_board).pack(side=BOTTOM)
        menu_frame.pack(side=LEFT)
        self.select_level_window.mainloop()

    def set_result_section(self):

        frame = Frame(self)
        self.label_score = Label(frame, text='Score : 0',  font=FONT)
        Button(frame, text='Start', font=FONT,
               command=self.start).pack()
        Button(frame, text='Restart', font=FONT,
               command=self.restart).pack()
        Button(frame, text='Pause',  font=FONT,
               command=self.pause).pack()
        Button(frame, text='Exit', font=FONT,
               command=self.destroy).pack()

        self.label_level = Label(frame, text="Level : 0", font="Andalus 14")
        self.label_score.pack()
        self.label_level.pack()

        frame.pack(side=LEFT)

    def preview_board(self, event):

        level_selected = self.board_list.curselection()
        if level_selected != ():
            self.set_bricks(self.preview_canvas, level_selected[0])

    def update_board(self):

        level_selected = self.board_list.curselection()
        if level_selected != ():
            self.set_level(level_selected[0])
            self.init_board()
            self.init_snake()
            self.select_level_window.destroy()

    def start(self):

        if self.game_state == INIT:
            self.game_state = PLAYING
            self.play()

    def restart(self):

        for body_item in self.body_items:  # delete current snake
            self.board_canvas.delete(body_item)
        self.set_level(self.current_level)
        self.init_snake()
        self.game_state = INIT

    def set_level(self, level=1):

        self.point = 0
        self.speed = 150 + 50*level
        self.bonus_active = False
        self.current_level = level
        self.label_level.configure(text="Level : " + str(self.current_level))
        self.x = GRID_SIZE
        self.y = 0

    def play(self):

        head_cords = self.board_canvas.coords(self.body_items[0])
        head_x, head_y = head_cords[0]+self.x, head_cords[1]+self.y
        # check if the head overlaps with any other item
        found = self.board_canvas.find_overlapping(
            head_x, head_y, head_x, head_y)

        if self.game_state == PLAYING:
            for i, body_item in enumerate(self.body_items):
                # on the first loop, the head takes the position incremented y self.x and self.y
                # the rest of the iterations, each body item takes the position of the item right in front of them
                hold_position = self.board_canvas.coords(self.body_items[i])
                self.board_canvas.coords(body_item,  head_x, head_y)
                head_x, head_y = hold_position[0], hold_position[1]

            self.board_canvas.after(self.speed, self.play)
            if self.bonus_active:
                self.bonus_time += INCREMENT_BONUS_TIME

                self.barre.configure(width=self.bonus_time*2)
                if self.bonus_time > 100: # bonus time is over
                    self.bonus_active = False
                    self.barre.configure(width=0) # reset bonus time bar
                    self.board_canvas.coords(self.power_image, -50, -50) # hide power image

        if found == ():
            pass

        elif found[0] == self.food_image:
            self.eat()

        elif found[0] == self.power_image:
            self.board_canvas.coords(self.power_image, -50, -50) # hide power image
            self.point += BONUS_POINT
            self.label_score.configure(text="Score : " + str(self.point))
            self.bonus_active = False
            self.barre.configure(width=0)

        else:  # overlap with an item that's not edible
            self.failure()
            self.game_state = FAILED

        self.handle_borderless_board()

    def failure(self):

        self.game_state = FAILED
        showinfo("Game over", "Vous avez echoué !!!")

    def handle_borderless_board(self):
        """
        Handle the case where the snake is out of the board, on a level without borders
        """
        head_cords = self.board_canvas.coords(self.body_items[0])
        if head_cords[0] < 0: # out of the left border. the snakes appears on the right side
            self.board_canvas.coords(
                self.body_items[0], BOARD_WIDTH, head_cords[1])
        elif head_cords[0] > BOARD_WIDTH: # out of the right border. the snakes appears on the left side
            self.board_canvas.coords(self.body_items[0], 0, head_cords[1])

        elif head_cords[1] < 0: # out of the top border. the snakes appears on the bottom side
            self.board_canvas.coords(
                self.body_items[0], head_cords[0], BOARD_HEIGHT)
        elif head_cords[1] > BOARD_HEIGHT:  # out of the bottom border. the snakes appears on the top side
            self.board_canvas.coords(self.body_items[0], head_cords[0], 0)

    def move(self, event):
        """
        Move the snake according to the key pressed
        """
        key = event.keysym.lower()

        if getattr(self, DIRECTION[key]['condition']) != GRID_SIZE:
            
            self.board_canvas.itemconfig(
                self.head, image=self.photo_images[key]) # Update the head's direction
            self.x = DIRECTION[key]['x_change']*GRID_SIZE
            self.y = DIRECTION[key]['y_change']*GRID_SIZE

    def pause(self, event=None):
        """
        Pause or resume the game
            event : the event that triggered the pause. 
            Set to None by default as it can be caused without being triggered by a keyboard
            event (when the pause button is pressed)
        """

        if self.game_state == PLAYING:
            self.game_state = PAUSE
        elif self.game_state == PAUSE:
            self.game_state = PLAYING
            self.play()

    def get_random_free_position(self):
        """
        returns: x, y position that don't collide with the walls or the snake body
        """

        x = randint(1, BOARD_WIDTH)//GRID_SIZE
        y = randint(1, BOARD_HEIGHT)//GRID_SIZE

        # generate new random value for x and y if they collide with a brick
        while (x, y) in self.bricks_coords:
            x = randint(1, BOARD_WIDTH)//GRID_SIZE
            y = randint(1, BOARD_HEIGHT)//GRID_SIZE

        return x * GRID_SIZE, y * GRID_SIZE

    def eat(self):
        """
        
        """

        x, y = self.get_random_free_position()
        # reset position of the food when the head collides with it
        self.board_canvas.coords(self.food_image, x, y) 
        self.point += FOOD_POINT
        last_body_item_coords = self.board_canvas.coords(self.body_items[self.body_size])

         # Add a new body part to the snake after every `GROWTH_FREQUENCY` points
        if self.point % GROWTH_FREQUENCY == 0:
            self.body_size += 1
            self.body_items.append(
                self.board_canvas.create_image(
                    last_body_item_coords[0]+self.x, last_body_item_coords[1]+self.y, image=self.photo_images['body']
                )
            )

        # display the bonus image every `DISPLAY_POWER_FREQUENCY` points
        if self.point % DISPLAY_POWER_FREQUENCY == 0:
            x, y = self.get_random_free_position()
            self.board_canvas.coords(self.power_image, x, y)
            self.bonus_active = True
            self.bonus_time = 0

        if self.point > MAXIMUM_POINT:  # new level
            self.current_level += 1
            self.init_board() # set the board for the new level
            self.restart()

        self.label_score.configure(text='Score : ' + str(self.point))

app = Snake()
