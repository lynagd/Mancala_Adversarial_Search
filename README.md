Mancala AI with Minimax Alpha-Beta Pruning
An intelligent Mancala (Awalé) game implementation featuring an AI opponent powered by the Minimax algorithm with Alpha-Beta pruning optimization.
📋 About
This project implements the traditional African board game Mancala (also known as Awalé) with an AI opponent. The computer player uses adversarial search techniques to make strategic decisions, providing a challenging gameplay experience.
🎮 Game Overview
Mancala is a sowing game played on a board with:

12 small pits (6 per player)
2 stores (one per player)
4 seeds in each pit at the start

Objective: Capture more seeds than your opponent by strategically sowing seeds around the board.
🤖 AI Implementation
The computer opponent uses:

Minimax Algorithm: For optimal decision-making in adversarial scenarios
Alpha-Beta Pruning: To optimize search efficiency by eliminating unnecessary branches
Heuristic Evaluation: Based on seed count difference between computer and human stores

🏗️ Project Structure
mancala-ai/
├── src/
│   ├── mancala_board.py    # Board state representation
│   ├── game.py              # Game logic and evaluation
│   └── play.py              # Game controller and AI
├── README.md
├── requirements.txt
└── .gitignore
🛠️ Technologies

Python 3.8+
Object-oriented design
Adversarial search algorithms
Game theory concepts

📖 How to Play

Choose your side (Player 1 or Player 2)
On your turn, select a pit (A-F for Player 1, G-L for Player 2)
Seeds are distributed counterclockwise
Capture opponent's seeds by landing in an empty pit
Game ends when one player's pits are empty
Player with most seeds in their store wins

🎓 Academic Context
This project is part of the Problem Solving course for Master 1 Visual Computing at USTHB (2025/2026).
📝 Features

 Complete Mancala game rules implementation
 AI opponent with configurable difficulty (search depth)
 Minimax algorithm with Alpha-Beta pruning
 Human vs Computer gameplay
 GUI interface 

Instructor: Dr. Meriem SEBAI
Academic Year: 2025/2026
