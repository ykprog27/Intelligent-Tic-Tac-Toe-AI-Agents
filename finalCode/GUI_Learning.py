import tkinter as tk
from tkinter import messagebox
import numpy as np
import pickle
import os

# استيراد الدوال اللازمة من ملف learning.py
from learning import is_game_over, choose_action, Q

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("XO 5x5 - Q-Learning AI")
        # تهيئة اللوحة (مصفوفة numpy كما يتوقعها ملف learning.py)
        self.board = np.full((5, 5), '-')
        self.buttons = [[None for _ in range(5)] for _ in range(5)]
        
        # محاولة تحميل ملف الـ Q-table إذا كان موجوداً
        self.load_q_table()
        
        self.setup_ui()

    def load_q_table(self):
        # التأكد من تحميل البيانات لضمان ذكاء العميل
        if os.path.exists('q_table_5x5.pkl'):
            with open('q_table_5x5.pkl', 'rb') as f:
                import learning
                learning.Q = pickle.load(f)
        else:
            print("Warning: q_table_5x5.pkl not found. AI will play randomly.")

    def setup_ui(self):
        for r in range(5):
            for c in range(5):
                btn = tk.Button(self.root, text=' ', font=('Arial', 20, 'bold'),
                                width=4, height=2, bg="#d4d4d4", activebackground="#080c5e",
                                command=lambda row=r, col=c: self.play_turn(row, col))
                btn.grid(row=r, column=c, padx=3, pady=3)
                self.buttons[r][c] = btn

    def play_turn(self, r, c):
        if self.board[r, c] == '-':
            # المستخدم يلعب بـ 'X' (حسب منطق learning.py الافتراضي)
            self.update_cell(r, c, 'X', "#a93394")
            
            game_finished, winner = is_game_over(self.board)
            if not game_finished:
                # تأخير بسيط لحركة الـ AI
                self.root.after(300, self.ai_play)
            else:
                self.handle_end_game(winner)

    def ai_play(self):
        # AI يلعب بـ 'O'
        # نستخدم exploration_rate = 0 لضمان اختيار أفضل حركة تعلمها
        move = choose_action(self.board, 'O', exploration_rate=0)
        if move:
            r, c = move
            self.update_cell(r, c, 'O', "#77add1")
            game_finished, winner = is_game_over(self.board)
            if game_finished:
                self.handle_end_game(winner)

    def update_cell(self, r, c, p, color):
        self.board[r, c] = p
        self.buttons[r][c].config(text=p, state='disabled', disabledforeground=color)

    def handle_end_game(self, winner):
        if winner == 'draw':
            msg = "It's a Tie!"
        elif winner == 'X':
            msg = "Congratulations, You won!"
        else:
            msg = "The Learning AI wins!"
            
        messagebox.showinfo("End of the Game", msg)
        self.reset_game()

    def reset_game(self):
        self.board = np.full((5, 5), '-')
        for r in range(5):
            for c in range(5):
                self.buttons[r][c].config(text=' ', state='normal')

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()