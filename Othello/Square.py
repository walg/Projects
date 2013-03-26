'''Squares are background to the circles being drawn on them. They only register clicks
and make a move based on where that click is
'''
import coordinate
class Square:
    def __init__(self, tlc,brc,width,height,x,y):
        self.tlc = tlc
        self.brc = brc
        self.min_x,self.min_y = self.tlc.frac()
        self.max_x,self.max_y = self.brc.frac()

        #these are the width and height of the frame (in pixels)
        self.width = width
        self.height = height

        #these are the stored indices from creating the square. If a square
        #registers a click inside of it, it'll use the indices stored here
        self.x = x
        self.y = y

    def contains(self,x,y):
        '''returns true if the (x,y) position is inside the square'''
        return (self.min_x * self.width < x < self.max_x * self.width
                and self.min_y * self.height < y < self.max_y * self.height)

    def indices(self):
        '''when creating the class, the indices are stored, so they can be used when
           attempting to make a move'''
        return self.x,self.y
