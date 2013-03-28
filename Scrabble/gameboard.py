from tkinter import *
import tiles
import player
import validation
import copy
#gamestate contains info on the game as it progresses

#Standard board dimensions are 15x15,which won't be hardcoded but are not meant
#to be changed, as it messes with the scoring
BOARD_COLUMNS = 15
BOARD_ROWS = 15

class gamestate:
    def __init__(self,player_num):
        #number of players is between 2 and 4
        self._player_num = player_num
        self._board = self._new_board()
        self._tiles = tiles.Tiles()
        
    def _new_board(self):
        '''creates fresh game with dimensions 15x15'''
        board = [[None]*15 for _ in range(15)]
        return board

    def make_move(self,column,row,word,movetype):
        if movetype == 'vertical':
            self._vertical_move(column,row,word)
        elif movetype == 'horizontal':
            self._horizontal_move(column,row,word)
        
    def _horizontal_move(self,column,row,word):
        '''makes a horizontal move to the right'''
        for letter,x in zip(word,range(len(word))):
            if letter == ' ':   #allows user to skip over occupied space
                continue
            self._write_one_letter(column,row+x,letter)
    def _vertical_move(self,column,row,word):
        '''makes a vertical move downwards'''
        for letter,x in zip(word,range(len(word))):
            if letter == ' ':   #allows user to skip over occupied space
                continue
            self._write_one_letter(column+x,row,letter)
    def _write_one_letter(self,column,row,letter):
        '''writes down a letter to board, raises exception if not already empty'''
        if  self._board[column][row] != None:
            raise ValueError()
        self._board[column][row] = letter

    def print_board(self):
        board_string = ''
        for y in range(BOARD_COLUMNS):
            for x in range(BOARD_ROWS):
                if self._board[y][x] == None:
                    board_string += ' . '
                else:
                    board_string += ' {} '.format(self._board[y][x])
            board_string+='\n'
        return board_string
                
                
            
class PlayerNumbers:
    '''reads in information on how many players (2-4)'''
    def __init__(self):
        self._player_number = Toplevel()

        self.label = Label(
            self._player_number,text = 'How many players?')
        self.label.grid(row=0,column=0)

        self.spinbox = Spinbox(
            self._player_number,from_ = 2,to = 4,width=5)
        self.spinbox.grid(row=0,column=1)

        self.ok_button = Button(
            self._player_number, text = 'OK',command = self._on_ok)
        self.ok_button.grid(row=1,column=0)

        self.cancel_button = Button(
            self._player_number, text = 'Cancel',command = self._on_cancel)
        self.cancel_button.grid(row=1,column=1)

    def _on_ok(self):
        self.number = self.spinbox.get()
        self._player_number.destroy()

    def _on_cancel(self):
        self._player_number.destroy()

    def show(self):
        self._player_number.grab_set()
        self._player_number.wait_window()



class GUI:
    def __init__(self,gamestate):
        self._gamestate = gamestate
        self._board = self._gamestate._board
        self.root = Tk()
        self.player_list = []
        self._current_player = None
        self.tiles = tiles.Tiles()

        #move data fields
        self._movetype = StringVar()
        self._word = StringVar()
        self._game = StringVar()
        self._error = StringVar()
        self._exchange_pieces_var = StringVar()

        #game data fields
        self._turn = StringVar()
        self._score = StringVar()
        self._letters = StringVar()
        
    def board(self):
        return self._board

    ### BUTTON PRESS ###
    def submit_move(self):
        '''final button user pushes to make a move after taking in
            -movetype
            -starting position
            -word
            '''
        column = int(self.spinbox2.get())
        row = int(self.spinbox1.get())
        movetype = self._movetype.get()
        word = self._word.get()
        '''
        print(self._validate_letters())
        print(self._validate_dictionary(column,row,word,movetype))'''
        try:
            self._gamestate.make_move(column,row,word,movetype)
            self.button.config(state=DISABLED)
            self.turnover.config(state=NORMAL)
            self.exchange_button.config(state=DISABLED)
            self._current_player.exchange_pieces(word)
        except:
            self._error.set('ERROR: INVALID MOVE')
        else:
            self._error.set('VALID MOVE')
        finally:
            self._game.set(self._gamestate.print_board())
            
            
    def turn_over(self):
        '''hands the move over to the next player

           -reactivates the 'press to move button'
           -updates the information on left(player turn, score, list of letters)
           -resets all variable fields(word entry, coordinates, movetype)
           '''
        self.button.config(state=NORMAL)
        self.turnover.config(state=DISABLED)
        self.exchange_button.config(state=NORMAL)
        
        self._current_player = self._set_new_player()
        
        self._turn.set(self._current_player._player_number)
        self._score.set('In Progress')
        self._letters.set(self._current_player.current_hand())

    def exchange_pieces(self):
        self.button.config(state=DISABLED)
        self.turnover.config(state=NORMAL)
        self.exchange_button.config(state=DISABLED)

        word = self._exchange_pieces_var.get()
        self._current_player.exchange_pieces(word)
        self._set_new_player()        

    

    def _set_new_player(self):
        '''sets the current player to the next one on the list'''
        previous_number = self._current_player._player_number
        try:
            result = self.player_list[previous_number]
            return result
        except:
            return self.player_list[0]
    def _validate_letters(self):
        '''validates that the user has sufficient letters to make the move'''
        list_of_letters = list(self._word.get())

        #compiles dictionary with values of letters of the word
        letter_dict = {}
        for item in self._current_player._current_hand:
            if item not in letter_dict:
                letter_dict[item] = 1
            else:
                letter_dict[item] += 1

        #checks the word dictionary against current letters in hand
        for item in list_of_letters:
            try:
                letter_dict[item] -= 1
                if letter_dict[item] < 0:
                    return False
            except:
                return False
        return True
    def _validate_dictionary(self,column,row,word,movetype):
        '''ensures the desired move creates words that are in the dictionary'''
        temp_gamestate = copy.copy(self._gamestate)
        temp_gamestate.make_move(column,row,word,movetype)
        valid = validation.execute(temp_gamestate._board)

        return True if valid else False

        


    ### BOARD INITIALIZATION ###
            
    def setup(self):
        '''initializes all widgets in application frame'''

        ###SET UP PLAYERS AND PLAYER INFORMATION
        self.dialog = PlayerNumbers()
        self.dialog.show()

        #create players
        self.player_list = [player.Player(self.tiles,x+1) for x in range(int(self.dialog.number))]
        self._current_player = self.player_list[0]
        self._turn.set(self._current_player._player_number)
        self._score.set('In Progress')
        self._letters.set(self._current_player.current_hand())


        ###SET UP GAMEBOARD AND GAME INFORMATION###
        self.root.title('Scrabble')
        greeter = Label(self.root,text = 'Welcome to scrabble!')
        greeter.grid(column=0,row=0,columnspan=2)

        #board
        self._game.set(value = self._gamestate.print_board())
        self.board_widget = Label(self.root,textvariable = self._game)
        self.board_widget.grid(column = 0,row = 1,sticky = S+W+E+N,columnspan=2)

        #game information
        self._create_move_handler().grid(column=0,row=2)
        self._create_game_information().grid(column = 1,row=2)

        #confirmation button
        #user either presses enter or clicks the button
        self.button = Button(self.root,text = 'Press to move',command = self.submit_move)
        self.button.grid(column=0,row=3)
        self.button.bind('<Return>',self.submit_move)

        #button to hand the turn over to another player
        self.turnover = Button(self.root,text = 'Press to hand turn over',command=self.turn_over)
        self.turnover.grid(column=1,row=3)


    def _create_move_handler(self):
        '''creates the move handler area, which contains entry for the movetype
        word and coordinates'''
        self.movehandler = Frame(self.root)
        
        #movetype
        self.move_label = Label(self.movehandler,text = 'Move Handler')
        self.move_label.grid(column = 0,row=0)
        self.vertical = Radiobutton(self.movehandler,text = 'Vertical',value='vertical',variable=self._movetype).grid(column=0,row=1,sticky = W)
        self.horizontal = Radiobutton(self.movehandler,text = 'Horizontal',value='horizontal',variable=self._movetype).grid(column=0,row=2,sticky = W)

        #wordentry
        self.wordentry = Frame(self.movehandler)
        self.word_label = Label(self.wordentry,text = 'Word')
        self.word_label.grid(column=0,row=0)
        self.entry = Entry(self.wordentry,textvariable = self._word)
        self.entry.grid(column=1,row=0)

        self.wordentry.grid(column=0,row=3)

        #coordinate buttons (packed into one Frame)
        self.spinboxes = Frame(self.movehandler)
        self.spinbox_label = Label(self.spinboxes,text = 'Coordinates')
        self.spinbox_label.grid(column=0,row=0)
        
        self.spinbox1 = Spinbox(self.spinboxes,from_=0,to=14,width=5)
        self.spinbox1.grid(column=1,row=0)
        self.spinbox2 = Spinbox(self.spinboxes,from_=0,to=14,width=5)
        self.spinbox2.grid(column=1,row=1)

        self.spinboxes.grid(column=0,row=4)

        return self.movehandler
    def _create_game_information(self):
        '''displays game information including:
              player turn,
              letters in hand,
              points for current player'''
        self.gameinfo = Frame(self.root)
        self.turnlabel = Label(self.gameinfo,text='Player turn:').grid(column=0,row=0)
        self.turnfield = Label(self.gameinfo,textvariable = self._turn).grid(column=1,row=0)

        self.letterlabel = Label(self.gameinfo,text= 'Current letters:').grid(column=0,row=1)
        self.letterfield = Label(self.gameinfo,textvariable = self._letters).grid(column=1,row=1)

        self.pointlabel = Label(self.gameinfo,text='Player Points:').grid(column=0,row=2)
        self.pointfield = Label(self.gameinfo,textvariable = self._score).grid(column=1,row=2)

        self.exchange_button = Button(self.gameinfo,text = 'Exchange Pieces',command = self.exchange_pieces)
        self.exchange_button.grid(column=0,row=3)
        self.exchange_pieces_entry = Entry(self.gameinfo,textvariable= self._exchange_pieces_var,width=10).grid(column=1,row=3)
        
        return self.gameinfo

y=gamestate(3)
z=GUI(y)
print(y._tiles._tile_count)
z.setup()
z.root.mainloop()
print(y._tiles._tile_count)
