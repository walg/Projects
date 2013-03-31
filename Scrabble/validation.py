'''This module validates that the most recent move creates all possible valid words'''


vertical_scanned_list = []
    
def _read_dictionary():
    '''readlines a dictionary into _dictionary'''
    with open('dictionary.txt','r') as dictionary:
        list_of_words = dictionary.readlines()
        #takes off newline characters from each word in the list
        for x in range(len(list_of_words)):
            list_of_words[x] = list_of_words[x].strip('\n')
    return list_of_words


dictionary = _read_dictionary()

def _check_space(x,y,board):
    '''returns the letter (or empty) in the current space'''
    try:
        return board[y][x]
    except:
        return False
def _check_horizontal(x,y,board):
    '''checks horizontally until an empty space or the end of the board is reached'''
    word = ''
    for z in range(15):
        try:
            if _check_space(x+z,y,board) == None or _check_space(x+z,y,board) == False:
                break
            word += _check_space(x+z,y,board)
        except:
            break
    return word

def _check_vertical(x,y,board):
    '''checks vertically until an empty space or the end of the board is reached'''
    word = ''
    global vertical_scanned_list
    for z in range(15):
        try:
            if _check_space(x,y+z,board) == None or _check_space(x,y+z,board) == False:
                break
            word += _check_space(x,y+z,board)
            vertical_scanned_list.append((x,y+z))
        except:
            break
    return word

def execute(board):
    '''function that checks if all words on the board are valid words, including
       incidental words'''
    check = None
    last_check = None
    global vertical_scanned_list
    #to stop vertical words from being scanned multiple times
    #(ex.: 'real' being scanned 4 times (real,eal,al,l))
    #make a list of all the coordinates where a vertical word is detected
    #if a vertical word is detected but that (x,y) coordinate is in the scanned
    #list, ignore it and continue
    for y in range(15):
        for x in range(15):
            print(vertical_scanned_list)
            last_check,check = check,_check_space(x,y,board)
            if last_check == None and check != None and _check_space(x+1,y,board) != None: #checks previous and current space
                if _check_horizontal(x,y,board) not in dictionary:
                    return False
            if _check_space(x,y+1,board) != None and check != None: #checks current space and one space below
                if _check_vertical(x,y,board) not in dictionary and (x,y) not in vertical_scanned_list:
                    return False
    vertical_scanned_list = []
    return True
    
    

