from datetime import datetime
import tkinter as tk
from tkinter import scrolledtext, ttk
import threading
import subprocess
import os
import time

def main_monkey(parent):

    parent.grid_rowconfigure(1, weight=0)
    parent.grid_rowconfigure(4, weight=0)
    parent.grid_columnconfigure(0, weight=0)
    parent.grid_columnconfigure(1, weight=0)
    parent.grid_columnconfigure(2, weight=0)
    parent.grid_columnconfigure(3, weight=0)

    global running, log_area, monkey_pid, log_process
    running = False
    monkey_pid = None
    log_process = None

    # 파일에 기록할 패키지 목록
    packages = [
        "com.mengbo.factory", "com.mengbo.carota", "com.android.settings",
        "com.mengbo.systemsettings", "com.mengbo.avm", "com.mengbo.statistic",
        "io.appium.settings", "com.he.ardc", "com.autopai.wtservice",
        "com.autopai.wttboxservice", "com.tencent.wecarspeech.gaodeagent",
        "com.android.phone", "com.wt.stability.monitor",
        "com.google.android.car.vms.subscriber", "com.android.car.settings",
        "com.chery.carsettings"
    ]

    # 임시 파일에 패키지 목록 쓰기
    temp_dir = os.getenv('TEMP')
    temp_file_path = os.path.join(temp_dir, "black.txt")
    with open(temp_file_path, "w") as temp_file:
        for package in packages:
            temp_file.write(package + "\n")

    # 생성된 파일을 adb를 통해 Android 장치로 덮어쓰기
    try:
        subprocess.run(f"adb push {temp_file_path} /sdcard/black.txt", shell=True, check=True)
    except subprocess.CalledProcessError:
        log_message("Failed to push black.txt to the device.")

    def log_message(message):
        log_area.insert(tk.END, message + '\n')
        log_area.yview(tk.END)

    def create_log_file():
        current_time = datetime.now()
        filename = current_time.strftime("%H-%M-%S")
        log_folder = os.path.expanduser("~/Desktop/monkey")
        if not os.path.exists(log_folder):
            os.makedirs(log_folder)
        return os.path.join(log_folder, filename + "_1.txt")

    def adb_check():
        try:
            subprocess.check_call("adb root", shell=True)
            log_message("ADB connected successfully. The monkey test will start in 5 seconds.")
            return True
        except subprocess.CalledProcessError:
            # log_message("ADB connection failed. Please check the device connection.")
            return False

    def adb_logcat(log_file):
        global log_process
        cmd = f"adb logcat -v time >> {log_file} 2>&1"
        log_process = subprocess.Popen(cmd, shell=True)

    def get_monkey_pid():
        global monkey_pid
        try:
            result = subprocess.check_output("adb shell ps | findstr com.android.commands.monkey", shell=True, text=True)
            if result:
                monkey_pid = result.split()[1]
                log_message(f"Monkey PID is {monkey_pid}")
        except subprocess.CalledProcessError as e:
            log_message(f"Failed to retrieve monkey PID: {str(e)}")

    def monkey_run(log_file):
        global running, log_process, monkey_pid
        if not adb_check():  # ADB 점검
            log_message("ADB connection failed. Please check the device connection.")
            running = False
            return  # ADB 점검 실패시 함수 종료

        # 로그 프로세스 시작
        adb_logcat(log_file)

        # 명령 실행 전 대기
        time.sleep(5)  # SOC 안정화 대기 시간

        # 기존 실행 중인 앱 종료 및 화면 조정
        subprocess.run("adb shell am force-stop com.mengbo.factory", shell=True)
        subprocess.run("adb shell wm overscan 0,0,0,0", shell=True)

        # Monkey 명령 실행
        cmd = ("adb shell monkey --pct-syskeys 0 --pkg-blacklist-file /sdcard/black.txt "
            "--throttle 300 --ignore-crashes --ignore-timeouts --monitor-native-crashes "
            "--ignore-security-exceptions --ignore-native-crashes -v 111111111")
        subprocess.Popen(cmd, shell=True, text=True)
        time.sleep(5)
        # Monkey 프로세스 실행 확인 및 PID 획득
        get_monkey_pid()
        running = True        

    def start_test():
        global running
        if not running:
            log_file = create_log_file()
            log_message("Starting monkey test...")
            threading.Thread(target=monkey_run, args=(log_file,)).start()
        else:
            log_message("Test is already running.")

    def stop_test():
        global running, monkey_pid, log_process
        if running:
            if monkey_pid:
                # Monkey 프로세스 종료
                subprocess.run(f"adb shell kill -9 {monkey_pid}", shell=True)
                log_message(f"Monkey test stopped. Monkey PID {monkey_pid} has been terminated.")
                monkey_pid = None
            if log_process:
                # log_process와 모든 자식 프로세스를 강제 종료
                try:
                    subprocess.run(f"taskkill /F /PID {log_process.pid} /T", shell=True)
                    # log_message("Log capture process and all child processes terminated successfully.")
                except Exception as e:
                    log_message(f"Failed to terminate log capture process: {str(e)}")
                finally:
                    log_process = None
            running = False
        else:
            log_message("No running test or monkey PID is not available.")


    # GUI setup within parent frame
    log_area = scrolledtext.ScrolledText(parent, height=20, width=80)
    log_area.pack(pady=20)

    start_btn = ttk.Button(parent, text="Start Test", command=start_test)
    start_btn.pack()

    stop_btn = ttk.Button(parent, text="Stop Test", command=stop_test)
    stop_btn.pack()