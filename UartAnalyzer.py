import tkinter as tk
from tkinter import scrolledtext, ttk, font
import subprocess
import re
import threading
import time
import queue
import atexit

def main_UartAnalyzer(parent):
    parent.grid_rowconfigure(1, weight=1)
    parent.grid_rowconfigure(4, weight=1)
    parent.grid_columnconfigure(0, weight=1)
    parent.grid_columnconfigure(1, weight=1)
    parent.grid_columnconfigure(2, weight=0)
    parent.grid_columnconfigure(3, weight=0)
    
    logcat_status = None
    show_all_bytes = False  # 전체보기 상태를 나타내는 변수 추가
    log_queue = queue.Queue()

    def Tx_log_message(message):
        if Tx_log_area.winfo_exists():
            Tx_log_area.insert(tk.END, message + '\n')
            Tx_log_area.yview(tk.END)

    def Rx_log_message(message):
        if Rx_log_area.winfo_exists():
            Rx_log_area.insert(tk.END, message + '\n')
            Rx_log_area.yview(tk.END)

    def clear_logcat_buffer():
        subprocess.run(['adb', 'logcat', '-c'], creationflags=subprocess.CREATE_NO_WINDOW)

    def clear_logs():
        if Tx_log_area.winfo_exists() and Rx_log_area.winfo_exists():
            Tx_log_area.delete('1.0', tk.END)
            Rx_log_area.delete('1.0', tk.END)

    def toggle_show_all_bytes():
        nonlocal show_all_bytes
        show_all_bytes = not show_all_bytes
        if show_all_bytes:
            show_all_button.config(text="Length, MessageID (현상태 : 표시)")
        else:
            show_all_button.config(text="Length, MessageID (현상태 : 감추기)")
            
    def on_exit():
        if logcat_status:
            logcat_status.terminate()
        
    def read_logcat():
        clear_logcat_buffer()
        nonlocal logcat_status
        max_retries = 9999
        retry_delay = 5
        attempts = 0
        while attempts < max_retries:
            try:
                logcat_status = subprocess.Popen(['adb', 'logcat', '-s', 'canservice', '|', 'findstr', 'MCU'], stdout=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
                log_queue.put(("Rx", "연결되었습니다."))
                log_queue.put(("Tx", "연결되었습니다."))
                while True:
                    line = logcat_status.stdout.readline().decode('utf-8', errors='replace').strip()
                    if line:
                        log_queue.put(("log", line))
                        findcaservice(line)
            except (subprocess.SubprocessError, OSError) as e:
                attempts += 1
                if attempts < max_retries:
                    time.sleep(retry_delay)
                    log_queue.put(("Rx", "연결중입니다.."))
                    log_queue.put(("Tx", "연결중입니다.."))
                else:
                    break

    def findcaservice(line):
        pattern_send = re.compile(r'canservice(.*)')
        match_send = pattern_send.search(line)
        if match_send:
            byte_string = match_send.group(1)
            if "MCU Record" in byte_string:
                byte_list = byte_string.split(' ')
                print("MCU", ' '.join(byte_list[3:]))
            elif "MCU" in byte_string:
                byte_list = byte_string.split(' ')
                # 3번째 배열부터 프린트
                print(' '.join(byte_list[3:]))

    def parse_logcat_line(line):
        pattern_send = re.compile(r'Send To MCU: (.*)')
        match_send = pattern_send.search(line)
        if match_send:
            byte_string = match_send.group(1)
            byte_list = byte_string.split(',')
            if show_all_bytes:
                if byte_list[4] != '0xaa':
                    byte_string = '\t'.join(byte_list)
                    log_queue.put(("Rx", byte_string))
            else:
                if byte_list[4] != '0xaa':
                    relevant_bytes = [byte_list[0], byte_list[1], byte_list[4]]
                    relevant_bytes.extend(byte_list[7:])
                    byte_string = '\t'.join(relevant_bytes)
                    log_queue.put(("Rx", byte_string))
        
        pattern_record = re.compile(r'MCU Record: (.*)')
        match_record = pattern_record.search(line)
        if match_record:
            record_string = match_record.group(1)
            Tx_byte_list = record_string.split(',')
            if show_all_bytes:
                record_string = '\t'.join(Tx_byte_list)
                log_queue.put(("Tx", record_string))
            else:
                relevant_bytes = [Tx_byte_list[0], Tx_byte_list[1], Tx_byte_list[4]]
                relevant_bytes.extend(Tx_byte_list[7:])
                record_string = '\t'.join(relevant_bytes)
                log_queue.put(("Tx", record_string))

    style = ttk.Style()
    style.configure("Bold.TLabel", font=(None, 12, 'bold'))
    
    ttk.Label(parent, text="Send To MCU: ", style="Bold.TLabel").grid(row=0, column=0, columnspan=2)
    Rx_log_area = scrolledtext.ScrolledText(parent, width=120, height=20)
    Rx_log_area.grid(row=1, column=0, columnspan=2, sticky='nsew')
    Rx_log_area.tag_config("fourth_byte", foreground="blue")

    ttk.Label(parent, text="MCU Record: ", style="Bold.TLabel").grid(row=3, column=0, columnspan=2)
    Tx_log_area = scrolledtext.ScrolledText(parent, width=120, height=20)
    Tx_log_area.grid(row=4, column=0, columnspan=2, sticky='nsew')
    Tx_log_area.tag_config("fourth_byte", foreground="blue")

    clear_button = ttk.Button(parent, text="CLEAR", command=clear_logs)
    clear_button.grid(row=0, column=1, sticky='e')

    show_all_button = ttk.Button(parent, text="Length, MessageID (현상태 : 감추기)", command=toggle_show_all_bytes)
    show_all_button.grid(row=0, column=0, columnspan=2, pady=1, sticky='w')
    
    def process_log_queue():
        while not log_queue.empty():
            try:
                log_type, message = log_queue.get_nowait()
                if log_type == "Rx":
                    Rx_log_message(message)
                elif log_type == "Tx":
                    Tx_log_message(message)
                elif log_type == "log":
                    parse_logcat_line(message)
            except queue.Empty:
                break
        parent.after(100, process_log_queue)

    parent.after(100, process_log_queue)

    log_thread = threading.Thread(target=read_logcat)
    log_thread.daemon = True
    log_thread.start()

    atexit.register(on_exit)

if __name__ == "__main__":
    parent = tk.Tk()
    parent.title("Uart Analyzer")
    main_UartAnalyzer(parent)
    parent.mainloop()
