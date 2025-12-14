from src.game import Game
from src.ai_player import Play


def display_menu():
    #Display the main menu.
    print("\n" + "="*60)
    print(" "*15 + "MANCALA GAME")
    print("="*60)
    print("\nChoose game mode:")
    print("1. Human vs Computer")
    print("2. Computer vs Computer")
    print("3. Exit")
    print("="*60)


def choose_side():
    #Let user choose side: Player 1 or Player 2.
    print("\n" + "="*60)
    print("Choose your side:")
    print("1. Player 1 (bottom side: A-F)")
    print("2. Player 2 (top side: G-L)")
    print("="*60)
    
    while True:
        choice = input("Enter your choice (1 or 2): ").strip()
        if choice == '1':
            return 'player1'
        elif choice == '2':
            return 'player2'
        else:
            print("Invalid choice! Please enter 1 or 2.")


def choose_depth():
    """Let user choose search depth."""
    print("\n" + "="*60)
    print("Choose difficulty (search depth):")
    print("1. Easy (depth = 3)")
    print("2. Medium (depth = 6)")
    print("3. Hard (depth = 9)")
    print("4. Custom")
    print("="*60)
    
    while True:
        choice = input("Enter your choice (1-4): ").strip()
        if choice == '1':
            return 3
        elif choice == '2':
            return 6
        elif choice == '3':
            return 9
        elif choice == '4':
            while True:
                try:
                    depth = int(input("Enter custom depth (1-15): "))
                    if 1 <= depth <= 15:
                        return depth
                    else:
                        print("Depth must be between 1 and 15!")
                except ValueError:
                    print("Invalid input! Please enter a number.")
        else:
            print("Invalid choice! Please enter 1-4.")


def human_vs_computer():
    print("\n" + "="*60)
    print(" "*10 + "HUMAN VS COMPUTER MODE")
    print("="*60)
    
    # Let human choose side
    human_side = choose_side()
    computer_side = 'player2' if human_side == 'player1' else 'player1'
    
    print(f"\nYou are: {human_side}")
    print(f"Computer is: {computer_side}")
    
    # Choose difficulty
    depth = choose_depth()
    
    # Initialize game
    game = Game(playerSide={
        'HUMAN': human_side,
        'COMPUTER': computer_side
    })
    
    play = Play(game, depth=depth)
    
    # Determine who starts
    current_player = 'HUMAN' if human_side == 'player1' else 'COMPUTER'
    
    print("\n" + "="*60)
    print("GAME START!")
    print(f"{current_player} plays first!")
    print("="*60)
    print("\nInitial board:")
    print(game.state)
    
    # Game loop
    while not game.gameOver():
        if current_player == 'HUMAN':
            # Human's turn (with replay rule)
            replay = True
            while replay and not game.gameOver():
                replay = play.humanTurn()
                if replay and not game.gameOver():
                    print("\n→ You get another turn!")
            
            if not game.gameOver():
                current_player = 'COMPUTER'
        else:
            # Computer's turn (with replay rule)
            replay = True
            while replay and not game.gameOver():
                replay = play.computerTurn('COMPUTER')
                if replay and not game.gameOver():
                    print("\n→ Computer gets another turn!")
                    input("Press Enter to see computer's next move...")
            
            if not game.gameOver():
                current_player = 'HUMAN'
    
    # Game over
    print("\n" + "="*60)
    print(" "*20 + "GAME OVER!")
    print("="*60)
    print("\nFinal board:")
    print(game.state)
    
    winner, score = game.findWinner()
    
    print("\n" + "="*60)
    if winner == 'TIE':
        print(f" "*20 + "IT'S A TIE!")
        print(f" "*15 + f"Both players: {score} seeds")
    else:
        # Determine winner name for display
        if winner == 'HUMAN':
            winner_name = 'HUMAN'
            loser_name = 'COMPUTER'
            loser_side = computer_side
        else:
            winner_name = 'COMPUTER'
            loser_name = 'HUMAN'
            loser_side = human_side
        
        loser_score = game.state.get_store_count(loser_side)
        
        print(f" "*15 + f"🏆 {winner_name} WINS! 🏆")
        print(f" "*10 + f"{winner_name}: {score} seeds")
        print(f" "*10 + f"{loser_name}: {loser_score} seeds")
    print("="*60)


def computer_vs_computer():
    #Computer vs Computer mode with two different heuristics.
    print("\n" + "="*60)
    print(" "*10 + "COMPUTER VS COMPUTER MODE")
    print("="*60)
    print("\nCOMPUTER 1 (Player 1) - Standard heuristic")
    print("COMPUTER 2 (Player 2) - Advanced heuristic")
    
    # Choose depth
    print("\nChoose search depth for both computers:")
    depth = choose_depth()
    
    # Initialize game
    game = Game(playerSide={
        'COMPUTER1': 'player1',
        'COMPUTER2': 'player2'
    })
    
    play = Play(game, depth=depth)
    
    print("\n" + "="*60)
    print("GAME START!")
    print("COMPUTER 1 plays first!")
    print("="*60)
    print("\nInitial board:")
    print(game.state)
    
    input("\nPress Enter to start the game...")
    
    # Game loop
    current_computer = 'COMPUTER1'
    move_count = 0
    
    while not game.gameOver():
        move_count += 1
        print(f"\n--- Move #{move_count} ---")
        
        if current_computer == 'COMPUTER1':
            # Computer 1's turn with standard heuristic
            replay = True
            while replay and not game.gameOver():
                replay = play.computerTurn('COMPUTER1', heuristic_version=1)
                if replay and not game.gameOver():
                    print("\n→ COMPUTER 1 gets another turn!")
                    input("Press Enter to continue...")
            
            if not game.gameOver():
                current_computer = 'COMPUTER2'
        else:
            # Computer 2's turn with advanced heuristic
            replay = True
            while replay and not game.gameOver():
                replay = play.computerTurn('COMPUTER2', heuristic_version=2)
                if replay and not game.gameOver():
                    print("\n→ COMPUTER 2 gets another turn!")
                    input("Press Enter to continue...")
            
            if not game.gameOver():
                current_computer = 'COMPUTER1'
        
        if not game.gameOver():
            input("\nPress Enter for next move...")
    
    # Game over
    print("\n" + "="*60)
    print(" "*20 + "GAME OVER!")
    print("="*60)
    print("\nFinal board:")
    print(game.state)
    
    winner, score = game.findWinner()
    
    print("\n" + "="*60)
    if winner == 'TIE':
        print(f" "*20 + "IT'S A TIE!")
        print(f" "*15 + f"Both computers: {score} seeds")
    else:
        winner_name = 'COMPUTER 1' if winner == 'COMPUTER1' else 'COMPUTER 2'
        loser_name = 'COMPUTER 2' if winner == 'COMPUTER1' else 'COMPUTER 1'
        loser_side = 'player2' if winner == 'COMPUTER1' else 'player1'
        loser_score = game.state.get_store_count(loser_side)
        
        print(f" "*15 + f"🏆 {winner_name} WINS! 🏆")
        print(f" "*10 + f"{winner_name}: {score} seeds")
        print(f" "*10 + f"{loser_name}: {loser_score} seeds")
    print("="*60)
    
    print(f"\nTotal moves: {move_count}")


def main():
    print("\n" + "="*60)
    print(" "*5 + "WELCOME TO MANCALA - ADVERSARIAL SEARCH")
    print("="*60)
    
    while True:
        display_menu()
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            human_vs_computer()
            
            # Ask if player wants to play again
            play_again = input("\nPlay again? (y/n): ").strip().lower()
            if play_again != 'y':
                break
        
        elif choice == '2':
            computer_vs_computer()
            
            # Ask if user wants to simulate again
            simulate_again = input("\nSimulate another game? (y/n): ").strip().lower()
            if simulate_again != 'y':
                break
        
        elif choice == '3':
            print("\n" + "="*60)
            print(" "*15 + "Thanks for playing!")
            print(" "*10 + "Goodbye! 👋")
            print("="*60)
            break
        
        else:
            print("\n❌ Invalid choice! Please enter 1, 2, or 3.")
    
    print()


if __name__ == "__main__":
    main()