import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox

def main_checksum_calculator(parent):

    parent.grid_rowconfigure(1, weight=0)
    parent.grid_rowconfigure(4, weight=0)
    parent.grid_columnconfigure(0, weight=0)
    parent.grid_columnconfigure(1, weight=0)
    parent.grid_columnconfigure(2, weight=0)
    parent.grid_columnconfigure(3, weight=0)

    def log_message(message):
        log_area.insert(tk.END, message + '\n')
        log_area.yview(tk.END)
    
    def calculate_checksum():
        try:
            data = list(map(lambda x: int(x, 16), data_entry.get().replace(',', ' ').split()))
            checksum_location = int(checksum_location_entry.get())
            if checksum_location < 0 or checksum_location >= len(data):
                log_message("Checksum location is out of data range.")
                return
            
            checksum = 0
            total_sum = 0
            
            for idx, byte in enumerate(data):
                if idx != checksum_location:
                    checksum += byte
                    total_sum += byte
            
            checksum &= 0xFF
            checksum ^= 0xFF
            
            log_message(f"Total sum of bytes excluding checksum: 0x{total_sum:X}")
            log_message(f"Calculated Checksum: 0x{checksum:X}")
        except Exception as e:
            log_message(f"Error: {str(e)}")
    
    # GUI setup
    log_area = scrolledtext.ScrolledText(parent, height=3, width=53)
    log_area.grid(row=0, column=0, columnspan=2, pady=(0, 10))

    ttk.Label(parent, text="Enter data bytes (e.g., 11 06 50 02 or 0x11 0x06 0x50 0x02):").grid(row=1, column=0, columnspan=2)
    data_entry = ttk.Entry(parent, width=53)
    data_entry.grid(row=2, column=0, columnspan=2, pady=(0, 5))
    
    ttk.Label(parent, text="Enter checksum location (e.g., 6 ... (0~) ):").grid(row=3, column=0, columnspan=2)
    checksum_location_entry = ttk.Entry(parent, width=53)
    checksum_location_entry.grid(row=4, column=0, columnspan=2, pady=(0, 5))
    
    calculate_button = ttk.Button(parent, text="Calculate Checksum", command=calculate_checksum)
    calculate_button.grid(row=5, column=0, columnspan=2, pady=10)

if __name__ == "__main__":
    parent = tk.Tk()
    parent.title("main_checksum_calculator")
    main_checksum_calculator(parent)
    parent.mainloop()