import tkinter as tk
from tkinter import messagebox, simpledialog

# ---- CONFIG ----
BOSS_HP = 2_770_000_000  # -- Hard-coded HP

def parse_time_days_hours(days: str, hours: str) -> float:
    """
    Convert days + hours into total seconds.
    """
    try:
        d = float(days) if days else 0
        h = float(hours) if hours else 0
        return d * 86400 + h * 3600
    except ValueError:
        raise ValueError("Days and hours must be numbers")

def check():
    try:
        t_left = parse_time_days_hours(days_entry.get(), hours_entry.get())
        dps = float(curr_dps.get())
        if t_left <= 0 or dps <= 0:
            raise ValueError("Time and DPS must be > 0")

        time_to_finish = HP_VAR.get() / dps
        ok = time_to_finish <= t_left

        verdict.set("YES ✅" if ok else "NO ❌")
        info.set(
            f"HP: {HP_VAR.get():,} | Time left: {t_left/3600:.1f}h | "
            f"Finish time: {time_to_finish/3600:.1f}h | "
            f"Req DPS: {HP_VAR.get() / t_left:.2f}"
        )
        result.config(fg=("green" if ok else "red"))
    except ValueError as e:
        messagebox.showerror("Input error", str(e))

def change_hp():
    try:
        new_hp = simpledialog.askstring("Change HP", "Enter new HP (number):", parent=root)
        if new_hp is None:
            return
        val = float(new_hp)
        if val < 0:
            raise ValueError("HP must be ≥ 0")
        HP_VAR.set(val)
        check()  # refresh output
    except ValueError as e:
        messagebox.showerror("Input error", str(e))

# ---- UI ----
root = tk.Tk()
root.title("Finish In Time? (Days/Hours)")
root.geometry("360x230")

HP_VAR = tk.DoubleVar(value=BOSS_HP)

# Time input
tk.Label(root, text="Time Left").pack(pady=(6, 0))
time_frame = tk.Frame(root)
time_frame.pack()
tk.Label(time_frame, text="Days:").grid(row=0, column=0)
days_entry = tk.Entry(time_frame, width=5); days_entry.grid(row=0, column=1, padx=4)
days_entry.insert(0, "6")  # sample

tk.Label(time_frame, text="Hours:").grid(row=0, column=2)
hours_entry = tk.Entry(time_frame, width=5); hours_entry.grid(row=0, column=3, padx=4)
hours_entry.insert(0, "22")  # sample

# DPS input
tk.Label(root, text="Current DPS").pack(pady=(6, 0))
curr_dps = tk.Entry(root); curr_dps.pack()
curr_dps.insert(0, "2745")  # sample

# Buttons
btns = tk.Frame(root); btns.pack(pady=6)
tk.Button(btns, text="Check", command=check).pack(side="left", padx=6)
tk.Button(btns, text="Change HP", command=change_hp).pack(side="left", padx=6)

# Result
verdict = tk.StringVar(value="—")
result = tk.Label(root, textvariable=verdict, font=("Segoe UI", 16, "bold"))
result.pack()

info = tk.StringVar(value=f"HP: {int(HP_VAR.get()):,}")
tk.Label(root, textvariable=info, justify="left").pack(pady=4)

root.mainloop()
