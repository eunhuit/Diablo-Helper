import tkinter as tk
from tkinter import ttk
import pyautogui
import keyboard
import threading
import time

running = False

def toggle_running():
    global running
    running = not running
    status_label.config(
        text=f"● {'RUNNING' if running else 'STOPPED'}",
        foreground="green" if running else "red"
    )

def macro_loop():
    global running
    while True:
        if running:
            actions = [
                (key1_var, key1_delay, lambda: pyautogui.press('1')),
                (key2_var, key2_delay, lambda: pyautogui.press('2')),
                (key3_var, key3_delay, lambda: pyautogui.press('3')),
                (key4_var, key4_delay, lambda: pyautogui.press('4')),
                (lclick_var, lclick_delay, lambda: pyautogui.click(button='left')),
                (rclick_var, rclick_delay, lambda: pyautogui.click(button='right')),
            ]

            for var, delay, action in actions:
                if not running:
                    break
                if var.get():
                    action()
                    time.sleep(delay.get())

            time.sleep(cycle_delay.get())
        else:
            time.sleep(0.05)

def pause_listener():
    keyboard.add_hotkey('pause', toggle_running)
    keyboard.wait()

# ================= GUI =================

root = tk.Tk()
root.title("Diablo Helper")
root.resizable(False, False)

main = ttk.Frame(root, padding=15)
main.pack()

ttk.Label(main, text="Diablo Helper", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=3, pady=(0, 10))

# ---- Header ----
ttk.Label(main, text="사용", width=8).grid(row=1, column=0)
ttk.Label(main, text="키", width=10).grid(row=1, column=1)
ttk.Label(main, text="딜레이 (초)", width=12).grid(row=1, column=2)

def add_row(row, text, var, delay_var):
    ttk.Checkbutton(main, variable=var).grid(row=row, column=0)
    ttk.Label(main, text=text).grid(row=row, column=1, sticky="w")
    ttk.Entry(main, textvariable=delay_var, width=10).grid(row=row, column=2)

# ---- Variables ----
default_speed = 0.001

key1_var = tk.BooleanVar(value=True)
key2_var = tk.BooleanVar(value=True)
key3_var = tk.BooleanVar(value=True)
key4_var = tk.BooleanVar(value=True)
lclick_var = tk.BooleanVar(value=True)
rclick_var = tk.BooleanVar(value=True)

key1_delay = tk.DoubleVar(value=default_speed)
key2_delay = tk.DoubleVar(value=default_speed)
key3_delay = tk.DoubleVar(value=default_speed)
key4_delay = tk.DoubleVar(value=default_speed)
lclick_delay = tk.DoubleVar(value=default_speed)
rclick_delay = tk.DoubleVar(value=default_speed)

# ---- Rows ----
add_row(2, "1", key1_var, key1_delay)
add_row(3, "2", key2_var, key2_delay)
add_row(4, "3", key3_var, key3_delay)
add_row(5, "4", key4_var, key4_delay)
add_row(6, "좌클릭", lclick_var, lclick_delay)
add_row(7, "우클릭", rclick_var, rclick_delay)

# ---- Cycle ----
ttk.Separator(main).grid(row=8, column=0, columnspan=3, sticky="ew", pady=10)

ttk.Label(main, text="사이클 딜레이 (초)").grid(row=9, column=0, columnspan=2, sticky="e")
cycle_delay = tk.DoubleVar(value=default_speed)
ttk.Entry(main, textvariable=cycle_delay, width=10).grid(row=9, column=2)

# ---- Status ----
status_label = ttk.Label(main, text="● STOPPED", foreground="red", font=("Arial", 10, "bold"))
status_label.grid(row=10, column=0, columnspan=3, pady=10)

ttk.Label(main, text="Pause 키 : 시작 / 중지").grid(row=11, column=0, columnspan=3)

# ================= THREAD =================
threading.Thread(target=macro_loop, daemon=True).start()
threading.Thread(target=pause_listener, daemon=True).start()

# ==== Footer ====
ttk.Label(
    main,
    text="Made by eunhuit",
    font=("Arial", 8),
    foreground="gray"
).grid(row=12, column=0, columnspan=3, pady=(8, 0))

root.mainloop()
