'''This module creates a class gameboard that initializes the gameboard and
handles all changes to it as the game progresses'''
import random
score_table = {'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1,
        'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8,
        'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1,
        'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1,
        'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10,}

'''initialized to number of starting tiles, changed as game progresses to keep count of
what's drawn'''
tile_count = {'a': 9, 'b': 2, 'c': 2, 'd': 4, 'e': 12,
              'f': 2, 'g': 3, 'h': 2, 'i': 9, 'j': 1,
              'k': 1, 'l': 4, 'm': 2, 'n': 6, 'o': 8,
              'p': 2, 'q': 1, 'r': 6, 's': 4, 't': 6,
              'u': 4, 'v': 2, 'w': 2, 'x': 1, 'y': 2, 'z': 1}
class Tiles:
    '''this class handles the tally of tiles in the bag, as well as drawing and
       exchanging of tiles'''
    def __init__(self):
        self._tile_count = tile_count
        self._score_table = score_table
    def tile_count(self):
        return self._tile_count

    # 2 POSSIBLE MOVES: NORMAL MOVE OR EXCHANGE PIECES
    def draw_piece(self):
        '''draws a piece from existing tile_count state, returns that letter
        '''
        choice = self._make_choice()
        self._pop_value(choice)
        return choice
    def exchange_pieces(self,discarded_pieces):
        '''exchances x number of pieces, returns them as a list to be added to
           players hand
           discarded_pieces in form 'abcd' (ordered right after the other, 1 string)
           '''
        result = []
        if len(self._listout()) < 7:
            # cannot exchange pieces if there are fewer than 7 left in play
            raise
        for x in range(len(discarded_pieces)):
            result.append(self._make_choice())

        #puts back pieces only after *all* new pieces are drawn
            
        for letter in discarded_pieces:
            self._add_value(letter)
        return result
        
    
    def _listout(self):
        '''takes the number associated with a letter and lists it out that many times
        e.g: 'a': 4 and 'b': 2= [a,a,a,a,b,b] so it can be used in a random choice'''
        result = []
        for entry in self._tile_count:
            number = self._tile_count[entry]
            for x in range(number):
                result.append(entry)
        return result
    def _pop_value(self,value):
        '''subtracts 1 from its value after choice is made'''
        self._tile_count[value] -= 1
    def _add_value(self,value):
        '''adds 1 to value when putting pieces back after exchange'''
        self._tile_count[value] += 1
    def _make_choice(self):
        '''makes a random choice from list generated in listout()'''
        while True:
            choice = random.choice(self._listout())
            if self._tile_count[choice] > 0:
                return choice
