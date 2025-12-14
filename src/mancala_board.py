import copy
class MancalaBoard:
    def __init__(self):
        #Initialize the board with starting configuration

        # Board dictionary: keys are pit letters and store numbers
        self.board = {
            # Player 1's pits (A-F)
            'A': 4, 'B': 4, 'C': 4, 'D': 4, 'E': 4, 'F': 4,
            # Player 2's pits (G-L)
            'G': 4, 'H': 4, 'I': 4, 'J': 4, 'K': 4, 'L': 4,
            # Stores
            1: 0,  # Player 1's store
            2: 0   # Player 2's store
        }
        
        # Player pit assignments
        self.player1_pits = ('A', 'B', 'C', 'D', 'E', 'F')
        self.player2_pits = ('G', 'H', 'I', 'J', 'K', 'L')
        
        # Opposite pits for capturing
        self.opposite_pit = {
            'A': 'L', 'B': 'K', 'C': 'J', 'D': 'I', 'E': 'H', 'F': 'G',
            'G': 'F', 'H': 'E', 'I': 'D', 'J': 'C', 'K': 'B', 'L': 'A'
        }
        
        # Next position in counterclockwise order
        self.next_pit = {
            'A': 'B', 'B': 'C', 'C': 'D', 'D': 'E', 'E': 'F', 'F': 1,
            1: 'G', 'G': 'H', 'H': 'I', 'I': 'J', 'J': 'K', 'K': 'L',
            'L': 2, 2: 'A'
        }
    
    def possibleMoves(self, player):
       #get list of possible moves for a player

        # Select the correct pits based on player
        pits = self.player1_pits if player == 'player1' else self.player2_pits
        
        # Return only pits that have seeds
        possible = [pit for pit in pits if self.board[pit] > 0]
        
        return possible
    
    def doMove(self, player, pit):
        #Execute a move: pick up seeds from pit and distribute counterclockwise.
        
        #Rules:
        #1. Pick up all seeds from the chosen pit
        #2. Distribute one seed per pit going counterclockwise
        #3. Include your own store, skip opponent's store
        #4. If last seed lands in empty pit on your side, capture!

        # Validation
        if pit not in self.board:
            raise ValueError(f"Invalid pit: {pit}")
        
        if self.board[pit] == 0:
            raise ValueError(f"Pit {pit} is empty")
        
        # Determine player's and opponent's stores
        if player == 'player1':
            my_store = 1
            opponent_store = 2
            my_pits = self.player1_pits
        else:
            my_store = 2
            opponent_store = 1
            my_pits = self.player2_pits
        
        # Step 1: Pick up all seeds from chosen pit
        seeds = self.board[pit]
        self.board[pit] = 0
        
        # Step 2: Distribute seeds counterclockwise
        current_position = pit
        
        while seeds > 0:
            # Move to next position
            current_position = self.next_pit[current_position]
            
            # Skip opponent's store
            if current_position == opponent_store:
                current_position = self.next_pit[current_position]
            
            # Drop one seed
            self.board[current_position] += 1
            seeds -= 1
        
        # Step 3: Check for capture
        # Capture conditions:
        # - Last seed landed in a pit (not a store)
        # - That pit is on my side
        # - That pit now has exactly 1 seed (was empty before)
        # - Opposite pit has seeds
        
        if (current_position in my_pits and 
            self.board[current_position] == 1):
            
            opposite = self.opposite_pit[current_position]
            
            if self.board[opposite] > 0:
                # CAPTURE!
                captured_seeds = self.board[current_position] + self.board[opposite]
                
                # Add to player's store
                self.board[my_store] += captured_seeds
                
                # Clear both pits
                self.board[current_position] = 0
                self.board[opposite] = 0
    
    def copy(self):
        #create deep copy to simulate moves without effecting the original board
        return copy.deepcopy(self)
    
    def reset(self):
        #reset to start a new round

        # Reset all pits to 4 seeds
        for pit in self.player1_pits + self.player2_pits:
            self.board[pit] = 4
        
        # Reset stores to 0
        self.board[1] = 0
        self.board[2] = 0
    
    def get_store_count(self, player):
        #get the number of seeds in a player's store

        store = 1 if player == 'player1' else 2
        return self.board[store]
    
    def is_side_empty(self, player):
        #check if all pits on a player's side are empty to end the game
        pits = self.player1_pits if player == 'player1' else self.player2_pits
        return all(self.board[pit] == 0 for pit in pits)
    
    def collect_remaining_seeds(self, player):
        #collect all remaining seeds from a player's side into their store at game end
        pits = self.player1_pits if player == 'player1' else self.player2_pits
        store = 1 if player == 'player1' else 2
        
        total = 0
        for pit in pits:
            total += self.board[pit]
            self.board[pit] = 0
        
        self.board[store] += total
        return total
    
    def __str__(self):
        #string representation of the board
        result = "\n"
        result += "          Player 2\n"
        result += "      L   K   J   I   H   G\n"
        result += f"   [{self.board[2]:2}]"
        
        for pit in ['L', 'K', 'J', 'I', 'H', 'G']:
            result += f" {self.board[pit]:2} "
        
        result += f" [{self.board[1]:2}]\n"
        result += "     "
        
        for pit in ['A', 'B', 'C', 'D', 'E', 'F']:
            result += f" {self.board[pit]:2} "
        
        result += "\n"
        result += "      A   B   C   D   E   F\n"
        result += "          Player 1\n"
        
        return result


# Testing functions
def test_board():
    # Basic tests for MancalaBoard functionality
    print("="*50)
    print("Testing MancalaBoard")
    print("="*50)
    
    # Test 1: Initialization
    print("\n1. Testing initialization...")
    board = MancalaBoard()
    print(board)
    assert board.board['A'] == 4, "Pit A should have 4 seeds"
    assert board.board[1] == 0, "Store 1 should be empty"
    print(" Initialization works!")
    
    # Test 2: Possible moves
    print("\n2. Testing possibleMoves...")
    moves = board.possibleMoves('player1')
    print(f"Player 1 possible moves: {moves}")
    assert len(moves) == 6, "Should have 6 possible moves"
    assert 'A' in moves, "A should be in possible moves"
    print(" possibleMoves works!")
    
    # Test 3: Basic move
    print("\n3. Testing basic move (A)...")
    board.doMove('player1', 'A')
    print(board)
    assert board.board['A'] == 0, "Pit A should be empty"
    assert board.board['B'] == 5, "Pit B should have 5 seeds"
    assert board.board['C'] == 5, "Pit C should have 5 seeds"
    assert board.board['D'] == 5, "Pit D should have 5 seeds"
    assert board.board['E'] == 5, "Pit E should have 5 seeds"
    print(" Basic move works!")
    
    # Test 4: Move reaching store
    print("\n4. Testing move reaching store (F)...")
    board.reset()
    board.doMove('player1', 'F')
    print(board)
    assert board.board['F'] == 0, "Pit F should be empty"
    assert board.board[1] == 1, "Store 1 should have 1 seed"
    print(" Move reaching store works!")
    
    # Test 5: Capture
    print("\n5. Testing capture...")
    board.reset()
    # Set up a capture scenario
    board.board['C'] = 0  # Empty pit C
    board.board['A'] = 2  # Move from A should land in C
    board.board['J'] = 3  # Opposite pit has seeds
    print("Before capture:")
    print(board)
    board.doMove('player1', 'A')
    print("After capture:")
    print(board)
    assert board.board['C'] == 0, "Pit C should be empty after capture"
    assert board.board['J'] == 0, "Opposite pit J should be empty"
    assert board.board[1] >= 4, "Store should have captured seeds"
    print(" Capture works!")
    
    # Test 6: Copy
    print("\n6. Testing copy...")
    board1 = MancalaBoard()
    board2 = board1.copy()
    board2.board['A'] = 10
    assert board1.board['A'] == 4, "Original should not change"
    assert board2.board['A'] == 10, "Copy should change"
    print(" Copy works!")
    
    # Test 7: Empty side check
    print("\n7. Testing is_side_empty...")
    board = MancalaBoard()
    assert not board.is_side_empty('player1'), "Side should not be empty"
    for pit in board.player1_pits:
        board.board[pit] = 0
    assert board.is_side_empty('player1'), "Side should be empty"
    print(" is_side_empty works!")
    
    print("\n" + "="*50)
    print("All tests passed! ✓")
    print("="*50)


if __name__ == "__main__":
    # Run tests
    test_board()
    
    # Interactive test
    print("\n\nInteractive Board Test:")
    print("Creating a new board...")
    board = MancalaBoard()
    print(board)
    
    print("\nTry a few moves:")
    print("Move from A:")
    board.doMove('player1', 'A')
    print(board)
    
    print("\nMove from G:")
    board.doMove('player2', 'G')
    print(board)