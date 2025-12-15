from flask import Flask, jsonify, request
from flask_cors import CORS
from src.game import Game
from src.ai_player import Play
import copy

app = Flask(__name__)
CORS(app)  # Allow requests from browser

# Store active games (in production, use a database)
games = {}

def normalize_board(board):
    """Convert all board keys to strings for JSON serialization"""
    return {str(k): v for k, v in board.items()}

@app.route('/api/new-game', methods=['POST'])
def new_game():
    """Create a new game"""
    data = request.json
    game_id = data.get('gameId', 'default')
    mode = data.get('mode', 'human')  # 'human' or 'ai'
    depth = data.get('depth', 6)
    
    # Set up player sides based on mode
    if mode == 'human':
        player_side = {
            'HUMAN': 'player1',
            'COMPUTER': 'player2'
        }
    else:  # ai vs ai
        player_side = {
            'COMPUTER1': 'player1',
            'COMPUTER2': 'player2'
        }
    
    # Create game
    game = Game(playerSide=player_side)
    play = Play(game, depth=depth)
    
    # Store game
    games[game_id] = {
        'game': game,
        'play': play,
        'mode': mode,
        'depth': depth
    }
    
    # Return initial state with normalized board
    return jsonify({
        'success': True,
        'board': normalize_board(game.state.board),
        'currentPlayer': 'player1'
    })

@app.route('/api/ai-move', methods=['POST'])
def ai_move():
    """Get AI move using Minimax Alpha-Beta Pruning"""
    data = request.json
    game_id = data.get('gameId', 'default')
    current_player = data.get('currentPlayer', 'player1')
    heuristic_version = data.get('heuristicVersion', 1)
    
    if game_id not in games:
        return jsonify({'success': False, 'error': 'Game not found'}), 404
    
    game_data = games[game_id]
    game = game_data['game']
    play = game_data['play']
    mode = game_data['mode']
    
    # Determine player name based on mode and current player
    if mode == 'human':
        player_name = 'COMPUTER'
        player_side = game.playerSide['COMPUTER']
    else:  # ai vs ai
        if current_player == 'player1':
            player_name = 'COMPUTER1'
            player_side = game.playerSide['COMPUTER1']
        else:
            player_name = 'COMPUTER2'
            player_side = game.playerSide['COMPUTER2']
    
    # Check for possible moves
    possible_moves = game.state.possibleMoves(player_side)
    
    if not possible_moves:
        return jsonify({
            'success': False,
            'error': 'No possible moves',
            'gameOver': True
        })
    
    # Determine player type for minimax (1 for MAX, -1 for MIN)
    if player_name in ['COMPUTER', 'COMPUTER1']:
        player_type = 1  # MAX
    else:
        player_type = -1  # MIN
    
    # Use Minimax Alpha-Beta Pruning to find best move
    best_value, best_pit = play.MinimaxAlphaBetaPruning(
        game,
        player_type,
        game_data['depth'],
        float('-inf'),
        float('inf'),
        heuristic_version
    )
    
    # Execute the move
    game.state.doMove(player_side, best_pit)
    
    # Check if game is over
    game_over = game.gameOver()
    winner_info = None
    
    if game_over:
        winner, score = game.findWinner()
        winner_info = {
            'winner': winner,
            'score': score,
            'player1Score': game.state.get_store_count('player1'),
            'player2Score': game.state.get_store_count('player2')
        }
    
    return jsonify({
        'success': True,
        'move': best_pit,
        'value': best_value,
        'board': normalize_board(game.state.board),
        'gameOver': game_over,
        'winner': winner_info
    })

@app.route('/api/human-move', methods=['POST'])
def human_move():
    """Process human move"""
    data = request.json
    game_id = data.get('gameId', 'default')
    pit = data.get('pit')
    
    if game_id not in games:
        return jsonify({'success': False, 'error': 'Game not found'}), 404
    
    game_data = games[game_id]
    game = game_data['game']
    
    human_side = game.playerSide['HUMAN']
    
    # Validate move
    possible_moves = game.state.possibleMoves(human_side)
    
    if pit not in possible_moves:
        return jsonify({
            'success': False,
            'error': 'Invalid move'
        }), 400
    
    # Execute move
    game.state.doMove(human_side, pit)
    
    # Check if game is over
    game_over = game.gameOver()
    winner_info = None
    
    if game_over:
        winner, score = game.findWinner()
        winner_info = {
            'winner': winner,
            'score': score,
            'player1Score': game.state.get_store_count('player1'),
            'player2Score': game.state.get_store_count('player2')
        }
    
    return jsonify({
        'success': True,
        'board': normalize_board(game.state.board),
        'gameOver': game_over,
        'winner': winner_info
    })

@app.route('/api/game-state/<game_id>', methods=['GET'])
def get_game_state(game_id):
    """Get current game state"""
    if game_id not in games:
        return jsonify({'success': False, 'error': 'Game not found'}), 404
    
    game_data = games[game_id]
    game = game_data['game']
    
    return jsonify({
        'success': True,
        'board': normalize_board(game.state.board),
        'mode': game_data['mode'],
        'depth': game_data['depth']
    })

@app.route('/api/delete-game/<game_id>', methods=['DELETE'])
def delete_game(game_id):
    """Delete a game session"""
    if game_id in games:
        del games[game_id]
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'Game not found'}), 404

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'activeGames': len(games)
    })

if __name__ == '__main__':
    print("=" * 60)
    print("🎮 Mancala Flask Server Starting...")
    print("=" * 60)
    print("\n✅ Server will run at: http://localhost:5000")
    print("✅ Open mancala_web.html in your browser")
    print("✅ The web interface will connect to this server\n")
    print("=" * 60)
    print("Press CTRL+C to stop the server")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)