import copy
from game import Game

class Play:
    def __init__(self, game, depth=6):
        """
        Initialize the Play class.
        
        Args:
            game: Instance of Game class
            depth: Maximum depth for Minimax search (default: 6)
        """
        self.game = game
        self.depth = depth
    
    def humanTurn(self):
        """
        Allow the human player to take their turn.
        Returns True if the player gets another turn (last seed in store).
        """
        print("\n" + "="*50)
        print("HUMAN'S TURN")
        print("="*50)
        print(self.game.state)
        
        # Get human player side
        human_side = self.game.playerSide['HUMAN']
        
        # Get possible moves
        possible_moves = self.game.state.possibleMoves(human_side)
        
        if not possible_moves:
            print("No possible moves! Skipping turn...")
            return False
        
        print(f"Possible moves: {possible_moves}")
        
        # Get valid input from human
        while True:
            try:
                pit = input("Choose a pit to play: ").upper().strip()
                
                if pit not in possible_moves:
                    print(f"Invalid move! Choose from: {possible_moves}")
                    continue
                
                break
            except Exception as e:
                print(f"Error: {e}. Please try again.")
        
        # Execute the move and check if last seed lands in store
        replay = self._execute_move_with_replay_check(human_side, pit)
        
        print(f"\nYou played pit {pit}")
        print(self.game.state)
        
        if replay:
            print("\n🎉 Last seed landed in your store! You get another turn!")
            return True
        
        return False
    
    def computerTurn(self, computer_name='COMPUTER', heuristic_version=1):
        """
        Allow the computer to take its turn using Minimax Alpha-Beta Pruning.
        
        Args:
            computer_name: 'COMPUTER' or 'COMPUTER2'
            heuristic_version: 1 for standard heuristic, 2 for advanced heuristic
        
        Returns True if the computer gets another turn (last seed in store).
        """
        print("\n" + "="*50)
        print(f"{computer_name}'S TURN")
        print("="*50)
        print(self.game.state)
        
        # Get computer player side
        computer_side = self.game.playerSide[computer_name]
        
        # Get possible moves
        possible_moves = self.game.state.possibleMoves(computer_side)
        
        if not possible_moves:
            print("No possible moves! Skipping turn...")
            return False
        
        print(f"Thinking... (depth={self.depth})")
        
        # Determine MAX or MIN based on computer name
        if computer_name == 'COMPUTER':
            player_type = 1  # MAX
        else:
            player_type = -1  # MIN
        
        # Use Minimax to find best move
        best_value, best_pit = self.MinimaxAlphaBetaPruning(
            self.game, 
            player_type, 
            self.depth, 
            float('-inf'), 
            float('inf'),
            heuristic_version
        )
        
        print(f"{computer_name} chooses pit {best_pit} (value: {best_value})")
        
        # Execute the move and check if last seed lands in store
        replay = self._execute_move_with_replay_check(computer_side, best_pit)
        
        print(self.game.state)
        
        if replay:
            print(f"\n🎉 {computer_name} gets another turn!")
            return True
        
        return False
    
    def _execute_move_with_replay_check(self, player, pit):
        """
        Execute a move and check if the last seed lands in the player's store.
        
        Args:
            player: 'player1' or 'player2'
            pit: The pit to play from
        
        Returns:
            True if last seed lands in player's store (replay), False otherwise
        """
        # Determine player's store
        my_store = 1 if player == 'player1' else 2
        opponent_store = 2 if player == 'player1' else 1
        
        # Get number of seeds
        seeds = self.game.state.board[pit]
        
        # Simulate the move to find where last seed lands
        current_position = pit
        remaining_seeds = seeds
        
        while remaining_seeds > 0:
            current_position = self.game.state.next_pit[current_position]
            
            # Skip opponent's store
            if current_position == opponent_store:
                current_position = self.game.state.next_pit[current_position]
            
            remaining_seeds -= 1
        
        # Check if last position is player's store
        lands_in_store = (current_position == my_store)
        
        # Now execute the actual move
        self.game.state.doMove(player, pit)
        
        return lands_in_store
    
    def MinimaxAlphaBetaPruning(self, game, player, depth, alpha, beta, heuristic_version=1):
        """
        Minimax algorithm with Alpha-Beta Pruning.
        
        Args:
            game: Current game state
            player: 1 (MAX) or -1 (MIN)
            depth: Remaining depth to search
            alpha: Alpha value for pruning
            beta: Beta value for pruning
            heuristic_version: 1 for standard, 2 for advanced heuristic
        
        Returns:
            (best_value, best_pit) tuple
        """
        # Terminal condition: game over or depth limit reached
        if game.gameOver() or depth == 0:
            if heuristic_version == 1:
                best_value = game.evaluate()
            else:
                best_value = self._advanced_heuristic(game)
            return best_value, None
        
        # Determine which player side to use
        if player == 1:  # MAX
            player_key = 'COMPUTER' if 'COMPUTER' in game.playerSide else 'MAX'
        else:  # MIN
            if 'HUMAN' in game.playerSide:
                player_key = 'HUMAN'
            elif 'COMPUTER2' in game.playerSide:
                player_key = 'COMPUTER2'
            else:
                player_key = 'MIN'
        
        player_side = game.playerSide[player_key]
        possible_moves = game.state.possibleMoves(player_side)
        
        # No possible moves
        if not possible_moves:
            if heuristic_version == 1:
                best_value = game.evaluate()
            else:
                best_value = self._advanced_heuristic(game)
            return best_value, None
        
        best_pit = possible_moves[0]  # Default
        
        if player == 1:  # MAX player
            best_value = float('-inf')
            
            for pit in possible_moves:
                # Create a copy of the game
                child_game = game.copy()
                
                # Execute the move
                child_game.state.doMove(player_side, pit)
                
                # Recursive call
                value, _ = self.MinimaxAlphaBetaPruning(
                    child_game, 
                    -player, 
                    depth - 1, 
                    alpha, 
                    beta,
                    heuristic_version
                )
                
                # Update best value
                if value > best_value:
                    best_value = value
                    best_pit = pit
                
                # Alpha-Beta pruning
                if best_value >= beta:
                    break
                
                if best_value > alpha:
                    alpha = best_value
        
        else:  # MIN player
            best_value = float('inf')
            
            for pit in possible_moves:
                # Create a copy of the game
                child_game = game.copy()
                
                # Execute the move
                child_game.state.doMove(player_side, pit)
                
                # Recursive call
                value, _ = self.MinimaxAlphaBetaPruning(
                    child_game, 
                    -player, 
                    depth - 1, 
                    alpha, 
                    beta,
                    heuristic_version
                )
                
                # Update best value
                if value < best_value:
                    best_value = value
                    best_pit = pit
                
                # Alpha-Beta pruning
                if best_value <= alpha:
                    break
                
                if best_value < beta:
                    beta = best_value
        
        return best_value, best_pit
    
    def _advanced_heuristic(self, game):
        """
        Advanced heuristic for COMPUTER2.
        Takes into account not just the score difference, but also:
        - Number of seeds on player's side (mobility)
        - Strategic pit positions
        
        Args:
            game: Current game state
        
        Returns:
            Heuristic value
        """
        # Determine players
        if 'COMPUTER' in game.playerSide and 'COMPUTER2' in game.playerSide:
            computer_player = game.playerSide['COMPUTER']
            opponent_player = game.playerSide['COMPUTER2']
        elif 'COMPUTER' in game.playerSide and 'HUMAN' in game.playerSide:
            computer_player = game.playerSide['COMPUTER']
            opponent_player = game.playerSide['HUMAN']
        else:
            return game.evaluate()
        
        # Store difference (main factor)
        store_diff = game.state.get_store_count(computer_player) - game.state.get_store_count(opponent_player)
        
        # Count seeds on each side (mobility advantage)
        computer_pits = game.state.player1_pits if computer_player == 'player1' else game.state.player2_pits
        opponent_pits = game.state.player1_pits if opponent_player == 'player1' else game.state.player2_pits
        
        computer_seeds = sum(game.state.board[pit] for pit in computer_pits)
        opponent_seeds = sum(game.state.board[pit] for pit in opponent_pits)
        
        mobility_diff = computer_seeds - opponent_seeds
        
        # Weighted combination
        return store_diff * 10 + mobility_diff * 0.5
