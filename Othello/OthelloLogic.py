'''
Get the number of rows and/or columns on the board.
Find out whose turn it is.
Determine whether the game is over.
Determine whether a disc is in some cell in the grid; if so, determine its color.
Make a move.'''


'''GIST OF THE GAME RULES: from wiki: Dark must place a piece with the dark side up on the
board, in such a position that there exists at least one straight
(horizontal, vertical, or diagonal) occupied line between the new piece and
another dark piece, with one or more contiguous light pieces between them.
and vice versa'''
class Gameboard:
    def __init__(self, board_rows,board_columns,starting_color,seed_color,win_type):
        self.board_rows = board_rows
        self.board_columns = board_columns
        
        #first move is either 'black' or 'white'
        self.current_color = starting_color
        #seed_color is the starting color to initialize the colors on board
        self.seed_color = seed_color
        #True wintype means play with opposite scoring
        self.win_type = win_type
        self.board = self.setup_board()

        self._black_score = 0
        self._white_score = 0
        
    def setup_board(self):
        '''performs setup of the board'''
        
        #used to check for the middle indices in columns and rows
        middle_column_checker = (self.board_columns / 2)-1
        middle_row_checker = (self.board_rows / 2) -1
        
        board = []
        for x in range(self.board_rows):
            row = []
            for y in range(self.board_columns):
                #initializes the square of alternating colors in the middle
                #the middle square always starts at half the board dimension length -1
                #   e.g. a board with board_columns = 12 will need to start the starting block
                #   at 12/2 -1 = 5
                if middle_column_checker == y and middle_row_checker == x:
                    row.append(self.seed_color)
                elif middle_column_checker + 1 == y and middle_row_checker == x:
                    row.append(self._opposite_seed_color())
                elif middle_column_checker == y and middle_row_checker + 1 == x:
                    row.append(self._opposite_seed_color())
                elif middle_column_checker + 1 == y  and middle_row_checker + 1  == x:
                    row.append(self.seed_color)
                else:
                    row.append('')
            
            board.append(row)
        return board
            
        
    def make_move(self,x,y):
        '''overarching method that submits a move
           -checks if move is valid by checking if the current color's piece bounds
           the opposite colors piece(s) (at least one straight vertical, horizontal or diagonal line)
           -'captures' all the necessary pieces
           - changes the current color to the opposite one
           '''
        if self.check_all(x,y) == False:
            return False
        
        self.flip_all_directions(x,y)
        self.board[y][x] = self.current_color
        self._change_turn()
        
    def print_board(self):
        '''Prints the board in a readable format.
           for console play only.
           The actual values of B and W are 'black' and 'white'''
        board_string = ''
        for x in range(self.board_columns+1):
            if x == 0:
                board_string += '   '
            elif x >= 10: #deals with the alignment of numbers with two digits for board dimensions greater than 10
                board_string += ' {}'.format(x-1)
            else:
                board_string += ' {} '.format(x-1)
        board_string+='\n'
        for y in range(self.board_rows):
            if y >= 10:
                board_string += '{} '.format(y)
            else:
                board_string += ' {} '.format(y)
            for x in range(self.board_columns):
                if self.board[y][x] =='':
                    board_string+=' . '
                elif self.board[y][x] == 'black':
                    board_string += ' B '
                elif self.board[y][x] == 'white':
                    board_string += ' W '
            board_string += '\n'

        return board_string

    
    def _change_color(self):
        '''changes the current color to the opposite color'''
        self.current_color = self._opposite_color()
    
    def _opposite_color(self):
        '''returns the opposite color from the current color'''
        if self.current_color == 'black':
            return 'white'
        elif self.current_color == 'white':
            return 'black'

    def _opposite_seed_color(self):
        '''returns the opposite color of current seed color'''
        if self.seed_color == 'black':
            return 'white'
        elif self.seed_color == 'white':
            return 'black'

    def _change_turn(self):
        '''performs necessary functions to change the turn
           -changes current color
           -tallies the score up'''
        self._change_color()
        self._tally_score()

        #if the changed turn ends up moving to the other player with no moves
        # then change color
        if self.check_all_valid_moves() == False:
            self._change_color()


    #### WINNER CHECK METHODS ####
    '''finds the winner and computes final score'''

    def find_winner(self):
        winner = ''
        
        # a True self.win_type means the player with the lower score wins
        if not self.game_over():
            return None
        else:
            if self.win_type == True: #Opposite Scoring
                if self._black_score > self._white_score:
                    winner = 'white'
                elif self._black_score < self._white_score:
                    winner = 'black'
                else:
                    winner = 'draw!'
            else: #Normal Scoring
                if self._black_score > self._white_score:
                    winner = 'black'
                elif self._black_score < self._white_score:
                    winner = 'white'
                else:
                    winner = 'draw!'
        return winner
    def game_over(self):
        '''if there is no valid move for either white or black, the game is over
           returns True if the game is over'''
        #temporarily changes color to opposite color then back to current color
        # to check for valid moves for both cases(no net change) 
        current_check = self.check_all_valid_moves()
        self._change_color()
        opposite_check = self.check_all_valid_moves()
        self._change_color()
        if not current_check and not opposite_check :
            result = True
        else:
            result = False
        return result
            

    def _tally_score(self):
        '''computes the score for black and white based on how many tiles are on the board
           '''
        white_score = 0
        black_score = 0
        for y in range(self.board_rows):
            for x in range(self.board_columns):
                if self.board[y][x] == 'black':
                    black_score += 1
                elif self.board[y][x] == 'white':
                    white_score +=1
        self._black_score = black_score
        self._white_score = white_score
        
    #### FLIPPER METHODS ####
    '''methods that deal with flipping captured pieces'''

    def flip_all_directions(self,x,y):
        '''main flip function that flips all captured pieces
           given coordinate of recently made move'''

        #_flip direction performs both a check for sandwich
        # and flips all pieces if it is a sandwich

        #verticals
        self._flip_direction(x,y,up = True) 
        self._flip_direction(x,y,down = True) 
        #diagonals
        self._flip_direction(x,y,up = True, left = True) 
        self._flip_direction(x,y,up = True, right = True) 
        self._flip_direction(x,y,down = True, left = True) 
        self._flip_direction(x,y,down = True, right = True) 
        #horizontals
        self._flip_direction(x,y,left = True)
        self._flip_direction(x,y,right = True)

                

    def _flip_direction(self,x,y,up=False,down=False,left=False,right=False):
        '''attempts to flip all pieces in a certain direction.
           if there's no valid sandwich in that direction, nothing happens

           flips all pieces to the current color until an empty space is hit'''
        checked = self._check_direction(x,y,up=up,down=down,left=left,right=right)
        if checked:
            space_check = None
            z=1
            while True:
                a = z if up else 0
                b = z if down else 0
                c = z if left else 0
                d = z if right else 0
                space_check = self._check_space(x,y,d-c,b-a)

                if space_check == self.current_color or space_check == '':
                    return

                self._flip_piece(x,y,d-c,b-a)

                z+=1
    def _flip_piece(self,x,y,x_delta,y_delta):
        '''flips one piece into current color at position (x_delta,y_delta) away from (x,y)'''
        try:
            y_place = y + y_delta
            x_place = x + x_delta
            #if either indices become negative, stop the check
            if x_place < 0 or y_place < 0:
                return 
            self.board[y_place][x_place] = self.current_color
        except:
            pass

        
    #### MOVE CHECKER METHODS ####
    '''methods that check to see if the desired move is valid or not'''

    
    def check_all_valid_moves(self):
        '''ensures that the new turn has a valid move on at least one place on the board
           -performs a check_all for every space
           -returns True if there is at least one space with a valid move, False otherwise'''
        for y in range(self.board_rows):
            for x in range(self.board_columns):
                if self.check_all(x,y) == True:
                    return True
        return False
    def check_all(self,x,y):
        '''performs all 3 checks
           1) empty check
           2) adjacent piece of opposite color check
           3) sandwich check
           if any one of them fails return false, otherwise return true'''
        if (not self._require_empty(x,y) or
            not self._require_opposite_adjacent_piece(x,y) or
            not self._check_sandwiches(x,y)):
            return False
        else:
            return True

    #CHECK 1 - EMPTY SPACE
    def _require_empty(self,x,y):
        '''checks to see if the current space is empty or not, returns false if
           not empty'''
        return True if self.board[y][x] == '' else False


    #CHECK 2 - ADJACENT PIECE OF OPPOSITE COLOR
    def _require_opposite_adjacent_piece(self,x,y):
        '''checks if at least 1 piece of the opposite color is next to it
           which must be true in order to make a valid move. by definition, also
           checks if the place pieced is not by itself

           if the checked adjacent square is an opposite piece, adds one to
           the counter. If not, keeps it zero. If the counter is zero after all
           checks (no adjacent pieces of the opposite color)returns false'''
        counter = 0
        
        counter += self._check_opposite_adjacent_piece(x-1,y-1)
        counter += self._check_opposite_adjacent_piece(x-1,y)
        counter += self._check_opposite_adjacent_piece(x-1,y+1)
        counter += self._check_opposite_adjacent_piece(x,y-1)
        counter += self._check_opposite_adjacent_piece(x,y+1)
        counter += self._check_opposite_adjacent_piece(x+1,y-1)
        counter += self._check_opposite_adjacent_piece(x+1,y)
        counter += self._check_opposite_adjacent_piece(x+1,y+1)


        return False if counter == 0 else True


    def _check_opposite_adjacent_piece(self,x,y):
        '''checks one adjacent piece for the opposite color.
           if the move is on the edge of the board, ignores checks that would
           be outside the board'''
        try:
            if x < 0 or y < 0 :
                return 0
            current_space = self.board[y][x]
            if current_space == self._opposite_color():
                return 1
            else:
                return 0
        except:
            return 0


    #CHECK 3 - SANDWICHES
    def _check_sandwiches(self,x,y):
        '''final check if the move to be placed sandwiches a
           piece of the opposite color on any side diagonally, horizontally
           or vertically

           Checks all 8 directions. If at least one is valid, let move proceed
           If none work, dont let the move proceed'''

        if (#verticals
            self._check_direction(x,y,up = True) or
            self._check_direction(x,y,down = True) or
            #diagonals
            self._check_direction(x,y,up = True, left = True) or
            self._check_direction(x,y,up = True, right = True) or
            self._check_direction(x,y,down = True, left = True) or
            self._check_direction(x,y,down = True, right = True) or
            #horizontals
            self._check_direction(x,y,left = True) or
            self._check_direction(x,y,right = True)):
            return True
        else:
            return False
    def _check_direction(self,x,y,up=False,down=False,left=False,right=False):
        ''' checks if the space is sandwiched in a certain direction (up or down and/or left or right)

            -assigns temporary variable to up, down, left, right as a,b,c,d respectively
            that are added or subtracted to either the x-deltas or y-deltas 
            -a and b are for change in vertical. a is negative for up, b is positive for down (the y-scale is inverted)
             c and d are for change in horizontal. d is positive for right, c is negative for left
            -a,b,c,d all scale with z or stay at zero
            '''
        sandwiched=False
        check=''
        z=1
        
        while check!= None:
            '''broken when _check_space returns none (the end of the board, no sandwich found)
               or a sandwich is found'''
            a = z if up else 0
            b = z if down else 0
            c = z if left else 0
            d = z if right else 0
            check = self._check_space(x,y,d-c,b-a)
            if check == self._opposite_color():
                sandwiched = True
            if check == '':
                return False
            if check == self.current_color and not sandwiched:
                return False
            elif check == self.current_color and sandwiched:
                return True
            z+=1
        return False
    def _check_space(self,x,y,x_delta,y_delta):
        '''retrieves the information (black,white, or empty) on a certain space at (x,y) and (x_delta,y_delta) away from (x,y)'''
        try:
            y_place = y + y_delta
            x_place = x + x_delta
            #if either indices become negative (which means they would loop back
            #to the other side of the row/column), automatically return None
            if x_place < 0 or y_place < 0:
                return None
            return self.board[y_place][x_place]
        except:
            #reached the end of the board (IndexError)
            return None

      
