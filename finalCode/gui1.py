import tkinter as tk
from tkinter import font
from gui2 import AgentSelectionMenu

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe - Ultimate")
        self.root.geometry("400x600")
        self.root.configure(bg="white")

        self.color_blue = "#77add1"
        self.color_pink = "#a93394"
        
        self.title_font = font.Font(family="Arial", size=40, weight="bold")
        self.button_font = font.Font(family="Arial", size=14, weight="bold")

        self.setup_ui()

    def setup_ui(self):
        # الديكور العلوي
        self.canvas = tk.Canvas(self.root, width=400, height=200, bg="white", highlightthickness=0)
        self.canvas.pack(pady=20)
        self.canvas.create_line(133, 0, 133, 200, fill="#E0F0FF")
        self.canvas.create_line(266, 0, 266, 200, fill="#E0F0FF")

        lbl_title = tk.Label(self.root, text="TIC TAC TOE", font=self.title_font, 
                             fg="#1DB2F7", bg="white")
        lbl_title.pack(pady=10)

        
        btn_1p = tk.Button(self.root, text="1 Player", font=self.button_font,
                           bg="#DD66CF", fg="white", width=15, height=2,
                           relief="flat", command=self.open_selection)
        btn_1p.pack(pady=15)

        
    def open_selection(self):
        self.root.withdraw() 
        selection_win = tk.Toplevel() 
        AgentSelectionMenu(selection_win)
        selection_win.protocol("WM_DELETE_WINDOW", lambda: self.on_close(selection_win))

    def on_close(self, win):
        win.destroy()
        self.root.deiconify()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainMenu(root)
    root.mainloop()