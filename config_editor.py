import tkinter as tk
from tkinter import ttk, messagebox

def setup_config_editor(parent):

    parent.grid_rowconfigure(1, weight=0)
    parent.grid_rowconfigure(4, weight=0)
    parent.grid_columnconfigure(0, weight=0)
    parent.grid_columnconfigure(1, weight=0)
    parent.grid_columnconfigure(2, weight=0)
    parent.grid_columnconfigure(3, weight=0)
    
    def binary_to_hex():
        try:
            result_hex = ''
            for bit_vars in bit_vars_list:
                binary_str = ''.join(var.get() for var in bit_vars)
                if binary_str:
                    hex_value = hex(int(binary_str, 2))[2:].upper().zfill(2)
                    result_hex += hex_value
                else:
                    result_hex += '00'
            hex_result_var.set(result_hex)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def hex_to_binary(hex_str):
        try:
            binary_value = bin(int(hex_str, 16))[2:].zfill(8)
            return binary_value
        except ValueError:
            messagebox.showerror("Error", "Invalid hex input")
            return None

    def convert_to_binary():
        try:
            hex_input = hex_entry.get().strip()
            # 입력이 공백으로 분리된 경우, 공백으로 분할하고, 아니면 2자리 단위로 분할합니다.
            if ' ' in hex_input:
                hex_parts = hex_input.split()
            else:
                hex_parts = [hex_input[i:i+2] for i in range(0, len(hex_input), 2)]
            
            # 각 16진수 문자열을 이진수로 변환
            binary_output = [hex_to_binary(hex_part) for hex_part in hex_parts]
            # 변환된 이진수를 각 비트 변수에 할당
            for i, bits in enumerate(binary_output):
                if i < len(bit_vars_list) and bits:
                    for j in range(8):
                        if j < len(bit_vars_list[i]):
                            bit_vars_list[i][j].set(bits[j])
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")



    def copy_to_clipboard():
        parent.clipboard_clear()
        parent.clipboard_append(hex_result_var.get())
        messagebox.showinfo("Copied", "Result copied to clipboard!")

    main_frame = ttk.Frame(parent, padding="1")
    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    bit_vars_list = []

    # 표 헤더 설정
    ttk.Label(main_frame, text="Byte").grid(column=0, row=0, sticky=tk.W)
    ttk.Label(main_frame, text="StartBit_Bit 0").grid(column=1, row=0, sticky=tk.W, padx=20)
    for i in range(8):
        ttk.Label(main_frame, text=f"Bit {i}").grid(column=i+2, row=0, sticky=tk.W)

    # 입력 필드 생성
    for byte in range(32):
        ttk.Label(main_frame, text=f"{byte}").grid(column=0, row=byte+1, sticky=tk.W)
        ttk.Label(main_frame, text=f"{byte * 8}").grid(column=1, row=byte+1, sticky=tk.W, padx=20)
        bit_vars = []
        for bit in range(8):
            var = tk.StringVar()
            entry = ttk.Entry(main_frame, textvariable=var, width=5)
            entry.grid(column=bit+2, row=byte+1)
            bit_vars.append(var)
        bit_vars_list.append(bit_vars)

    # 별도의 프레임에 Hexadecimal 관련 위젯 추가
    control_frame = ttk.Frame(parent, padding="1")
    control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    ttk.Label(control_frame, text="Enter Hexadecimal:").grid(column=0, row=0, sticky=tk.W)
    hex_entry = ttk.Entry(control_frame, width=38)
    hex_entry.grid(column=1, row=0, columnspan=8, sticky=(tk.W, tk.E))

    hex_result_var = tk.StringVar()
    ttk.Label(control_frame, text="Hexadecimal result:").grid(column=0, row=1, sticky=tk.W)
    hex_result_entry = ttk.Entry(control_frame, textvariable=hex_result_var, width=38)
    hex_result_entry.grid(column=1, row=1, columnspan=7, sticky=(tk.W, tk.E))

    copy_button = ttk.Button(control_frame, text="Copy", command=copy_to_clipboard)
    copy_button.grid(column=8, row=1)

    convert_hex_button = ttk.Button(control_frame, text="binary to Hex", command=binary_to_hex)
    convert_hex_button.grid(column=0, row=2, columnspan=9)
    convert_binary_button = ttk.Button(control_frame, text="Hex to Binary", command=convert_to_binary)
    convert_binary_button.grid(column=0, row=3, columnspan=9)


if __name__ == "__main__":
    parent = tk.Tk()
    parent.title("setup_config_editor")
    setup_config_editor(parent)
    parent.mainloop()