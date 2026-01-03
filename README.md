# 🎮 Mancala AI Game

An intelligent implementation of the traditional African board game Mancala (Awalé) featuring an AI opponent powered by **Minimax algorithm with Alpha-Beta pruning**. Play in your terminal or through a web interface!


---


### Game Rules

- **Board Setup**: 12 pits (6 per player) + 2 stores, starting with 4 seeds per pit
- **Objective**: Capture more seeds than your opponent
- **Gameplay**: Pick up all seeds from a pit and distribute them counterclockwise, one per pit
- **Capture Rule**: Land in an empty pit on your side to capture opponent's seeds from the opposite pit
- **Replay Rule**: Land in your store to earn an extra turn
- **End Game**: Game ends when one side is empty; player with most seeds wins

---

## 🤖 AI Implementation

The computer opponent uses sophisticated adversarial search techniques:

- **Minimax Algorithm**: Explores the game tree to find optimal moves
- **Alpha-Beta Pruning**: Optimizes search by eliminating unnecessary branches
- **Heuristic Evaluation**: 
  - Standard: Score difference between players
  - Advanced: Considers score difference + mobility (seed distribution)
- **Configurable Depth**: Choose difficulty levels (depth 3, 6, 9, or custom)

---

## 🏗️ Project Structure

```
mancala-ai/
├── src/
│   ├── mancala_board.py    # Board state and game mechanics
│   ├── game.py              # Game logic and evaluation functions
│   └── ai_player.py         # Minimax AI implementation
├── main.py                  # Terminal-based game interface
├── server.py                # Flask API server for web interface
├── mancala_web.html         # Beautiful web-based UI
├── requirements.txt         # Python dependencies
├── README.md
└── .gitignore
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Flask (for web interface only)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd mancala-ai
   ```

2. **Install dependencies** (optional, for web interface)
   ```bash
   pip install flask flask-cors
   ```

---

## 🎯 How to Play

### Option 1: Terminal Interface

Run the game in your terminal with a text-based interface:

```bash
python main.py
```

**Features:**
- Human vs Computer mode (choose your side!)
- Computer vs Computer mode (watch AI battle with different heuristics)
- Configurable difficulty levels (Easy/Medium/Hard/Custom)
- Play multiple rounds with the same configuration
- Visual board representation in ASCII

### Option 2: Web Interface

Experience the game with a web interface:

1. **Start the Flask server:**
   ```bash
   python server.py
   ```

2. **Open the web interface:**
   - Simply open `mancala_web.html` in your web browser
   - The interface will automatically connect to the server at `http://localhost:5000`

**Features:**
- Animated seed distribution
- Real-time game state updates
- Pause/Resume functionality
- Interactive pit selection with hover effects
- Game over screen with statistics

---

## 🎮 Game Modes

### 1. Human vs Computer
- Choose to play as Player 1 (bottom) or Player 2 (top)
- Select difficulty level (search depth)
- Challenge the AI and test your strategy!

### 2. Computer vs Computer
- Watch two AI opponents battle it out
- Computer 1 uses standard heuristic (score difference)
- Computer 2 uses advanced heuristic (score + mobility)
- Perfect for learning optimal strategies

---

## 🛠️ Technical Details

### Core Components

**MancalaBoard** (`mancala_board.py`)
- Board state representation and management
- Move validation and execution
- Capture mechanics
- Game state queries

**Game** (`game.py`)
- Game flow control
- Win condition detection
- State evaluation (heuristic functions)
- Deep copying for AI simulation

**AI Player** (`ai_player.py`)
- Minimax algorithm implementation
- Alpha-Beta pruning optimization
- Move selection logic
- Two heuristic variants

**Flask Server** (`server.py`)
- RESTful API endpoints
- Game session management
- AI move computation
- State synchronization

### API Endpoints

- `POST /api/new-game` - Initialize a new game
- `POST /api/ai-move` - Compute and execute AI move
- `POST /api/human-move` - Process human player move
- `GET /api/game-state/<game_id>` - Retrieve current game state
- `DELETE /api/delete-game/<game_id>` - Clean up game session
- `GET /health` - Server health check

---

## 📊 Difficulty Levels

| Level | Search Depth | Characteristics |
|-------|--------------|-----------------|
| Easy | 3 | Quick decisions, beatable for beginners |
| Medium | 6 | Balanced challenge, looks several moves ahead |
| Hard | 9 | Strong opponent, plans many moves in advance |
| Custom | 1-15 | Choose your own depth for experimentation |

**Note**: Higher depth = stronger AI but slower computation time

---

## 🔧 Configuration

### Adjusting AI Behavior

Edit difficulty in `main.py` or web interface:
- Modify `depth` parameter (1-15)
- Higher depth = stronger but slower AI

### Customizing Heuristics

In `ai_player.py`, modify `_advanced_heuristic()`:
```python
# Weight factors
store_diff * 10      # Score difference (main factor)
mobility_diff * 0.5  # Seed distribution (secondary)
```

---

## 🐛 Troubleshooting

**Web interface won't connect:**
- Ensure Flask server is running (`python server.py`)
- Check console for connection errors
- Verify port 5000 is not blocked

**AI taking too long:**
- Reduce search depth
- Use Easy or Medium difficulty

**Game state desynchronization:**
- Refresh the page
- Restart the Flask server

---

**Enjoy playing Mancala! **
