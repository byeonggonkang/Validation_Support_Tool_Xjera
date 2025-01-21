import subprocess
import tkinter as tk
from tkinter import Menu, messagebox, scrolledtext, PhotoImage
import sys
import os
import requests
import gittoken
import updatemanager

class TextRedirector(object):
    def __init__(self, widget):
        self.widget = widget

    def write(self, str):
        self.widget.config(state=tk.NORMAL)
        self.widget.insert(tk.END, str)
        self.widget.see(tk.END)
        self.widget.config(state=tk.DISABLED)

    def flush(self):
        pass

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        icon_path = self.resource_path("xjeraEasyTool.ico")
        try:
            self.iconbitmap(icon_path)
        except tk.TclError:
            print(f"Warning: '{icon_path}' not found. Icon will not be set.")
        print("본 창을 끄시면 프로그램이 꺼집니다.")
        print("If you close this window, the program will close.")
        print("如果关闭此窗口，程序将关闭。")
        self.debug_log_window = None
        self.title(f"Validation Support Tool_Xjera {updatemanager.CURRENT_VERSION}")
        self.geometry("700x800+0+0")
        self.check_updates_on_startup()  # 시작시 업데이트 확인

        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.setup_menu()

        self.load_adbcontrol_gui()
        self.image1 = self.load_image("manual1_adb.png")
        self.image2 = self.load_image("autoreset.png")
        self.image3 = self.load_image("monkey.png")
        
    def check_updates_on_startup(self):
        self.after(1000, updatemanager.check_for_updates)

    def send_github_issue(self, issue_title, issue_body):
        github_token = gittoken.token
        github_repo = gittoken.repo

        """GitHub Issue 전송"""
        # 입력 필드가 비어있는지 확인
        if not issue_title.strip() or not issue_body.strip():
            messagebox.showwarning("Warning", "Please fill in both the title and description.")
            return

        # GitHub Issue 생성 API 호출
        try:
            headers = {
                "Authorization": f"token {github_token}",
                "Accept": "application/vnd.github.v3+json"
            }
            data = {
                "title": issue_title,
                "body": issue_body
            }
            url = f"https://api.github.com/repos/{github_repo}/issues"
            response = requests.post(url, headers=headers, json=data)

            if response.status_code == 201:
                messagebox.showinfo("Success", "Your issue has been submitted!")
            else:
                messagebox.showerror("Error", f"Failed to submit the issue.\n{response.json().get('message', 'Unknown error')}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def send_github_issue_dialog(self):
        issue_dialog = tk.Toplevel(self)
        issue_dialog.title("Send Issue & Suggestion")
        tk.Label(issue_dialog, text="Issue Title:").pack(pady=5)
        issue_title_entry = tk.Entry(issue_dialog, width=50)
        issue_title_entry.pack(pady=5)

        tk.Label(issue_dialog, text="Issue Description:").pack(pady=5)
        issue_body_entry = tk.Text(issue_dialog, width=50, height=10)
        issue_body_entry.pack(pady=5)

        def send_issue():
            issue_title = issue_title_entry.get()
            issue_body = issue_body_entry.get("1.0", tk.END)
            self.send_github_issue(issue_title, issue_body)
            issue_dialog.destroy()

        def cancel():
            issue_dialog.destroy()

        tk.Button(issue_dialog, text="Send", command=send_issue).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(issue_dialog, text="Cancel", command=cancel).pack(side=tk.RIGHT, padx=10, pady=10)


    def resource_path(self, relative_path):
        """ PyInstaller로 패키징된 실행 파일 내부 리소스 경로 설정 """
        try:
            # PyInstaller로 빌드된 실행 파일 내부일 때 경로 설정
            base_path = sys._MEIPASS
        except AttributeError:
            # 일반 실행 환경에서 경로 설정
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def load_image(self, filename):
        script_dir = os.path.dirname(__file__)
        image_path = os.path.join(script_dir, filename)
        return PhotoImage(file=image_path)

    def setup_menu(self):
        menu_bar = Menu(self)
        self.config(menu=menu_bar)

        file_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Load ADBcontroller", command=self.load_adbcontrol_gui)
        file_menu.add_command(label="Load UartAnalyzer", command=self.load_UartAnalyzer)
        file_menu.add_command(label="Load MonkeyTest", command=self.load_monkey_gui)
        file_menu.add_command(label="Load Autoreset", command=self.load_autoreset_gui)
        file_menu.add_command(label="Load ChecksumCalculator", command=self.load_checksum_calculator_gui)
        file_menu.add_command(label="Load Config Editor", command=self.load_config_editor)
        topmost_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Options", menu=topmost_menu)
        self.topmost_var = tk.BooleanVar()
        topmost_menu.add_checkbutton(label="항상 위", onvalue=True, offvalue=False, variable=self.topmost_var, command=self.toggle_topmost)
        topmost_menu.add_command(label="DebugLog", command=self.show_log_window)

        info_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Info", menu=info_menu)
        info_menu.add_command(label="Version History", command=self.show_version_history)
        menu_bar.add_command(label="Manual", command=self.show_manual)
        menu_bar.add_command(label="Send Issue & Suggest", command=self.send_github_issue_dialog)

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def set_window_geometry(self, width, height):
        self.geometry(f"{width}x{height}")

    def show_log_window(self):
        if not self.debug_log_window:
            self.debug_log_window = tk.Toplevel(self)
            self.debug_log_window.title("로그 보기")
            self.debug_log_window.geometry("500x400")

            log_text = scrolledtext.ScrolledText(self.debug_log_window, wrap=tk.WORD)
            log_text.pack(fill=tk.BOTH, expand=True)

            sys.stdout = TextRedirector(log_text)

            self.debug_log_window.protocol("WM_DELETE_WINDOW", self.close_debug_log_window)
        else:
            self.debug_log_window.lift()

    def close_debug_log_window(self):
        sys.stdout = sys.__stdout__
        self.debug_log_window.destroy()
        self.debug_log_window = None

    def load_config_editor(self):
        self.clear_main_frame()
        self.set_window_geometry(490, 800)
        import config_editor
        config_editor.setup_config_editor(self.main_frame)

    def load_autoreset_gui(self):
        self.clear_main_frame()
        self.set_window_geometry(550, 250)
        import autoreset
        autoreset.main_autoreset(self.main_frame)

    def load_monkey_gui(self):
        self.clear_main_frame()
        self.set_window_geometry(510, 380)
        import monkeytest
        monkeytest.main_monkey(self.main_frame)

    def load_adbcontrol_gui(self):
        self.clear_main_frame()
        self.set_window_geometry(585, 480)
        import adb_control
        adb_control.main_adbcontroller(self.main_frame)

    def load_checksum_calculator_gui(self):
        self.clear_main_frame()
        self.set_window_geometry(400, 200)
        import checksum_calculator
        checksum_calculator.main_checksum_calculator(self.main_frame)

    def load_UartAnalyzer(self):
        self.clear_main_frame()
        self.set_window_geometry(860, 550)
        import UartAnalyzer
        UartAnalyzer.main_UartAnalyzer(self.main_frame)

    def toggle_topmost(self):
        is_topmost = self.attributes('-topmost')
        self.attributes('-topmost', not is_topmost)

    def show_version_history(self):
        version_info = """

        Version v1.0.1:
        - Add the function of Screen Mirror Loop

        Version v1.0.0:
        - Initial release.

        Version 7.0:
        - adb controller -- canMessageSend 기능 추가

        Version 6.0:
        - CAN Device : "Vector, Kvser" 선택 기능 추가

        Version 5.0:
        - UartAnalyzer 멈춤현상 개선

        Version 4.0:
        - UartAnalyze 기능 추가 (MCU Record: , Send to MCU: )
        - adb controller -- adb shell command 기능 추가

        Version 3.0:
        - adb controller - ScreenMirror 기능 추가
        - diag import module
        
        Version 2.0:
        - checksum_calculator 기능 추가 (x50)
        - adb controller 창사이즈 축소
        - adb controller candiag_usbEnable 동작 추가 
            (우상단 채널 명 입력 Vector사)
        
        Version 1.0:
        - Initial release.
        - autoreset 기능
        - config editor 기능 추가
        - monkey 기능 추가
        - adb controller 기능 추가

        Created.by byeonggon.kang
        """
        messagebox.showinfo("Version History", version_info)

    def show_manual(self):
        manual_window = tk.Toplevel(self)
        manual_window.title("Manual")

        # Set manual window size
        window_width = self.winfo_screenwidth() - 200
        window_height = self.winfo_screenheight() - 200

        # Create canvas with scrollbars
        canvas = tk.Canvas(manual_window, width=window_width, height=window_height)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        vscrollbar = tk.Scrollbar(manual_window, orient=tk.VERTICAL, command=canvas.yview)
        vscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.configure(yscrollcommand=vscrollbar.set)

        hscrollbar = tk.Scrollbar(manual_window, orient=tk.HORIZONTAL, command=canvas.xview)
        hscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        canvas.configure(xscrollcommand=hscrollbar.set)

        # Create a frame inside the canvas to hold the manual content
        manual_frame = tk.Frame(canvas)
        manual_frame.bind("<Configure>", lambda event, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=manual_frame, anchor="nw")

        # Add image labels
        image_label1 = tk.Label(manual_frame, image=self.image1)
        image_label1.pack(fill=tk.BOTH, expand=True)

        image_label2 = tk.Label(manual_frame, image=self.image2)
        image_label2.pack(fill=tk.BOTH, expand=True)

        image_label3 = tk.Label(manual_frame, image=self.image3)
        image_label3.pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    app = App()
    app.mainloop()
