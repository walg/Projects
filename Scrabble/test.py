import validation
import gameboard

game = gameboard.gamestate(3)
game.make_move(0,0,'abbey','horizontal')
game.make_move(5,5,'real','horizontal')
game.make_move(8,5,'real','vertical')
valid_checker = validation.execute(game._board)
print(game.print_board())
print(valid_checker)
