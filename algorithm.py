import copy
import math

class AI:

    #Inisialisasi player AI
    def __init__(self, player=2):
        self.ai_player = player
        self.algorithm = 1          # 1- minimax    2-alpha beta
        self.difficulty = 'hard'

    # Evaluasi Posisi
    def eval(self, main_board, turn, game_mode, alg=1):

        # Pada awal,  maximizer diset false
        maximizer = False

        # Jika AI pemain pertama (X), AI akan berperan sebagai "maximizer."
        if self.ai_player == 1:
            maximizer = True

        #Memeriksa mode game
        if game_mode == 'aivsai':
            #Peran "maximizer" dan "minimizer" diatur berdasarkan giliran 
            if turn == 1:
                maximizer = True
            else:
                maximizer = False

        # Inisialisasi alpha = - tak hingga, beta = tak hingga
        a, b = -math.inf, math.inf

        #Jika pilih algoritma 1 -> masuk ke minimax, selain itu, alpha beta
        if alg == 1:                                                # alg = 1 -> Minimax
            eval_, move = self.minimax(main_board, maximizer)
        else:                                                       # alg = 2 -> alpha beta
            eval_, move = self.alpha_beta(main_board, maximizer, a, b)

        #Cetak informasi langkah AI
        print(f'AI has chosen to mark the square in pos {move} with an eval of: {eval_}')

        return move  # Mengembalikan langkah (row, col)

    # ALGORITMA MINIMAX
    # ambil 3 parameter
    def minimax(self, board, maximizing):

        # Mengecek pemenang dan disimpan ke variable case
        case = board.winner()

        # Player X wins (nilai 1)
        if case == 1:
            return 1, None  # hasil eval, langkah/move
        
        # Player O wins (nilai -1)
        if case == 2: 
            return -1, None 
        
        # Draw (nilai 0)
        if board.isfull():
            return 0, None

        # Kondisi player maximizing
        if maximizing:
            max_eval = -100 # Untuk mencari skor yg lebih tinggi dari ini
            best_move = None #Belum ada langkah terbaik
            empty_sqrs = board.get_empty_sqrs() # Menyimpan daftar square

            # Jika easy
            if self.difficulty == 'easy':
                empty_sqrs = empty_sqrs[:5] #Pencarian hanya pada 5 sel kosong pertama

            # Iterasi 
            for (row, col) in empty_sqrs:

                temp_board = copy.deepcopy(board) #Board dicopy untuk mencoba langkah
                temp_board.mark_sqr(row, col, 1) #Menandai sel kosong
                eval_ = self.minimax(temp_board, False)[0] #masuk fungsi

                #Memperoleh skor maksimum & nilai diupdate
                if eval_ > max_eval:
                    max_eval = eval_
                    best_move = (row, col)

            return max_eval, best_move

        # Kondisi player minimizing
        elif not maximizing:
            min_eval = 100 # Untuk mencari skor yg lebih rendah dari ini
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            if self.difficulty == 'easy':
                empty_sqrs = empty_sqrs[:5]

            #Iterasi
            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 2)
                eval_ = self.minimax(temp_board, True)[0]

                #Memperoleh skor minimum & nilai diupdate
                if eval_ < min_eval:
                    min_eval = eval_
                    best_move = (row, col)

            return min_eval, best_move

    # ALPHA BETA PRUNING
    def alpha_beta(self, board, maximizing, a, b):
        # terminal case
        case = board.winner()

        # Player X wins
        if case == 1:
            return 1, None  # eval, move
        # Player O wins
        if case == 2:
            return -1, None
        # Draw
        if board.isfull():
            return 0, None

        # Kondisi Maximizing
        if maximizing:
            max_eval = -100 #  Untuk mencari skor yg lebih tinggi dari ini
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            if self.difficulty == 'easy':
                empty_sqrs = empty_sqrs[:5]

            # Iterasi untuk menemukan nilai max
            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval_ = self.alpha_beta(temp_board, False, a, b)[0] # Memanggil fungsi alpha beta
               
               # Menemukan nilai max dan diupdate
                if eval_ > max_eval:
                    max_eval = eval_
                    best_move = (row, col)

                # Jika nilai max eval lebih besar atau sama dengan nilai beta, dilakukan beta cut/pemangkasan
                if max_eval >= b:
                    print('Beta cut')
                    break
                a = max(a, max_eval)
                print(f'alpha value is {a}') # nilai alpha dicetak

            return max_eval, best_move

         # Kondisi Minimizing
        elif not maximizing:
            min_eval = 100 #  Untuk mencari skor yg lebih tinggi dari ini
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            if self.difficulty == 'easy':
                empty_sqrs = empty_sqrs[:5]

            #Iterasi
            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 2)
                eval_ = self.alpha_beta(temp_board, True, a, b)[0]

                #Menemukan nilai minimum
                if eval_ < min_eval:
                    min_eval = eval_
                    best_move = (row, col)

                #Jika nilai minimum <= a, maka dilakukan pemangkasa/alpha cut
                if min_eval <= a:
                    print('alpha cut')
                    break

                b = min(b, min_eval)
                print(f'Beta value is {b}') # mencetak nilai beta

            return min_eval, best_move



