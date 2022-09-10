from tkinter import *
from tkinter import messagebox
import settings


root = Tk()
root.title("Tic-Tac-Toe")
root.resizable(False, False)


class Game:

    def __init__(self, turn=True, players=settings.DEFAULT_PLAYERS, filled_space_counter=0):
        self.turn = turn  # True = player x's turn
        self.players = players
        self.filled_space_counter = filled_space_counter  # used to detect draw game
        self.label_turn_indicator = StringVar()
        self.label_turn_indicator.set(f'Player {self.players[0] if self.turn else self.players[1]}\'s turn')

        # create label indicating player's turn
        player_turn_label = Label(root, textvariable=self.label_turn_indicator,
                                  font=('Arial', 8), fg='#0f274d', pady=5)
        player_turn_label.grid(column=1, row=0)


class Board:

    all = []

    def __init__(self, x, y, is_empty=True):
        self.is_empty = is_empty
        self.cell_btn_object = None
        self.x = x
        self.y = y

        Board.all.append(self)

    def create_btn_object(self, location):
        btn = Button(location, text='', width=settings.CELL_WIDTH, height=settings.CELL_HEIGHT, bg=settings.BG_COLOR,
                     command=lambda x=self.x, y=self.y: self.click_actions(game.turn))
        self.cell_btn_object = btn

    def click_actions(self, turn):

        end_game = False

        if self.is_empty:
            self.cell_btn_object.configure(text=f'{game.players[0] if turn else game.players[1]}')
            self.is_empty = False

            if Board.check_win():
                messagebox.showinfo(title=None, message=f'Player {game.players[0] if game.turn else game.players[1]} wins!')
                end_game = True

            game.filled_space_counter += 1
            if game.filled_space_counter == settings.GRID_SIZE * settings.GRID_SIZE and not end_game:
                messagebox.showinfo(title=None, message=f'Draw game!')
                end_game = True

            game.turn = not game.turn
            game.label_turn_indicator.set(f'Player {game.players[0] if game.turn else game.players[1]}\'s turn')

            # reset if game ends
            if end_game:
                game.turn = True
                game.label_turn_indicator.set(f'Player {game.players[0] if game.turn else game.players[1]}\'s turn')
                game.filled_space_counter = 0
                for i in range(len(Board.all)):
                    Board.all[i].cell_btn_object.config(text='', bg=settings.BG_COLOR)
                    Board.all[i].is_empty = True

        else:
            messagebox.showinfo(title=None, message=f'Please click on an empty square.')

    @classmethod
    def check_win(cls):

        winning_coord = []  # array to record winning cells to facilitate change in color
        win = False

        # check rows and columns
        for i in range(settings.GRID_SIZE):
            if Board.all[i * settings.GRID_SIZE].cell_btn_object['text'] == Board.all[i * settings.GRID_SIZE + 1].cell_btn_object['text'] == \
                    Board.all[i * settings.GRID_SIZE + 2].cell_btn_object['text'] != '':
                winning_coord = [i * settings.GRID_SIZE, i * settings.GRID_SIZE + 1, i * settings.GRID_SIZE + 2]
                win = True

            if Board.all[i].cell_btn_object['text'] == Board.all[i + settings.GRID_SIZE].cell_btn_object['text'] == \
                    Board.all[i + settings.GRID_SIZE * 2].cell_btn_object['text'] != '':
                winning_coord = [i, i + settings.GRID_SIZE, i + settings.GRID_SIZE * 2]
                win = True

        # check diagonals
        if Board.all[0].cell_btn_object['text'] == Board.all[4].cell_btn_object['text'] == \
                Board.all[8].cell_btn_object['text'] != '':
            winning_coord = [0, 4, 8]
            win = True

        if Board.all[2].cell_btn_object['text'] == Board.all[4].cell_btn_object['text'] == \
                Board.all[6].cell_btn_object['text'] != '':
            winning_coord = [2, 4, 6]
            win = True

        # change color of winning cells
        if win:
            for k in range(len(winning_coord)):
                Board.all[winning_coord[k]].cell_btn_object['bg'] = '#fca14c'

        return win


# commence game
game = Game()

# create buttons
for x in range(settings.GRID_SIZE):
    for y in range(1, settings.GRID_SIZE+1):
        b = Board(x, y)
        b.create_btn_object(root)
        b.cell_btn_object.grid(column=x, row=y)

# run the window
root.mainloop()
