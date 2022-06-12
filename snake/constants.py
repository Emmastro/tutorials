INIT = 0
PLAYING = 1
PAUSE = 2
FAILED = 3
MAXIMUM_POINT = 30
GRID_SIZE = 14
BOARD_WIDTH = 364
BOARD_HEIGHT = 364
FOOD_POINT = 1
BONUS_POINT = 5
FONT = 'Andalus 13'
INCREMENT_BONUS_TIME = 2.5
DISPLAY_POWER_FREQUENCY = 3
GROWTH_FREQUENCY = 2

IMAGES = [
    'left', 'right', 'up', 'down',
    'body', 'food', 'power', 'bric'
]

DIRECTION = {'left': {
    'x_change': -1,
    'y_change': 0,
    'condition': 'x'
},
    'right': {
    'x_change': 1,
    'y_change': 0,
    'condition': 'x'
},
    'up': {
    'x_change': 0,
    'y_change': -1,
    'condition': 'y'
},
    'down': {
    'x_change': 0,
    'y_change': 1,
    'condition': 'y'
}
}
