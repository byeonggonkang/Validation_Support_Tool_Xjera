import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox
import threading
import pyautogui
import time

def main_autoreset(parent):

    parent.grid_rowconfigure(1, weight=0)
    parent.grid_rowconfigure(4, weight=0)
    parent.grid_columnconfigure(0, weight=0)
    parent.grid_columnconfigure(1, weight=0)
    parent.grid_columnconfigure(2, weight=0)
    parent.grid_columnconfigure(3, weight=0)
    
    global running, log_area, start_button, stop_button

    running = False


    def perform_sequence(delay):
        time.sleep(delay)  # 시퀀스 시작 전 지연
        # pyautogui를 사용한 키 입력 시뮬레이션
        pyautogui.press('enter')
        command = command_entry.get()
        pyautogui.write(command)
        pyautogui.press('enter')
        log_area.insert(tk.END, f" '{command}' command sent after {delay} seconds delay.\n")
        log_area.yview(tk.END)

    def start_sequence(initial_delay, repeat_count, increment):
        global running
        running = True
        try:
            initial_delay = float(initial_delay)
            repeat_count = int(repeat_count)
            increment = float(increment)

            for i in range(repeat_count):
                if not running:
                    break
                current_delay = initial_delay + i * increment
                # perform_sequence 함수를 별도의 스레드에서 실행
                threading.Thread(target=perform_sequence, args=(current_delay,)).start()
                time.sleep(current_delay)  # 메인 스레드에서의 지연을 위해

            if running:
                log_area.insert(tk.END, f"{repeat_count} cycles completed. Resetting initial delay...\n")
            else:
                log_area.insert(tk.END, "Sequence stopped.\n")
            log_area.yview(tk.END)

        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def on_start():
        global running
        if running:
            on_stop()
        else:
            # start_sequence를 별도의 스레드에서 실행
            threading.Thread(target=start_sequence, args=(
                initial_delay_entry.get(),
                repeat_count_entry.get(),
                increment_entry.get(),
            )).start()

    def on_stop():
        global running
        running = False
        log_area.insert(tk.END, "Sequence stopped by user.\n")
        log_area.yview(tk.END)

    # GUI setup

    command_label = ttk.Label(parent, text="Command:")
    command_label.grid(row=0, column=0)
    
    command_entry = ttk.Entry(parent, width=20)
    command_entry.grid(row=0,column=1)
    command_entry.insert(0, "reset")

    initial_delay_label = ttk.Label(parent, text="Initial Delay (seconds):")
    initial_delay_label.grid(row=1, column=0)

    initial_delay_entry = ttk.Entry(parent, width=20)
    initial_delay_entry.grid(row=1, column=1)
    initial_delay_entry.insert(0, "0.5")

    repeat_count_label = ttk.Label(parent, text="Repeat Count:")
    repeat_count_label.grid(row=2, column=0)

    repeat_count_entry = ttk.Entry(parent, width=20)
    repeat_count_entry.grid(row=2, column=1)
    repeat_count_entry.insert(0, "20")

    increment_label = ttk.Label(parent, text="Delay Increment (seconds):")
    increment_label.grid(row=3, column=0)

    increment_entry = ttk.Entry(parent, width=20)
    increment_entry.grid(row=3, column=1)
    increment_entry.insert(0, "0.5")

    log_area = scrolledtext.ScrolledText(parent, width=70, height=10)
    log_area.grid(row=4, column=0, columnspan=2)

    start_button = ttk.Button(parent, text="Start Sequence", command=on_start)
    start_button.grid(row=5, column=0)

    stop_button = ttk.Button(parent, text="Stop Sequence", command=on_stop)
    stop_button.grid(row=5, column=1)

if __name__ == "__main__":
    parent = tk.Tk()
    parent.title("main_autoreset")
    main_autoreset(parent)
    parent.mainloop()
