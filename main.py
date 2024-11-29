import tkinter as tk
import copy

class MainUI():
    def __init__(self):
        self.root = tk.Tk()
        self.button1 = tk.Button(self.root, text="New Game", command = self.launch_new_game)
        self.button1.pack()

        self.root.mainloop()

    def launch_new_game(self):
        Board()

class Board:
    
    selected = None
    current_turn = "white"
    def on_click(self, row, col):
        # place if selected
        if self.selected and (row, col) != (self.selected[0], self.selected[1]) and self.available[row][col]: # for test

            # check for promotion
            if self.board[self.selected[0]][self.selected[1]] == self.black_pieces[5] and row == 7:
                self.promote_pawn(row, col, "black")
            
            elif self.board[self.selected[0]][self.selected[1]] == self.white_pieces[5] and row == 0:
                self.promote_pawn(row, col, "white")
            
            
            else:
                self.board[row][col] = self.board[self.selected[0]][self.selected[1]]
                self.board_buttons[row][col].config(text = self.board[self.selected[0]][self.selected[1]])

            self.board[self.selected[0]][self.selected[1]] = " "
            self.board_buttons[self.selected[0]][self.selected[1]].config(text = " ")

            self.restore_square_color(self.selected[0], self.selected[1])

            if self.selected[2] == "white":
                self.label1.config(text = "Black's \n turn")
                self.current_turn = "black"
                self.check_for_check(self.board, "black")
            else:
                self.label1.config(text = "White's \n turn")
                self.current_turn = "white"
                self.check_for_check(self.board, "white")


            self.selected = None
            self.hide_available_moves()

        
        # deselect if selected
        elif self.selected and (row, col) == (self.selected[0], self.selected[1]):
            self.selected = None
            self.hide_available_moves()
            self.restore_square_color(row, col)

        # select piece/square
        elif self.board[row][col] != " " and ((self.current_turn == "black" and self.board[row][col] in self.black_pieces) or (self.current_turn == "white" and self.board[row][col] in self.white_pieces)):
            if self.board[row][col] in self.white_pieces:
                self.selected_color = "white"
            else:
                self.selected_color = "black"
            # (row, column, color, piece)
            self.selected = (row, col, self.selected_color, self.board[row][col])
            self.mark_available_moves(row, col)
            self.board_buttons[self.selected[0]][self.selected[1]].config(bg = 'yellow')
    
    def check_available_moves(self, board, row, col):
        r = row
        c = col

        # for white pawn
        if board[r][c] == self.white_pieces[5] and r == 6 and board[r-1][c] == " " and board[r-2][c] == " ":
            self.available[r-1][c] = 1
            self.available[r-2][c] = 1

        elif board[r][c] == self.white_pieces[5] and r != 0 and board[r-1][c] == " ":
            self.available[r-1][c] = 1
        
        # capturable
        if board[r][c] == self.white_pieces[5] and r >= 1 and col <= 6 and board[r-1][c+1] != " " and board[r-1][c+1] in self.black_pieces:
            self.available[r-1][c+1] = 1

        if board[r][c] == self.white_pieces[5] and r >= 1 and col >= 1 and board[r-1][c-1] != " " and board[r-1][c-1] in self.black_pieces:
            self.available[r-1][c-1] = 1
        
        
        # for black pawn
        if board[r][c] == self.black_pieces[5]  and r == 1 and board[r+1][c] == " " and board[r+2][c] == " ":
            self.available[r+1][c] = 1
            self.available[r+2][c] = 1

        elif board[r][c] == self.black_pieces[5] and r != 7 and board[r+1][c] == " ":
            self.available[r+1][c] = 1
        
        # capturable
        if board[r][c] == self.black_pieces[5] and r <= 6 and col <= 6 and board[r+1][c+1] != " " and board[r+1][c+1] in self.white_pieces:
            self.available[r+1][c+1] = 1

        if board[r][c] == self.black_pieces[5] and r <= 6 and col >= 1 and board[r+1][c-1] != " " and board[r+1][c-1] in self.white_pieces:
            self.available[r+1][c-1] = 1
        
        
        # for rooks and queens (mark straight)
        if board[r][c] in [self.white_pieces[2], self.black_pieces[2], self.white_pieces[1], self.black_pieces[1]]:
            ra = r + 1
            rc = c
            while ra <= 7 and ra >= 0:
                if board[ra][rc] == " ":
                    self.available[ra][rc] = 1
                    ra += 1
                elif (board[ra][rc] in self.white_pieces and self.selected[2] == "white") or (board[ra][rc] in self.black_pieces and self.selected[2] == "black"):
                    break
                else:
                    self.available[ra][rc] = 1
                    break
            ra = r-1
            rc = c
            while ra <= 7 and ra >= 0:
                if board[ra][rc] == " ":
                    self.available[ra][rc] = 1
                    ra -= 1
                elif (board[ra][rc] in self.white_pieces and self.selected[2] == "white") or (board[ra][rc] in self.black_pieces and self.selected[2] == "black"):
                    break
                else:
                    self.available[ra][rc] = 1
                    break
            ra = r
            rc = c+1
            while rc <= 7 and rc >= 0:
                if board[ra][rc] == " ":
                    self.available[ra][rc] = 1
                    rc += 1
                elif (board[ra][rc] in self.white_pieces and self.selected[2] == "white") or (board[ra][rc] in self.black_pieces and self.selected[2] == "black"):
                    break
                else:
                    self.available[ra][rc] = 1
                    break
            ra = r
            rc = c-1
            while rc <= 7 and rc >= 0:
                if board[ra][rc] == " ":
                    self.available[ra][rc] = 1
                    rc -= 1
                elif (board[ra][rc] in self.white_pieces and self.selected[2] == "white") or (board[ra][rc] in self.black_pieces and self.selected[2] == "black"):
                    break
                else:
                    self.available[ra][rc] = 1
                    break


        # for bishops and queens (mark diagonals)
        if board[r][c] in [self.white_pieces[3], self.black_pieces[3], self.white_pieces[1], self.black_pieces[1]]:
            ra = r + 1
            rc = c + 1
            while ra <= 7 and ra >= 0 and rc <= 7 and rc >= 0:
                if board[ra][rc] == " ":
                    self.available[ra][rc] = 1
                    ra += 1
                    rc += 1
                elif (board[ra][rc] in self.white_pieces and self.selected[2] == "white") or (board[ra][rc] in self.black_pieces and self.selected[2] == "black"):
                    break
                else:
                    self.available[ra][rc] = 1
                    break
            ra = r - 1
            rc = c + 1
            while ra <= 7 and ra >= 0 and rc <= 7 and rc >= 0:
                if board[ra][rc] == " ":
                    self.available[ra][rc] = 1
                    ra -= 1
                    rc += 1
                elif (board[ra][rc] in self.white_pieces and self.selected[2] == "white") or (board[ra][rc] in self.black_pieces and self.selected[2] == "black"):
                    break
                else:
                    self.available[ra][rc] = 1
                    break
            ra = r + 1
            rc = c - 1
            while ra <= 7 and ra >= 0 and rc <= 7 and rc >= 0:
                if board[ra][rc] == " ":
                    self.available[ra][rc] = 1
                    ra += 1
                    rc -= 1
                elif (board[ra][rc] in self.white_pieces and self.selected[2] == "white") or (board[ra][rc] in self.black_pieces and self.selected[2] == "black"):
                    break
                else:
                    self.available[ra][rc] = 1
                    break
            ra = r - 1
            rc = c - 1
            while ra <= 7 and ra >= 0 and rc <= 7 and rc >= 0:
                if board[ra][rc] == " ":
                    self.available[ra][rc] = 1
                    ra -= 1
                    rc -= 1
                elif (board[ra][rc] in self.white_pieces and self.selected[2] == "white") or (board[ra][rc] in self.black_pieces and self.selected[2] == "black"):
                    break
                else:
                    self.available[ra][rc] = 1
                    break


        # for kings
        if board[r][c] in [self.black_pieces[0], self.white_pieces[0]]:
            mark_moves = [(r+1, c+1), (r-1, c-1), (r+1, c-1), (r-1, c+1), (r+1, c), (r-1, c), (r, c+1), (r, c-1)]
            for tup in mark_moves:
                if tup[0] >= 0 and tup[0] <= 7 and tup[1] >= 0 and tup[1] <= 7:
                    if board[tup[0]][tup[1]] == " ":
                        self.available[tup[0]][tup[1]] = 1
                    elif (board[tup[0]][tup[1]] in self.black_pieces and self.selected[2] == "white") or (board[tup[0]][tup[1]] in self.white_pieces and self.selected[2] == "black"):
                        self.available[tup[0]][tup[1]] = 1

        # for knights
        if board[r][c] in [self.black_pieces[4], self.white_pieces[4]]:
            mark_moves =  [(r+2, c+1), (r+2, c-1), (r-2, c+1), (r-2, c-1), (r+1, c+2), (r+1, c-2), (r-1, c+2), (r-1, c-2)]
            for tup in mark_moves:
                if tup[0] >= 0 and tup[0] <= 7 and tup[1] >= 0 and tup[1] <= 7:
                    if board[tup[0]][tup[1]] == " ":
                        self.available[tup[0]][tup[1]] = 1
                    elif (board[tup[0]][tup[1]] in self.black_pieces and self.selected[2] == "white") or (board[tup[0]][tup[1]] in self.white_pieces and self.selected[2] == "black"):
                        self.available[tup[0]][tup[1]] = 1
        
        return self.available
        
    def mark_available_moves(self, row, col):
        new_available = copy.deepcopy(self.check_available_moves(self.board, row, col))

        # hide all moves that results in self-check
        # if self.selected[2] == "black":
        #     for x in range(8):
        #         for y in range(8):
        #             if new_available[x][y]:
        #                 new_board = copy.deepcopy(self.board)
        #                 new_board[x][y] = self.board[self.selected[0]][self.selected[1]]
        #                 new_board[self.selected[0]][self.selected[1]] = " "
        #                 if self.check_for_check(new_board, "black"):
        #                     new_available[x][y] = 0
                            
        # else:
        #     for x in range(8):
        #         for y in range(8):
        #             if new_available[x][y]:
        #                 new_board = copy.deepcopy(self.board)
        #                 new_board[x][y] = self.board[self.selected[0]][self.selected[1]]
        #                 new_board[self.selected[0]][self.selected[1]] = " "
        #                 if self.check_for_check(new_board, "white"):
        #                     new_available[x][y] = 0
            
        
        # mark all available
        for x in range(8):
            for y in range(8):
                if new_available[x][y]:
                    self.board_buttons[x][y].config(bg = 'blue')
        
    def hide_available_moves(self):
        for x in range(8):
            for y in range(8):
                if self.available[x][y]:
                    self.restore_square_color(x,y)
                    self.available[x][y] = 0
    
    def restore_square_color(self, r, c):
        if (r + c) % 2 == 0:
            self.board_buttons[r][c].config(bg = 'white')
        else:
            self.board_buttons[r][c].config(bg = 'gray')
    
    def on_click_promote_pawn(self, row, col, piece):
        self.board[row][col] = piece
        self.board_buttons[row][col].config(text = piece)
        self.pawn_win.destroy()
        
        
    def promote_pawn(self, row, col, color):
        self.pawn_win = tk.Tk()
        self.button1 = [None for _ in range(4)]

        for i in range(4):
            self.button1[i] = tk.Button(self.pawn_win)
            if color == "black":
                self.button1[i].config(text = self.black_pieces[i+1])
                self.button1[i].config(command = lambda  r = row, c = col, i_new = i + 1 : self.on_click_promote_pawn(r, c, self.black_pieces[i_new]))
            else:
                self.button1[i].config(text = self.white_pieces[i+1])
                self.button1[i].config(command = lambda  r = row, c = col, i_new = i + 1 : self.on_click_promote_pawn(r, c, self.white_pieces[i_new]))
            
            self.button1[i].config(width = 2, height = 1, font = ("Calibri", 40))
            self.button1[i].grid(row = 0, column = i)
    
    def check_for_check(self, new_board, to_color):
        if to_color == "black":
            for x in range(8):
                for y in range(8):
                    if new_board[x][y] in self.white_pieces:
                        available_moves = self.check_available_moves(new_board, x, y)
                        # print(f"current_square = {x}{y} and available_matrix = {available_moves}")
                        for x1 in range(8):
                            for y1 in range(8):
                                if available_moves[x1][y1] and new_board[x1][y1] == self.black_pieces[0]:
                                    print("currently in check")
                                    return True
        else:
            for x in range(8):
                for y in range(8):
                    if new_board[x][y] in self.black_pieces:
                        available_moves = self.check_available_moves(new_board, x, y)
                        # print(f"current_square = {x}{y} and available_matrix = {available_moves}")
                        for x1 in range(8):
                            for y1 in range(8):
                                if available_moves[x1][y1] and new_board[x1][y1] == self.white_pieces[0]:
                                    print("currently in check")
                                    return True

                        
        
            
        
    def __init__(self):
        self.root = tk.Tk()
        rows = 8
        cols = 8

        self.board = [[" " for _ in range(cols)] for _ in range(rows)]

        # pieces = [king(0), queen(1), rook(2), bishop(3), knight(4), pawn(5)]
        self.black_pieces = ["♚", "♛", "♜", "♝", "♞", "♟"]
        self.white_pieces = ["♔", "♕", "♖", "♗", "♘", "♙"]

        # pawns
        for col in range(cols):
            self.board[1][col] = self.black_pieces[5]
            self.board[6][col] = self.white_pieces[5]
        self.board[0][0] = self.black_pieces[2]
        self.board[0][7] = self.black_pieces[2]
        self.board[7][0] = self.white_pieces[2]
        self.board[7][7] = self.white_pieces[2]
        self.board[0][1] = self.black_pieces[4]
        self.board[0][6] = self.black_pieces[4]
        self.board[7][1] = self.white_pieces[4]
        self.board[7][6] = self.white_pieces[4]
        self.board[0][2] = self.black_pieces[3]
        self.board[0][5] = self.black_pieces[3]
        self.board[7][2] = self.white_pieces[3]
        self.board[7][5] = self.white_pieces[3]
        self.board[0][3] = self.black_pieces[1]
        self.board[0][4] = self.black_pieces[0]
        self.board[7][3] = self.white_pieces[1]
        self.board[7][4] = self.white_pieces[0]



        self.board_buttons = [[None for _ in range(cols)] for _ in range(rows)]
        self.available = [[0 for _ in range(cols)] for _ in range(rows)]
        for row in range(rows):
            for col in range(cols):
                if (row + col) % 2 == 0:
                    self.board_buttons[row][col] = tk.Button(self.root, text = self.board[row][col], command = lambda r = row, c = col : self.on_click(r, c), bg = 'white', width = 2, height = 1, font = ("Calibri", 40))
                else:
                    self.board_buttons[row][col] = tk.Button(self.root, text = self.board[row][col], command = lambda r = row, c = col : self.on_click(r, c), bg = 'gray', width = 2, height = 1, font = ("Calibri", 40))
                self.board_buttons[row][col].grid(row = row, column = col)

        self.label1 = tk.Label(self.root, text="White's \n turn")
        self.label1.grid(row = 8, column=0)
        
        self.root.mainloop()


if __name__ == "__main__":
    Board()
    # MainUI()
        
    