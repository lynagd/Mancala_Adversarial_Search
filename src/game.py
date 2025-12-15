import copy
from .mancala_board import MancalaBoard
class Game:
    
    def __init__(self, playerSide=None):
       
        self.state = MancalaBoard()
        
        # Default configuration (for testing/development only)
        # main.py will provide the actual configuration
        if playerSide is None:
            self.playerSide = {
                'COMPUTER': 'player1',
                'HUMAN': 'player2'
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
       # Determine the winner of the game.
        
        score1 = self.state.get_store_count('player1')
        score2 = self.state.get_store_count('player2')
        
        if score1 > score2:
            winner_side = 'player1'
            winner_score = score1
        elif score2 > score1:
            winner_side = 'player2'
            winner_score = score2
        else:
            return 'TIE', score1
        
        # Find who owns the winning side
        for player_name, side in self.playerSide.items():
            if side == winner_side:
                return player_name, winner_score
        
        # Should never reach here
        return 'UNKNOWN', winner_score
    
    def evaluate(self):
    #Evaluate the current game state from the perspective of the maximizing player.

    # Determine the maximizing player
    # The maximizing player is always the one doing the thinking (the AI)
    
        if 'COMPUTER' in self.playerSide and 'HUMAN' in self.playerSide:
         # Human vs Computer mode
         maximizing_player = self.playerSide['COMPUTER']
         minimizing_player = self.playerSide['HUMAN']
        elif 'COMPUTER1' in self.playerSide and 'COMPUTER2' in self.playerSide:
         # Computer vs Computer mode
         # COMPUTER1 is designated as the maximizing player
         maximizing_player = self.playerSide['COMPUTER1']
         minimizing_player = self.playerSide['COMPUTER2']
    
        elif 'COMPUTER' in self.playerSide and 'COMPUTER2' in self.playerSide:
         # Alternative Computer vs Computer mode (COMPUTER vs COMPUTER2)
         maximizing_player = self.playerSide['COMPUTER']
         minimizing_player = self.playerSide['COMPUTER2']
        
        else:
         # Fallback - should not happen in normal gameplay
         # If playerSide only has player1 and player2, use those
         maximizing_player = 'player1'
         minimizing_player = 'player2'
    
        max_seeds = self.state.get_store_count(maximizing_player)
        min_seeds = self.state.get_store_count(minimizing_player)
    
        return max_seeds - min_seeds
    
    def copy(self):
       # Create a deep copy of the game state for simulation purposes.
        new_game = Game(self.playerSide.copy())
        new_game.state = self.state.copy()
        return new_game
    
    def reset(self):
        # Reset the game state for a new round.
        self.state.reset()


# Testing
if __name__ == "__main__":
    print("="*50)
    print("Testing Game Class")
    print("="*50)
    
    # Test 1: Human vs Computer (Human goes first)
    print("\n1. Testing Human vs Computer (Human as player1)...")
    game = Game(playerSide={'HUMAN': 'player1', 'COMPUTER': 'player2'})
    assert game.playerSide['HUMAN'] == 'player1'
    assert game.playerSide['COMPUTER'] == 'player2'
    print("✓ Human vs Computer setup works!")
    
    # Test 2: Human vs Computer (Computer goes first)
    print("\n2. Testing Human vs Computer (Computer as player1)...")
    game = Game(playerSide={'COMPUTER': 'player1', 'HUMAN': 'player2'})
    game.state.board[1] = 30  # Computer's store
    game.state.board[2] = 20  # Human's store
    eval_score = game.evaluate()
    assert eval_score == 10, f"Computer should be ahead by 10, got {eval_score}"
    print("✓ Evaluation works correctly!")
    
    # Test 3: Computer vs Computer
    print("\n3. Testing Computer vs Computer mode...")
    game = Game(playerSide={'COMPUTER1': 'player1', 'COMPUTER2': 'player2'})
    assert game.playerSide['COMPUTER1'] == 'player1'
    assert game.playerSide['COMPUTER2'] == 'player2'
    
    game.state.board[1] = 25  # COMPUTER1
    game.state.board[2] = 20  # COMPUTER2
    eval_score = game.evaluate()
    assert eval_score == 5, f"COMPUTER1 should be ahead by 5, got {eval_score}"
    print("✓ Computer vs Computer works!")
    
    # Test 4: Find Winner (Human wins)
    print("\n4. Testing findWinner (Human wins)...")
    game = Game(playerSide={'HUMAN': 'player1', 'COMPUTER': 'player2'})
    game.state.board[1] = 30  # Human's store
    game.state.board[2] = 18  # Computer's store
    winner, score = game.findWinner()
    assert winner == 'HUMAN', f"Winner should be HUMAN, got {winner}"
    assert score == 30
    print("✓ Human can win!")
    
    # Test 5: Find Winner (Computer wins)
    print("\n5. Testing findWinner (Computer wins)...")
    game = Game(playerSide={'HUMAN': 'player1', 'COMPUTER': 'player2'})
    game.state.board[1] = 18  # Human's store
    game.state.board[2] = 30  # Computer's store
    winner, score = game.findWinner()
    assert winner == 'COMPUTER', f"Winner should be COMPUTER, got {winner}"
    assert score == 30
    print("✓ Computer can win!")
    
    # Test 6: Find Winner (Computer vs Computer)
    print("\n6. Testing findWinner (Computer1 wins)...")
    game = Game(playerSide={'COMPUTER1': 'player1', 'COMPUTER2': 'player2'})
    game.state.board[1] = 30
    game.state.board[2] = 18
    winner, score = game.findWinner()
    assert winner == 'COMPUTER1'
    print("✓ Computer vs Computer winner detection works!")
    
    # Test 7: Game Over
    print("\n7. Testing gameOver...")
    game = Game()
    assert not game.gameOver(), "Game should not be over at start"
    
    # Empty player1's side
    for pit in game.state.player1_pits:
        game.state.board[pit] = 0
    assert game.gameOver(), "Game should be over when side is empty"
    print("✓ gameOver works!")
    
    # Test 8: Reset for new round
    print("\n8. Testing reset (play another round)...")
    game = Game(playerSide={'HUMAN': 'player1', 'COMPUTER': 'player2'})
    game.state.board['A'] = 10
    game.state.board[1] = 20
    game.state.board[2] = 15
    
    # Reset for new round - playerSide stays the same
    game.reset()
    
    assert game.state.board['A'] == 4, "Pits should reset to 4"
    assert game.state.board[1] == 0, "Stores should reset to 0"
    assert game.state.board[2] == 0, "Stores should reset to 0"
    assert game.playerSide['HUMAN'] == 'player1', "playerSide should stay the same"
    print("✓ Reset for new round works!")
    
    # Test 9: Copy
    print("\n9. Testing copy (for AI simulation)...")
    game1 = Game(playerSide={'HUMAN': 'player1', 'COMPUTER': 'player2'})
    game2 = game1.copy()
    game2.state.board['A'] = 10
    assert game1.state.board['A'] == 4, "Original should not change"
    assert game2.playerSide == game1.playerSide, "playerSide should be copied"
    print("✓ Copy works!")
    
    print("\n" + "="*50)
    print("All tests passed! ✓")
    print("="*50)
    print("\nKey points:")
    print("- Human vs Computer: Can choose who goes first")
    print("- Computer vs Computer: Both sides use AI")
    print("- Reset: Allows playing multiple rounds")
    print("- playerSide: Set by main.py based on user choice")