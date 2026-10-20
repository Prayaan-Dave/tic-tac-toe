
import tkinter as tk
import random

# ---------- GAME SETTINGS ----------
BG = "#101827"
CELL = "#202e44"
BLUE = "#38bdf8"
GREEN = "#4ade80"
WHITE = "#f8fafc"

board = [""] * 9
buttons = []
human_score = 0
ai_score = 0
ties = 0
game_over = False

root = tk.Tk()
root.title("Tic-Tac-Toe AI")
root.geometry("440x590")
root.resizable(False, False)
root.configure(bg=BG)

# ---------- WIN CHECK ----------
def winner(b):
    lines = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]

    for a, c, d in lines:
        if b[a] and b[a] == b[c] == b[d]:
            return b[a]
    return None


# ---------- HARD AI: MINIMAX ----------
def minimax(b, ai_turn):
    result = winner(b)

    if result == "O":
        return 1
    if result == "X":
        return -1
    if "" not in b:
        return 0

    scores = []

    for i in range(9):
        if b[i] == "":
            b[i] = "O" if ai_turn else "X"
            score = minimax(b, not ai_turn)
            b[i] = ""
            scores.append(score)

    return max(scores) if ai_turn else min(scores)


def ai_move():
    available = [i for i in range(9) if board[i] == ""]

    if difficulty.get() == "Easy":
        return random.choice(available)

    if difficulty.get() == "Medium":
        # Win if possible
        for i in available:
            board[i] = "O"
            if winner(board) == "O":
                board[i] = ""
                return i
            board[i] = ""

        # Otherwise block the player
        for i in available:
            board[i] = "X"
            if winner(board) == "X":
                board[i] = ""
                return i
            board[i] = ""

        return random.choice(available)

    # Hard: choose the best move using minimax
    best_score = -999
    best_moves = []

    for i in available:
        board[i] = "O"
        score = minimax(board, False)
        board[i] = ""

        if score > best_score:
            best_score = score
            best_moves = [i]
        elif score == best_score:
            best_moves.append(i)

    return random.choice(best_moves)


# ---------- UPDATE DISPLAY ----------
def update_score():
    score_label.config(
        text=f"YOU: {human_score}     AI: {ai_score}     TIES: {ties}"
    )


def finish_round():
    global game_over, human_score, ai_score, ties

    result = winner(board)

    if result == "X":
        game_over = True
        human_score += 1
        status.config(text="🎉 YOU WIN!", fg=GREEN)
    elif result == "O":
        game_over = True
        ai_score += 1
        status.config(text="🤖 AI WINS!", fg="#fb7185")
    elif "" not in board:
        game_over = True
        ties += 1
        status.config(text="🤝 IT'S A DRAW!", fg=BLUE)
    else:
        return False

    update_score()
    return True


def refresh_cell(i):
    buttons[i].config(
        text=board[i],
        fg=BLUE if board[i] == "X" else "#fb7185",
        state="disabled" if board[i] else "normal"
    )


# ---------- PLAYER MOVE ----------
def player_move(i):
    if game_over or board[i] != "":
        return

    board[i] = "X"
    refresh_cell(i)

    if finish_round():
        return

    status.config(text="AI IS THINKING...", fg=WHITE)
    root.after(350, computer_turn)


def computer_turn():
    if game_over:
        return

    move = ai_move()
    board[move] = "O"
    refresh_cell(move)

    if not finish_round():
        status.config(text="YOUR TURN — PLAY X", fg=BLUE)


# ---------- NEW GAME ----------
def new_round():
    global board, game_over

    board = [""] * 9
    game_over = False

    for i in range(9):
        buttons[i].config(
            text="",
            state="normal",
            bg=CELL,
            fg=WHITE
        )

    status.config(text="YOUR TURN — PLAY X", fg=BLUE)


def reset_scores():
    global human_score, ai_score, ties
    human_score = ai_score = ties = 0
    update_score()
    new_round()


# ---------- INTERFACE ----------
tk.Label(
    root, text="TIC-TAC-TOE",
    font=("Arial", 27, "bold"),
    bg=BG, fg=BLUE
).pack(pady=(18, 2))

tk.Label(
    root, text="CAN YOU BEAT THE COMPUTER?",
    font=("Arial", 10, "bold"),
    bg=BG, fg=WHITE
).pack(pady=(0, 12))

score_label = tk.Label(
    root, text="YOU: 0     AI: 0     TIES: 0",
    font=("Arial", 12, "bold"),
    bg=BG, fg=GREEN
)
score_label.pack(pady=6)

difficulty = tk.StringVar(value="Hard")

tk.Label(
    root, text="AI DIFFICULTY",
    font=("Arial", 10, "bold"),
    bg=BG, fg=WHITE
).pack(pady=(8, 4))

tk.OptionMenu(
    root, difficulty, "Easy", "Medium", "Hard"
).pack()

status = tk.Label(
    root, text="YOUR TURN — PLAY X",
    font=("Arial", 12, "bold"),
    bg=BG, fg=BLUE
)
status.pack(pady=12)

grid = tk.Frame(root, bg=BG)
grid.pack()

for i in range(9):
    button = tk.Button(
        grid,
        text="",
        font=("Arial", 30, "bold"),
        width=3,
        height=1,
        bg=CELL,
        fg=WHITE,
        activebackground="#34465f",
        relief="flat",
        command=lambda i=i: player_move(i)
    )
    button.grid(
        row=i // 3,
        column=i % 3,
        padx=5,
        pady=5,
        ipadx=8,
        ipady=8
    )
    buttons.append(button)

tk.Button(
    root, text="🔄  NEW ROUND",
    font=("Arial", 12, "bold"),
    bg=BLUE, fg=BG,
    activebackground=GREEN,
    relief="flat",
    command=new_round
).pack(fill="x", padx=45, pady=(17, 7), ipady=5)

tk.Button(
    root, text="RESET SCORES",
    font=("Arial", 10, "bold"),
    bg=CELL, fg=WHITE,
    activebackground="#34465f",
    relief="flat",
    command=reset_scores
).pack(fill="x", padx=45, ipady=4)

tk.Label(
    root, text="YOU PLAY X     •     COMPUTER PLAYS O",
    font=("Arial", 9),
    bg=BG, fg="#94a3b8"
).pack(pady=12)

root.mainloop()
