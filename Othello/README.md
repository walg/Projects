Othello
Othello made using Tkinter

This is the 5th of 5 projects in ICS 32 during winter quarter. The class is taught by Professor Alex Thornton and is
located at the University of California, Irvine.

Othello is played starting with a square of alternating colors initialized on the middle of the board. The first player
-black or white- tries to capture the opponents pieces by placing their own piece so that they sandwich the opponents' 
vertically, horizontally or diagonally. For example, on one row on the board is BWWW (B & W representing the pieces 
that are placed). It is black's turn, so theyplace a piece to the right of that sequence making BWWWB. Since the black
pieces sandwich the three white pieces, black captures all 3 of those, making them flip into BBBBB. The game is played
until there are no more possible flips on each side or the game board is filled.

The project itself, when run from the OthelloGUI.py module, initializes a frame that reads in 5 information fields:
-The board length: must be an even integer between 4 and 16 -The board width: must be an even integer between 4 and 16
-The starting color: which player moves first
-The seed color: which color starts the square of colors in the middle of the board at the start 
-The scoring type: normal scoring, in which the player with the most points wins, or opposite scoring, 
                   in which the player with the fewest points wins.
