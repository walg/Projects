'''Each player is represented by a player class'''

class Player:
    def __init__(self,tiles,player_number):
        self._tiles = tiles
        self._current_hand = self._draw_initial_pieces()
        self._player_number = player_number

    def _draw_initial_pieces(self):
        '''creates the initial hand'''
        hand = []
        for x in range(7):
            hand.append(self._tiles.draw_piece())
        return hand

    def current_hand(self):
        string = ''
        for item in self._current_hand:
            string += item
        return string

    def exchange_pieces(self,word):
        '''given a word that is played, takes those pieces out of play and
           gets new pieces'''
        pieces = list(word)
        for item in pieces:
            self._current_hand.remove(item)
            self._current_hand.append(self._tiles.draw_piece())
            
    
    
'''
x = Player(tiles.Tiles())
print(x._current_hand)
print(x._tiles.tile_count())
print(x.current_hand())
'''
