import chess
import random

VALUES = {chess.PAWN : 100,
          chess.KNIGHT : 300,
          chess.BISHOP : 320,
          chess.ROOK : 500,
          chess.QUEEN : 900}

def search(board: chess.Board) -> chess.Move :

    for move in board.legal_moves :
        board.push(move)
        if board.is_checkmate() :
            board.pop()
            return move
        board.pop()

    hanging_squares = []
    
    for square in chess.SquareSet(board.occupied_co[1 - int(board.turn)]) :
        if board.attackers(1 - int(board.turn), square) == chess.SquareSet(0) :
            hanging_squares.append(square)

    def score_capture(move: chess.Move) -> int :
    
        if board.piece_type_at(move.to_square) == chess.PAWN and board.piece_type_at(move.from_square) == chess.PAWN :
            return 1
        
        elif board.is_en_passant(move) :
            return 1
    
        elif not (move.to_square in hanging_squares) :
            return VALUES[board.piece_type_at(move.to_square)] - VALUES[board.piece_type_at(move.from_square)]

        else :
            return VALUES[board.piece_type_at(move.to_square)]

    captures = list(board.generate_legal_captures())
    captures.sort(key=score_capture, reverse=True)

    if len(captures) :
        if score_capture(captures[0]) > 0 :
            return captures[0]

    moves = list(board.legal_moves)
    random.shuffle(moves)
    for move in moves :
        if not board.is_capture(move) :
            return move
    
    if len(moves) :
        return random.choice(moves)
    return '0000'

def pretty_fen(fen) :
    FEN = ''
    for i in ''.join(fen.replace('/', '').split(' ')[0]) :
        if i.isdigit() :
            FEN += int(i) * ' '
        else :
            FEN += i

    board = ' +---+---+---+---+---+---+---+---+'
    count = 0
    for i in range(8) :
        board += '\n'
        for j in range(8) :
            board += ' | ' + FEN[count]
            count += 1
        board += ' | ' + str(8-i)
        board += '\n +---+---+---+---+---+---+---+---+'
    board += '\n   a   b   c   d   e   f   g   h'
    board += '\n\nFen : ' + fen

    return board

def main() -> None :

    board = chess.Board()
    book = True

    print('Imporver-Engine by Paul JF')

    while True :

        inp = input().split()

        try :
            
            if inp[0] == 'uci' :
                print('id name Imporver-Engine\nid author Paul JF\n')
                print('uciok')

            elif inp[0] == 'isready' :
                print('readyok')

            elif inp[0] == 'ucinewgame' :
                board = chess.Board()

            elif inp[0] == 'd' :
                print()
                print(pretty_fen(board.fen()))

            elif inp[0] == 'quit' :
                break

            elif inp[0] == 'position' :

                try : # if fen is invalid

                    if inp[1] == 'startpos' :
                        board = chess.Board()

                    elif inp[1] == 'fen' :

                        if 'moves' in inp :
                            board = chess.Board(
                                ' '.join(inp[2:inp.index('moves')])
                                )
                        else :
                            board = chess.Board(' '.join(inp[2:]))

                    if 'moves' in inp :
                        for move in inp[inp.index('moves')+1:] :
                            board.push_uci(move)

                except Exception :
                    print('Invalid FEN or moves')

            elif inp[0] == 'go' :
                move = search(board)
                print('bestmove ' + str(move))

        except IndexError :
            pass

if __name__ == '__main__' :
    main()