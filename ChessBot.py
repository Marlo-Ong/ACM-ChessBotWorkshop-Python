import chess as ch # AKA python-chess
import random

class Bot:
    # Properties:
        # - Board 
        #   - (class object imported from python-chess; not defined by us)
        #   - legal_moves: property of Board
        # - color (b/w)
        # - max_depth (higher depth = bigger brain, slower computing time)

    # Methods:
        # public:
        #   - getBestMove() (called by Main.py)
        #       - calls recursive search
        #       - returns Move with best evaluation
        # private: 
        #   - search(Move candidate, int depth, float alpha, float beta)
        #   - evaluate()

    def __init__(self, Board, max_depth, color):
        self.Board = Board
        self.color = color
        self.max_depth = max_depth # depth = ply
        self.pieceValues = {
            ch.PAWN : 1,
            ch.ROOK : 5.1,
            ch.BISHOP : 3.33,
            ch.KNIGHT : 3.2,
            ch.QUEEN : 8.8,
            ch.KING : 10_000
            } # based on Hans Berliner System
    
    def getBestMove(self):
        best_move, best_value = self.search(depth = 1, alpha = float("-inf"), beta = float("inf")) # self is passed automatically
        print(best_move, best_value)
        return best_move

    def evaluate(self):
        score = 0

        # Iterate through entire board, sum up piece values of each square
        for i in range(64):
            score += self.eval_square_value(ch.SQUARES[i])

        # Misc. score improvements - ADD MORE LOGIC HERE
        score += (
              self.eval_mate_opportunity()
            + self.eval_opening()
            + (0.001 * random.random()) # ensure bot doesn't play exact same moves in each scenario - less predictable
        )
        return score

    def eval_mate_opportunity(self):
        ### Stalemate or checkmate is worst outcome ###

        if (self.Board.legal_moves.count() == 0):
            return float("-inf") if (self.Board.turn == self.color) else float("inf")
        return 0

    def eval_opening(self):
        # Prioritize the bot developing the opening

        if (self.Board.fullmove_number < 10):
            if (self.Board.turn == self.color):
                return 1/30 * self.Board.legal_moves.count()
            return -1/30 * self.Board.legal_moves.count()
        return 0

    def eval_square_value(self, square):
        # Takes a square as input and returns
        # the corresponding Hans Berliner's
        # system value of the piece atop it

        piece_type = self.Board.piece_type_at(square)
        if piece_type:
            pieceValue = self.pieceValues[piece_type]
            ishumanColor = self.Board.color_at(square) == self.color
            return pieceValue if ishumanColor else -pieceValue
        return 0
            
    # Recursive search function
    def search(self, depth, alpha, beta):
        
        # Reached max depth of search or no possible moves
        if (depth == self.max_depth or self.Board.legal_moves.count() == 0):
            return None, self.evaluate()

        # - Bot plays every odd turn (odd depth)
        # - When bot plays, it wants to maximize its score
        # - When it's human's turn, it wants to minize their score
        is_maximizing = (depth % 2 != 0)

        if is_maximizing:
            best_value = float("-inf") 
            best_move = None
            
            for move in self.Board.legal_moves:
                self.Board.push(move)
                _, value_candidate = self.search(depth + 1, alpha, beta)
        
                if value_candidate > best_value:
                    best_move = move
                    best_value = value_candidate

                if best_value > beta:
                    self.Board.pop()
                    break
                alpha = max(alpha, best_value)
                self.Board.pop()

            return best_move, best_value

        elif not is_maximizing:
            best_value = float("inf")
            best_move = None

            for move in self.Board.legal_moves:
                self.Board.push(move)
                _, value_candidate = self.search(depth + 1, alpha, beta)

                if value_candidate < best_value:
                    best_move = move
                    best_value = value_candidate

                if best_value < alpha:
                    self.Board.pop()
                    break
                beta = min(beta, best_value)
                self.Board.pop()

            return best_move, best_value