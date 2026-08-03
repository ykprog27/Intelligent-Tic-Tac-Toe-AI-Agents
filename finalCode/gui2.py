import tkinter as tk
from tkinter import font
import GUI_RuleBased
import GUI_MiniMax
import GUI_Learning

class AgentSelectionMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Select AI Opponent")
        self.root.geometry("400x600")
        self.root.configure(bg="#f4f0fd") 

        self.color_blue = "#77add1" 
        self.color_pink = "#e079cd"
        
        self.title_font = font.Font(family="Arial", size=28, weight="bold")
        self.button_font = font.Font(family="Arial", size=14, weight="bold")

        self.setup_ui()

    def setup_ui(self):
        lbl_title = tk.Label(self.root, text="Choose Your\nAI Opponent", font=self.title_font, 
                             fg=self.color_pink, bg="#fdf0f6", pady=50)
        lbl_title.pack()

        # زر Rule-Based
        tk.Button(self.root, text="Rule-Based Agent", font=self.button_font,
                  bg=self.color_blue, fg="white", width=20, height=2,
                  relief="flat", command=self.open_rule).pack(pady=10)

        # زر MiniMax
        tk.Button(self.root, text="MiniMax Agent", font=self.button_font,
                  bg=self.color_pink, fg="white", width=20, height=2,
                  relief="flat", command=self.open_minimax).pack(pady=10)

        # زر Learning
        tk.Button(self.root, text="Learning Agent", font=self.button_font,
                  bg=self.color_blue, fg="white", width=20, height=2,
                  relief="flat", command=self.open_learning).pack(pady=10)

    def open_rule(self):
        self.launch_game(GUI_RuleBased)

    def open_minimax(self):
        self.launch_game(GUI_MiniMax)

    def open_learning(self):
        self.launch_game(GUI_Learning)

    def launch_game(self, module):
        game_win = tk.Toplevel()
        module.TicTacToeGUI(game_win) 

if __name__ == "__main__":
    root = tk.Tk()
    app = AgentSelectionMenu(root)
    root.mainloop()