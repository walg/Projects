import tkinter
import OthelloLogic
import coordinate
import Square

class Information:
    def __init__(self):
        self._root = tkinter.Tk()

        #everything related to initializing the gameboard, such as reading in
        #user input about the board dimensions or the starting color will be put
        #in one frame.
        #Modified by self._setup_data_fields()
        self._data_fields = tkinter.Frame(master = self._root)

        #Variables for tkinter use
        self._starting_color = tkinter.StringVar()
        self._seed_color = tkinter.StringVar()
        self._win_type = tkinter.BooleanVar()
        
    def start(self):
        '''start the application'''
        self.setup()
        self._root.mainloop()

    ###INITIALIZATION FUNCTIONS###
    '''These functions deal with reading in information to create the gamestate
       and initializing the gameboard'''
    def setup(self):
        '''initializes all widgets in the application frame'''
        self._root.title('Othello')
        self._setup_data_fields().grid(row=0,column=0,sticky = tkinter.W + tkinter.E + tkinter.S + tkinter.N)
        self._root.rowconfigure(0,weight=1)
        self._root.columnconfigure(0,weight=1)

    def _setup_data_fields(self):
        '''sets up the frame used to read in data when creating the gameboard class
           -board size
           -starting color
           -'seed' color
           -wintype'''
        self.greeting = tkinter.Label(master=self._data_fields,
             text = 'Welcome to Othello! Please input required data,\nthen press \'Generate\' to starting playing!')
        self.greeting.grid(row=0,column=0)
        self._dimensions_setup().grid(row=1,column=0)
        self._color_setup().grid(row=1,column=1)
        self._win_type_setup().grid(row=2,column=0)

        self._data_fields.rowconfigure(0,weight=2)
        self._data_fields.rowconfigure(1,weight=2)
        self._data_fields.rowconfigure(2,weight=2)
        self._data_fields.columnconfigure(0,weight=2)
        self._data_fields.columnconfigure(1,weight=2)


        self._generate_button = tkinter.Button(master = self._data_fields,text = 'Generate',command = self.execute)
        self._generate_button.grid(row=2,column=1)

        return self._data_fields
                            
    def _dimensions_setup(self):
        '''sets up the data entry fields for board dimensions'''
        self._dimensions = tkinter.Frame(master = self._data_fields)
        self._dimensions_label = tkinter.Label(master=self._dimensions,
             text = 'Board Dimensions')
        self._dimensions_label.grid(row=0,column=0)
        
        #ROWS
        self._row_label = tkinter.Label(master = self._dimensions,
             text = 'Rows:')
        self._row_label.grid(row=1,column=0)
        self._row_spinbox = tkinter.Spinbox(master = self._dimensions,
             increment = 2, from_ = 4, to = 16, width = 5)
        self._row_spinbox.grid(row=1,column=1)

        #COLUMNS
        self._column_label = tkinter.Label(master = self._dimensions,
             text = 'Columns:')
        self._column_label.grid(row=2,column=0)
        self._column_spinbox = tkinter.Spinbox(master = self._dimensions,
             increment = 2, from_ = 4, to = 16, width = 5)
        self._column_spinbox.grid(row=2,column=1)

        return self._dimensions

    def _color_setup(self):
        '''sets up data entry fields for both the starting color and seed color'''
        self._color_frame = tkinter.Frame(master = self._data_fields)

        #Starting Color
        self._starting_color_label = tkinter.Label(master = self._color_frame,
            text = 'Starting Color:')
        self._starting_color_label.grid(row=0,column=0)
        self._starting_black_button = tkinter.Radiobutton(master = self._color_frame,text = 'Black',value='black',variable=self._starting_color).grid(row=0,column=1)
        self._starting_white_button = tkinter.Radiobutton(master = self._color_frame,text = 'White',value='white',variable=self._starting_color).grid(row=1,column=1)

        #Seed Color
        self._seed_color_label = tkinter.Label(master = self._color_frame,
            text = 'Seed Color:')
        self._seed_color_label.grid(row=2,column=0)
        self._seed_black_button = tkinter.Radiobutton(master = self._color_frame,text = 'Black',value='black',variable=self._seed_color).grid(row=2,column=1)
        self._seed_white_button = tkinter.Radiobutton(master = self._color_frame,text = 'White',value='white',variable=self._seed_color).grid(row=3,column=1)

        return self._color_frame

    def _win_type_setup(self):
        '''sets up data entry field for the wintype'''
        self._win_type_frame = tkinter.Frame(master = self._data_fields)

        self._win_type_label = tkinter.Label(master = self._win_type_frame,
            text = 'Opposite Scoring?\n(The player with fewer points wins)')
        self._win_type_label.grid(row=0,column=0)

        self._win_type_check = tkinter.Checkbutton(self._win_type_frame, state=tkinter.ACTIVE, variable = self._win_type)
        self._win_type_check.grid(row=0,column=1)
        return self._win_type_frame

    def execute(self):
        '''feeds all the information into class variables after pressing the button'''

        self.rows = int(self._row_spinbox.get())
        self.columns = int(self._column_spinbox.get())
        self.starting_color = self._starting_color.get()
        self.seed_color = self._seed_color.get()
        self.win_type = self._win_type.get()
        
        if self.validate():
            self._root.destroy()


    def validate(self):
        '''checks if user has completed all gameboard information accurately
        returns true if: -rows and columns are even numbers between 4 and 16
                         -starting_color, seed_color, and win_type all have some value '''
        row_check = 4 <= self.rows <= 16 and self.rows % 2 == 0
        column_check = 4 <= self.columns <= 16 and self.columns % 2 == 0
        true_false_checks = not (self.starting_color == ''
                             or self.seed_color == '')
        return row_check and column_check and true_false_checks
class GUI:
    def __init__(self):
        #creates an empty list of all the squares to be added later
        self.square_list = []
        
    def start(self):
        self._read_information()
        self.create_gameboard().grid(
            row=0,column=0,padx=10,pady=10,
            sticky=tkinter.W + tkinter.S + tkinter.N + tkinter.E)

        self.create_game_information().grid(
            row=1,column=0,
            sticky=tkinter.W + tkinter.S + tkinter.N + tkinter.E)
        self._root.mainloop()
        

    def draw_board(self):
        '''draws the board on the canvas'''
        self._canvas.delete(tkinter.ALL)
        self.square_list = []

        #updates the game information window
        self._white_score.set(self.gamestate._white_score)
        self._black_score.set(self.gamestate._black_score)
        self._current_color.set(self.gamestate.current_color)
        
        for y in range(self.gamestate.board_rows):
            for x in range(self.gamestate.board_columns):
                #Find fractional coordinates for drawing one square/circle
                min_x = x / self.gamestate.board_columns
                min_y = y / self.gamestate.board_rows
                max_x = (x+1) / self.gamestate.board_columns
                max_y = (y+1) / self.gamestate.board_rows

                #create coordinate objects
                tlc = coordinate.from_frac(min_x,min_y)
                brc = coordinate.from_frac(max_x,max_y)

                #find current canvas dimensions                
                width = self._canvas.winfo_width()
                height = self._canvas.winfo_height()

                #find the absolute coordinates given current canvas dimensions
                #and coordinate objects of top-left corner and bottom-right corner
                tlc_x,tlc_y = tlc.absolute(width,height)
                brc_x,brc_y = brc.absolute(width,height)

                #determines the color of the circle
                color = '#68daae'
                if self.gamestate.board[y][x] == 'black':
                    color = 'black'
                elif self.gamestate.board[y][x] == 'white':
                    color = 'white'

                
                #creates a Square object to register click positions
                #creates an oval and rectangle to draw the piece and lines, respectively
                self.square_list.append(Square.Square(tlc,brc,width,height,x,y))
                self._canvas.create_rectangle(tlc_x,tlc_y,brc_x,brc_y,fill = '#ff6b62')
                self._canvas.create_oval(tlc_x,tlc_y,brc_x,brc_y,fill = color)

        #after drawing the board, checks if the game is over

        if self.gamestate.game_over():
            self._winner.set(self.gamestate.find_winner())

        

    def _on_resize(self,event):
        '''execute when the canvas is resized'''
        self.draw_board()

    def _on_button_click(self,event):
        '''-find the x,y coordinate of the click
           -register which square (and corresponding circle) was clicked
           -attempt to make a move there
           -if a successful move is made, redraw the board'''

        x = event.x
        y = event.y
        for square in self.square_list:
            if square.contains(x,y):
                move = self.gamestate.make_move(square.x,square.y)
                if move != False:
                    #updates the black and white scores after each successful move
                    self.draw_board()
                    
        

    ###WINDOW CREATION METHODS###

    def _read_information(self):
        '''reads in the information to create the gamestate from the information
           module'''
        self._info = Information()
        self._info.start()

        self._rows = self._info.rows
        self._columns = self._info.columns
        self._starting_color = self._info.starting_color
        self._seed_color = self._info.seed_color
        self._win_type = self._info.win_type

        self.gamestate = OthelloLogic.Gameboard(self._rows,self._columns,
                                            self._starting_color, self._seed_color,
                                            self._win_type)
                      
    def create_gameboard(self):
        '''creates the new root window and canvas on which the game will be
           played'''
        self._root = tkinter.Tk()
        self._root.title('Othello')

        #creates and initializes the variables needed to update the labels for black_score,white_score and the winner
        self._black_score = tkinter.IntVar()
        self._white_score = tkinter.IntVar()
        self._winner = tkinter.StringVar()
        self._current_color = tkinter.StringVar()
        
        self._white_score.set(self.gamestate._white_score)
        self._black_score.set(self.gamestate._black_score)
        self._current_color.set(self.gamestate.current_color)
        
        self._canvas = tkinter.Canvas(master= self._root,
            width = 500,height = 500)

        self._root.rowconfigure(0, weight = 10)
        self._root.rowconfigure(1, weight=1,minsize = 40)
        self._root.columnconfigure(0, weight = 1)

        self._canvas.bind('<Configure>',self._on_resize)
        self._canvas.bind('<Button-1>',self._on_button_click)

        return self._canvas
    
    def create_game_information(self):
        '''creates the game information Frame that contains the scores for
           both players as well as the current turn and winner
           '''
        #white score
        self.game_info = tkinter.Frame(master = self._root)
        self.white_label = tkinter.Label(
            master = self.game_info, text = 'white:')
        self.white_label.grid(row=0,column=0)

        self.white_score_label = tkinter.Label(
            master = self.game_info,textvariable = self._white_score)
        self.white_score_label.grid(row=0,column=1)

        #black score
        self.black_label = tkinter.Label(
            master = self.game_info, text = 'black:')
        self.black_label.grid(row=1,column=0)

        self.black_score_label = tkinter.Label(
            master = self.game_info,textvariable = self._black_score)
        self.black_score_label.grid(row=1,column=1)

        #current turn
        self.turn_text_label = tkinter.Label(
            master = self.game_info, text = 'Current turn:')
        self.turn_text_label.grid(row=0,column=2)

        self.turn_label = tkinter.Label(
            master = self.game_info,textvariable = self._current_color)
        self.turn_label.grid(row=0,column=3)

        #winner
        self.winner_text_label = tkinter.Label(
            master = self.game_info,text = 'winner:')
        self.winner_text_label.grid(row=1,column=2)
        self.winner_label = tkinter.Label(
            master = self.game_info,textvariable = self._winner)
        self.winner_label.grid(row=1,column=3)

        return self.game_info

if __name__ == '__main__':
    game = GUI()
    game.start()
