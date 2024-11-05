import chess
import chess.engine

# Evaluation Function for Scoring the Board
def evaluate_board(board):
    piece_values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0  # King's value is high, but we typically avoid assigning it.
    }
    
    # Initialize the score
    score = 0
    for piece_type in piece_values:
        # Sum values for white pieces
        score += len(board.pieces(piece_type, chess.WHITE)) * piece_values[piece_type]
        # Subtract values for black pieces
        score -= len(board.pieces(piece_type, chess.BLACK)) * piece_values[piece_type]
    
    return score

# Minimax with Alpha-Beta Pruning
def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)
    
    if maximizing_player:
        max_eval = -float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Beta cut-off
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Alpha cut-off
        return min_eval

# Choosing the Best Move
def select_best_move(board, depth):
    best_move = None
    best_value = -float('inf') if board.turn == chess.WHITE else float('inf')
    
    for move in board.legal_moves:
        board.push(move)
        board_value = minimax(board, depth - 1, -float('inf'), float('inf'), not board.turn)
        board.pop()
        
        if board.turn == chess.WHITE:
            if board_value > best_value:
                best_value = board_value
                best_move = move
        else:
            if board_value < best_value:
                best_value = board_value
                best_move = move
    
    return best_move

def play_chess():
    board = chess.Board()
    depth = 3

    while not board.is_game_over():
        if board.turn == chess.WHITE:
            print("\nWhite's turn")
            # White makes the best move using Minimax
            move = select_best_move(board, depth)
        else:
            print("\nBlack's turn")
            # Black also uses Minimax
            move = select_best_move(board, depth)

        board.push(move)
        print(board)

    print("\nGame Over:", board.result())

play_chess()
