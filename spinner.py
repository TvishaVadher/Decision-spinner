import tkinter as tk
import random
import time
import math

# ================= CONFIG ================= #
BG = "#F8FAFC"
BTN = "#E4769B"
TEXT = "#050505"
ARROW = "#666769"

PASTELS = [
    "#FBCFE8",
    "#DDD6FE",
    "#BBF7D0",
    "#FEF3C7",
    "#FED7AA",
    "#E9D5FF",
    "#DCFCE7"
]

WIDTH, HEIGHT = 420, 650
CANVAS_SIZE = 300
CENTER = CANVAS_SIZE // 2
RADIUS = 120

# ================= APP ================= #
root = tk.Tk()
root.title("Decision Spinner")
root.geometry(f"{WIDTH}x{HEIGHT}")
root.configure(bg=BG)

rotation = 0

# DEFAULT EDITABLE OPTIONS
option_vars = [
    tk.StringVar(value="Option 1"),
    tk.StringVar(value="Option 2"),
    tk.StringVar(value="Option 3")
]

def get_options():
    return [v.get() for v in option_vars if v.get().strip()]

# ================= CANVAS ================= #
canvas = tk.Canvas(
    root, width=CANVAS_SIZE, height=CANVAS_SIZE,
    bg=BG, highlightthickness=0
)
canvas.pack(pady=20)

def draw_wheel(angle):
    canvas.delete("all")
    options = get_options()
    if not options:
        return

    slice_angle = 360 / len(options)
    start = angle

    for i, option in enumerate(options):
        canvas.create_arc(
            CENTER - RADIUS, CENTER - RADIUS,
            CENTER + RADIUS, CENTER + RADIUS,
            start=start,
            extent=slice_angle,
            fill=PASTELS[i % len(PASTELS)],
            outline=BG
        )

        mid = math.radians(start + slice_angle / 2)
        x = CENTER + (RADIUS * 0.65) * math.cos(mid)
        y = CENTER - (RADIUS * 0.65) * math.sin(mid)

        canvas.create_text(
            x, y,
            text=option,
            fill=TEXT,
            font=("Poppins", 10, "bold"),
            width=80
        )

        start += slice_angle

    # 🔻 FIXED ARROW
    canvas.create_line(
        CENTER, CENTER - RADIUS - 12,
        CENTER, CENTER - RADIUS + 8,
        width=4,
        fill=ARROW
    )
    canvas.create_polygon(
        CENTER - 8, CENTER - RADIUS + 8,
        CENTER + 8, CENTER - RADIUS + 8,
        CENTER, CENTER - RADIUS + 22,
        fill=ARROW
    )

# ================= OPTION EDITOR ================= #
editor_frame = tk.Frame(root, bg=BG)
editor_frame.pack(pady=5)

def refresh_wheel(*args):
    draw_wheel(rotation)

for i, var in enumerate(option_vars):
    var.trace_add("write", refresh_wheel)

    row = tk.Frame(editor_frame, bg=BG)
    row.pack(pady=3)

    tk.Label(
        row,
        text=f"Option {i+1}:",
        bg=BG,
        fg=TEXT,
        font=("Poppins", 10, "bold"),
        width=8,
        anchor="w"
    ).pack(side="left")

    tk.Entry(
        row,
        textvariable=var,
        font=("Poppins", 11),
        width=20
    ).pack(side="left")

# ================= ADD NEW OPTION ================= #
new_option_entry = tk.Entry(root, font=("Poppins", 12))
new_option_entry.pack(pady=6)

def add_option():
    if new_option_entry.get().strip():
        var = tk.StringVar(value=new_option_entry.get().strip())
        var.trace_add("write", refresh_wheel)
        option_vars.append(var)

        row = tk.Frame(editor_frame, bg=BG)
        row.pack(pady=3)

        tk.Label(
            row,
            text=f"Option {len(option_vars)}:",
            bg=BG,
            fg=TEXT,
            font=("Poppins", 10, "bold"),
            width=8,
            anchor="w"
        ).pack(side="left")

        tk.Entry(
            row,
            textvariable=var,
            font=("Poppins", 11),
            width=20
        ).pack(side="left")

        new_option_entry.delete(0, tk.END)
        draw_wheel(rotation)

tk.Button(
    root,
    text="+ Add Option",
    command=add_option,
    bg=BTN,
    fg="white",
    font=("Poppins", 11, "bold"),
    relief="flat"
).pack()

# ================= RESULT ================= #
result_label = tk.Label(
    root,
    text="",
    bg=BG,
    fg=TEXT,
    font=("Poppins", 14, "bold")
)
result_label.pack(pady=10)

# ================= SPIN ================= #
def spin():
    global rotation
    options = get_options()

    if len(options) < 2:
        result_label.config(text="Add at least 2 options ✨")
        return

    result_label.config(text="Spinning... 🎡")
    root.update()

    rounds = random.randint(3, 6)
    extra = random.randint(0, 359)
    total_spin = rounds * 360 + extra

    steps = 120
    step_angle = total_spin / steps

    for _ in range(steps):
        rotation += step_angle
        draw_wheel(rotation)
        root.update()
        time.sleep(0.015)

    slice_angle = 360 / len(options)
    pointer_angle = (90 - (rotation % 360)) % 360
    index = int(pointer_angle // slice_angle)

    result_label.config(text=f"✨ Decision: {options[index]} ✨")

tk.Button(
    root,
    text="SPIN",
    command=spin,
    bg=BTN,
    fg="white",
    font=("Poppins", 13, "bold"),
    relief="flat",
    padx=22,
    pady=7
).pack()

# ================= INITIAL DRAW ================= #
draw_wheel(rotation)
root.mainloop()
