import tkinter as tk
from tkinter import messagebox

from rulebased import checkWinner, rule_based_agent 

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("XO 5x5 - Professional AI")
        self.board = [[' ' for _ in range(5)] for _ in range(5)]
        self.buttons = [[None for _ in range(5)] for _ in range(5)]
        self.setup_ui()

    def setup_ui(self):
        for r in range(5):
            for c in range(5):
                btn = tk.Button(self.root, text=' ', font=('Arial', 20, 'bold'),
                                width=4, height=2, bg="#D4D4D4",
                                command=lambda row=r, col=c: self.play_turn(row, col))
                btn.grid(row=r, column=c, padx=3, pady=3)
                self.buttons[r][c] = btn

    def play_turn(self, r, c):
        if self.board[r][c] == ' ':
            self.update_cell(r, c, 'X', "#77add1")
            if not self.is_game_over():
                
                self.root.after(400, self.ai_play)

    def ai_play(self):
        move = rule_based_agent(self.board, 'O')
        if move:
            self.update_cell(move[0], move[1], 'O', "#e079cd")
            self.is_game_over()

    def update_cell(self, r, c, p, color):
        self.board[r][c] = p
        self.buttons[r][c].config(text=p, state='disabled', disabledforeground=color)

    def is_game_over(self):
        result = checkWinner(self.board)
        if result != 0:
            msg ="tie" if result == 1 else f"the winner is {'you' if result == 4 else 'computer'}!"
            messagebox.showinfo("end of the game", msg)
            self.reset_game()
            return True
        return False

    def reset_game(self):
        self.board = [[' ' for _ in range(5)] for _ in range(5)]
        for r in range(5):
            for c in range(5):
                self.buttons[r][c].config(text=' ', state='normal')

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()