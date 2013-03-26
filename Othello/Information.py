###supplementary gui class that reads in information for creation of gameboard###
import Project4
import tkinter

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
        
        self._root.destroy()

