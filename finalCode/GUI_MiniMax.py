
import tkinter as tk
from tkinter import messagebox


from minimax import checkWinner, getBestMove

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("XO 5x5 - MiniMax AI")
        self.board = [[' ' for _ in range(5)] for _ in range(5)]
        self.buttons = [[None for _ in range(5)] for _ in range(5)]
        self.setup_ui()

    def setup_ui(self):
        for r in range(5):
            for c in range(5):
                btn = tk.Button(self.root, text=' ', font=('Arial', 20, 'bold'),
                                width=4, height=2, bg="#d4d4d4", activebackground="#080c5e",
                                command=lambda row=r, col=c: self.play_turn(row, col))
                btn.grid(row=r, column=c, padx=3, pady=3)
                self.buttons[r][c] = btn

    def play_turn(self, r, c):
        if self.board[r][c] == ' ':
            # المستخدم يلعب بـ 'O'
            self.update_cell(r, c, 'O', "#e079cd")
            
            if not self.is_game_over():
                # تأخير بسيط 300 مللي ثانية لتظهر حركة الكمبيوتر بشكل طبيعي
                self.root.after(300, self.ai_play)

    def ai_play(self):
        # استدعاء دالة الذكاء الاصطناعي المستوردة بعمق 3
        move = getBestMove(self.board, depth=3)
        if move:
            self.update_cell(move[0], move[1], 'X', "#77add1")
            self.is_game_over()

    def update_cell(self, r, c, p, color):
        self.board[r][c] = p
        self.buttons[r][c].config(text=p, state='disabled', disabledforeground=color)

    def is_game_over(self):
        # استدعاء دالة فحص الفوز المستوردة
        result = checkWinner(self.board)
        if result != 0:
            if result == 1:
                msg = "It's a Tie!"
            elif result == -4:
                msg = "Congratulations, You won!"
            else:
                msg = "The Computer wins!"
                
            messagebox.showinfo("End of the Game", msg)
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