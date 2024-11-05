import chess
import chess.engine

def evaluate_board(board):
    piece_values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0
    }
    
    score = 0
    for piece_type in piece_values:
        # calculating sum values for white pieces
        score += len(board.pieces(piece_type, chess.WHITE)) * piece_values[piece_type]
        # calculating sum values for black pieces
        score -= len(board.pieces(piece_type, chess.BLACK)) * piece_values[piece_type]
    
    return score

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
                break  # Beta
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
                break  # Alpha
        return min_eval

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
def get_user_move(board):
    while True:
        try:
            user_input = input("Enter your move (e.g., e2e4): ")
            move = chess.Move.from_uci(user_input)
            
            if move in board.legal_moves:
                board.push(move)
                break
            else:
                print("Invalid move. Try again.")
        
        except ValueError:
            print("Invalid format.")

def play_chess():
    board = chess.Board()
    depth = 3
    print(type(board))

    while not board.is_game_over():
        print(board)
        if board.turn == chess.WHITE:
            print()
            print("Your turn: ")
            get_user_move(board)
        else:
            print()
            print("Agent's turn: ", end='')
            move = select_best_move(board, depth)
            board.push(move)
            print(move)

    print("\nGame Over:", board.result())

play_chess()
