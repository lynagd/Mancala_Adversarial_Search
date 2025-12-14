import copy
from mancala_board import MancalaBoard

class Game:
    
    def __init__(self, playerSide=None):
     
        self.state = MancalaBoard()
        
        # Default: MAX is player1, MIN is player2
        if playerSide is None:
            self.playerSide = {
                'MAX': 'player1',
                'MIN': 'player2'
            }
        else:
            self.playerSide = playerSide
    
    def gameOver(self):
        #Check if the game has ended (one player's side is empty).
        #If game is over, collect all remaining seeds.
   
        # Check if player1's side is empty
        if self.state.is_side_empty('player1'):
            # Collect remaining seeds for player2
            self.state.collect_remaining_seeds('player2')
            return True
        
        # Check if player2's side is empty
        if self.state.is_side_empty('player2'):
            # Collect remaining seeds for player1
            self.state.collect_remaining_seeds('player1')
            return True
        
        return False
    
    def findWinner(self):
        #Determine the winner of the game.
 
        score1 = self.state.get_store_count('player1')
        score2 = self.state.get_store_count('player2')
        
        if score1 > score2:
            return 'player1', score1
        elif score2 > score1:
            return 'player2', score2
        else:
            return 'TIE', score1
    
    def evaluate(self):
        # Two modes supported:
        #1. Human vs Computer
        #2. Computer vs Computer
        
        if 'COMPUTER' in self.playerSide and 'HUMAN' in self.playerSide:
            # Human vs Computer mode
            computer_player = self.playerSide['COMPUTER']
            opponent_player = self.playerSide['HUMAN']
        elif 'COMPUTER' in self.playerSide and 'COMPUTER2' in self.playerSide:
            # Computer vs Computer mode
            # COMPUTER (player1) is MAX, COMPUTER2 (player2) is MIN
            computer_player = self.playerSide['COMPUTER']
            opponent_player = self.playerSide['COMPUTER2']
        else:
            raise ValueError("Invalid playerSide configuration. Must have either COMPUTER/HUMAN or COMPUTER/COMPUTER2")
        
        computer_seeds = self.state.get_store_count(computer_player)
        opponent_seeds = self.state.get_store_count(opponent_player)
        
        return computer_seeds - opponent_seeds
    
    def copy(self):
        #Create a deep copy of the game state.
 
        new_game = Game(self.playerSide.copy())
        new_game.state = self.state.copy()
        return new_game
    
    def reset(self):
        #Reset the game to initial state for a new round.
        #Keeps the same player assignments but resets the board.
    
        self.state.reset()
                  # Returns deep copy