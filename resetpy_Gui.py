import tkinter as tk
from tkinter import scrolledtext
import threading
import pyautogui
import time

# 글로벌 변수로 실행 중 상태 및 스레드 관리
running = False
current_thread = None

def perform_sequence(delay, log_widget):
    # for _ in range(3):
    #     if not running:
    #         return
    #     pyautogui.press('enter')
    #     time.sleep(0.1)
    pyautogui.press('enter')
    pyautogui.write('reset')
    pyautogui.press('enter')
    log_widget.insert(tk.END, f"Reset command sent after {delay} seconds delay.\n")
    log_widget.yview(tk.END)
    time.sleep(0.1)

def start_sequence(initial_delay, repeat_count, increment, log_widget):
    global running
    running = True
    initial_delay = float(initial_delay)
    repeat_count = int(repeat_count)
    increment = float(increment)

    log_widget.insert(tk.END, "Starting sequence in 10 seconds...\n")
    log_widget.yview(tk.END)
    time.sleep(10)

    while running:
        for i in range(repeat_count):
            if not running:
                break
            current_delay = initial_delay + i * increment
            perform_sequence(current_delay, log_widget)
            time.sleep(current_delay)

        if running:
            log_widget.insert(tk.END, f"{repeat_count} cycles completed. Resetting initial delay...\n")
        else:
            log_widget.insert(tk.END, "Sequence stopped.\n")
        log_widget.yview(tk.END)

def on_start(initial_delay, repeat_count, increment, log_widget):
    global running, current_thread
    if running:
        on_stop()
        if current_thread is not None:
            current_thread.join()  # Ensure the thread has stopped before starting a new one

    current_thread = threading.Thread(target=start_sequence, args=(initial_delay, repeat_count, increment, log_widget))
    current_thread.daemon = True
    current_thread.start()

def on_stop():
    global running
    running = False

# GUI setup
window = tk.Tk()
window.title("Automation Reset Control Panel_Xjera")
window.geometry('530x230')  # Set window size

# Input for initial_delay
tk.Label(window, text="Initial Delay (seconds):").grid(row=0, column=0)
initial_delay_entry = tk.Entry(window, width=20)
initial_delay_entry.grid(row=0, column=1)
initial_delay_entry.insert(0, "0.1")

# Input for repeat_count
tk.Label(window, text="Repeat Count:").grid(row=1, column=0)
repeat_count_entry = tk.Entry(window, width=20)
repeat_count_entry.grid(row=1, column=1)
repeat_count_entry.insert(0, "50")

# Input for increment
tk.Label(window, text="Delay Increment (seconds):").grid(row=2, column=0)
increment_entry = tk.Entry(window, width=20)
increment_entry.grid(row=2, column=1)
increment_entry.insert(0, "0.1")

# Console log area
log_area = scrolledtext.ScrolledText(window, width=70, height=10)
log_area.grid(row=3, column=0, columnspan=2)

# Start and Stop buttons
start_button = tk.Button(window, text="Start Sequence", command=lambda: on_start(initial_delay_entry.get(), repeat_count_entry.get(), increment_entry.get(), log_area))
start_button.grid(row=4, column=0)
stop_button = tk.Button(window, text="Stop Sequence", command=on_stop)
stop_button.grid(row=4, column=1)

# Version label
version_label = tk.Label(window, text="V2.0", font=("Arial", 8))
version_label.grid(row=4, column=1, sticky=tk.E)  # Align to the right

window.mainloop()
