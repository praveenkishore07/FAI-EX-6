import time

class TicTacToe:
    def __init__(self):
        self.board = [['.' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
    
    def print_board(self):
        for i in range(3):
            print(' | '.join(self.board[i]))
            if i < 2:
                print('---------')
    
    def get_available_moves(self):
        moves = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '.':
                    moves.append((i, j))
        return moves
    
    def make_move(self, move, player):
        i, j = move
        if self.board[i][j] == '.':
            self.board[i][j] = player
            return True
        return False
    
    def undo_move(self, move):
        i, j = move
        self.board[i][j] = '.'
    
    def check_winner(self, player):
     
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)):
                return True
        
      
        for j in range(3):
            if all(self.board[i][j] == player for i in range(3)):
                return True
        
      
        if all(self.board[i][i] == player for i in range(3)):
            return True
        if all(self.board[i][2-i] == player for i in range(3)):
            return True
        
        return False
    
    def is_board_full(self):
        return all(self.board[i][j] != '.' for i in range(3) for j in range(3))
    
    def game_over(self):
        return self.check_winner('X') or self.check_winner('O') or self.is_board_full()

class MinimaxAI:
    def __init__(self, player):
        self.player = player
        self.opponent = 'O' if player == 'X' else 'X'
    
    def evaluate(self, game):
        if game.check_winner(self.player):
            return 10
        elif game.check_winner(self.opponent):
            return -10
        else:
            return 0
    
    def minimax(self, game, depth, is_maximizing):
        if game.check_winner(self.player):
            return 10 - depth
        if game.check_winner(self.opponent):
            return depth - 10
        if game.is_board_full():
            return 0
        
        if is_maximizing:
            best_score = float('-inf')
            for move in game.get_available_moves():
                game.make_move(move, self.player)
                score = self.minimax(game, depth + 1, False)
                game.undo_move(move)
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for move in game.get_available_moves():
                game.make_move(move, self.opponent)
                score = self.minimax(game, depth + 1, True)
                game.undo_move(move)
                best_score = min(score, best_score)
            return best_score
    
    def get_best_move(self, game):
        best_score = float('-inf')
        best_move = None
        
        available_moves = game.get_available_moves()
        if not available_moves:
            return None
        
        for move in available_moves:
            game.make_move(move, self.player)
            score = self.minimax(game, 0, False)
            game.undo_move(move)
            
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move

def main():
    game = TicTacToe()
    ai = MinimaxAI('X')
    
    print("Initial board:")
    game.print_board()
    print()
    
    while not game.game_over():
        if game.current_player == 'X':
            start_time = time.time()
            move = ai.get_best_move(game)
            end_time = time.time()
            
            print(f"Evaluation time: {end_time - start_time:.7f}s")
            print(f"Recommended move: X = {move[0]}, Y = {move[1]}")
            
            x = int(input("Insert the X coordinate: "))
            y = int(input("Insert the Y coordinate: "))
            game.make_move((x, y), 'X')
            game.current_player = 'O'
        
        else:
            available_moves = game.get_available_moves()
            if available_moves:
                move = available_moves[0]
                game.make_move(move, 'O')
                game.current_player = 'X'
        
        print()
        game.print_board()
        print()
    
    if game.check_winner('X'):
        print("X wins!")
    elif game.check_winner('O'):
        print("O wins!")
    else:
        print("It's a tie!")

if __name__ == "__main__":
    main()