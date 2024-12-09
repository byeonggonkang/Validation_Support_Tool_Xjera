import tkinter as tk
from tkinter import scrolledtext, ttk
import subprocess
import threading
import canExcuteList as sendCan

def main_adbcontroller(parent):
    parent.grid_rowconfigure(1, weight=0)
    parent.grid_rowconfigure(4, weight=0)
    parent.grid_columnconfigure(0, weight=1)
    parent.grid_columnconfigure(1, weight=1)
    parent.grid_columnconfigure(2, weight=1)
    parent.grid_columnconfigure(3, weight=1)

    global log_area
    
    def log_message(message):
        log_area.insert(tk.END, message + '\n')
        log_area.yview(tk.END)
    
    sendCan.set_log_message_callback(log_message)

    def df_useradbcommand(useradbcommand):
        if useradbcommand == "adb shell":
            log_message(f"plese do not input 'adb shell'only")
        else:
            try:
                subprocess.Popen(useradbcommand, shell=True)
                log_message(f" '{useradbcommand}' running cmd.exe")
            except subprocess.CalledProcessError as e:
                log_message("Please Check ADB Connect.")


    def execute_adb_command(commands, description=""):
        try:
            for command in commands:
                subprocess.check_call(command, shell=True)
            if description:
                log_message(f"{description} Success.")
        except subprocess.CalledProcessError as e:
            log_message(f"{description} Error: {e}")
        except subprocess.TimeoutExpired:
            log_message(f"{description} TimeoutExpired.")

    def run_command_in_thread(commands, description=""):
        thread = threading.Thread(target=execute_adb_command, args=(commands, description))
        thread.start()

    def start_scrcpymirror():
        def read_process_output(process):
            for line in process.stdout:
                print(line.strip())
            for line in process.stderr:
                print(line.strip())

        try:
            result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
            output = result.stdout
            if 'List of devices attached' in output:
                device_list = [line for line in output.split('\n')[1:-1] if line.strip() != '']
                device_count = len(device_list)
                if device_count == 0:
                    log_message("Please check the ADB device connection.")
                elif device_count == 1:
                    log_message("ADB Connected. Start Scrcpy")
                    cmd_command = 'scrcpy'
                    process = subprocess.Popen(cmd_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    thread = threading.Thread(target=read_process_output, args=(process,))
                    thread.start()
                elif device_count > 1:
                    log_message("More than one device is connected. Please disconnect one of the devices.")
            else:
                log_message("Please add the ADB path to the environment variables.")
        except subprocess.CalledProcessError as e:
            log_message(f"adb devices command Error: {e}")

    def check_adb_devices():
        try:
            result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
            output = result.stdout
            if 'List of devices attached' in output:
                device_list = [line for line in output.split('\n')[1:-1] if line.strip() != '']
                device_count = len(device_list)
                if device_count == 0:
                    log_message("Please check the ADB device connection.")
                elif device_count == 1:
                    log_message("ADB Connected.")
                elif device_count > 1:
                    log_message("More than one device is connected. Please disconnect one of the devices.")
            else:
                log_message("Failed to execute ADB command.")
        except subprocess.CalledProcessError as e:
            log_message(f"Error occurred during ADB command execution: {e}")
        except FileNotFoundError:
            log_message("ADB command not found. Please ensure that ADB is installed and added to your PATH environment variable.")

    def logcat_MCU():
        try:
            cmd_command = 'start cmd.exe /k "adb logcat -G 100M"'
            cmd_command = 'start cmd.exe /k "adb logcat -s canservice | findstr MCU"'
            subprocess.Popen(cmd_command, shell=True)
        except subprocess.CalledProcessError as e:
            log_message("Please Check ADB Connect.")

    def send_can_messages(messages):
        channel = str(int(channel_entry.get()) - 1)  # 입력 필드에서 channel 값 가져오기
        bustype = bustype_var.get()  # 라디오 버튼에서 선택된 bustype 값 가져오기
        sendCan.send_can_messages(messages, channel, bustype)

    #log_area영역 추가
    log_area = scrolledtext.ScrolledText(parent)
    log_area.grid(row=2, column=0, columnspan=4, sticky='nsew')
    parent.grid_rowconfigure(2, weight=1)

    #cmd shell 대체 영역 추가
    ttk.Label(parent, text="adb command:").grid(column=0, row=0, sticky=tk.W)
    useradbcommnad = ttk.Entry(parent, width=7)
    useradbcommnad.grid(column=1, columnspan=3, row=0, sticky='nsew')
    useradbcommnad.insert(0, 'adb shell input keyevent 4')
    useradbcommnad_button = ttk.Button(parent, text="Send", command=lambda: df_useradbcommand(useradbcommnad.get()))
    useradbcommnad_button.grid(row=0, column=3, sticky='e')

    # can채널 입력 영역 추가
    ttk.Label(parent, text="CAN Channel:").grid(column=3, row=1, sticky=tk.W)
    channel_entry = ttk.Entry(parent, width=7)
    channel_entry.grid(column=3, row=1, sticky=(tk.E))
    channel_entry.insert(0, '1')

    # bustype 라디오 버튼 추가
    bustype_var = tk.StringVar(value='vector')
    vector_radio = ttk.Radiobutton(parent, text="Vector", variable=bustype_var, value='vector')
    kvaser_radio = ttk.Radiobutton(parent, text="Kvaser", variable=bustype_var, value='kvaser')
    vector_radio.grid(column=0, row=1, sticky=tk.W)
    kvaser_radio.grid(column=1, row=1, sticky=tk.W)

    #메뉴선 추가
    ttk.Label(parent, text="ADB Command", font=('Arial', 10, 'bold')).grid(row=3, column=0, columnspan=3, sticky="ew")


    #버튼 배열 생성 및 추가
    adb_buttons = [
        ("ADB device check", check_adb_devices),
        ("Factory Crash", lambda: run_command_in_thread(["adb root", "adb shell am force-stop com.mengbo.factory"], "Factory Crash")),
        ("FactoryMode Enable", lambda: run_command_in_thread(["adb root", "adb shell pm enable com.mengbo.factory"], "FactoryMode Enable")),
        ("FactoryMode Disable", lambda: run_command_in_thread(["adb root", "adb shell pm disable com.mengbo.factory"], "FactoryMode Disable")),
        ("GPS OFF & NaviDataErase", lambda: run_command_in_thread(["adb root", "adb shell settings put secure location_providers_allowed -gps", "adb shell pm clear com.tencent.wecarnavi"], "GPS OFF & NaviDataErase")),
        ("logcat Enable", lambda: run_command_in_thread(["adb root", "adb shell setprop persist.logd.logpersistd.enable true", "adb shell setprop persist.logd.logpersistd logcatd", "adb shell setprop persist.logd.logpersistd.buffer default,kernel,events"], "logcat Enable")),
        ("logcat |grep MCU", logcat_MCU),
        ("USB Mode ADB Disable", lambda: run_command_in_thread(["adb root", "adb shell setprop persist.usb.adbenable 0"], "USB Mode ADB Disable")),
        ("Enter FactoryMode", lambda: run_command_in_thread(["adb root", "adb shell am start -n com.mengbo.factory/com.mengbo.factory.activity.MainActivity"], "Enter FactoryMode")),
        ("adb reboot", lambda: run_command_in_thread(["adb root", "adb reboot"], "adb reboot")),
        ("Screen Mirror", start_scrcpymirror)
    ]

    for i, (text, func) in enumerate(adb_buttons):
        btn = ttk.Button(parent, text=text, command=func)
        btn.grid(row=(i // 4) + 4, column=i % 4, padx=1, pady=1, sticky='nsew')

    #메뉴선 추가
    ttk.Label(parent, text="CAN Command", font=('Arial', 10, 'bold')).grid(row=7, column=0, columnspan=3, sticky="ew")

    CAN_buttons = [
        ("USB Mode ADB Enable", sendCan.diag_usb_Enable),
        ("USB Mode ADB Disable", sendCan.diag_usb_Disable),
        ("Alarm Mode ON", lambda: sendCan.send_alarm_mode_on_off(1)),
        ("Alarm Mode OFF", lambda: sendCan.send_alarm_mode_on_off(0)),
        ("Driver Door Open", lambda: sendCan.send_driver_door_open_close(1)),
        ("Driver Door Close", lambda: sendCan.send_driver_door_open_close(0)),
        ("Key Status ON", lambda: sendCan.send_KeySts_on_off(1)),
        ("Key Status OFF", lambda: sendCan.send_KeySts_on_off(0)),
        ("send_gear_0", lambda: sendCan.send_gear_position(0)),
        ("send_gear_1", lambda: sendCan.send_gear_position(1)),
        ("send_gear_2", lambda: sendCan.send_gear_position(2)),
        ("send_gear_3", lambda: sendCan.send_gear_position(3)),
        ("send_NWM_WAKEUP_0", lambda: sendCan.send_nwm_cgw(0)),
        ("send_NWM_WAKEUP_1", lambda: sendCan.send_nwm_cgw(1)),
        ("send_NWM_WAKEUP_2", lambda: sendCan.send_nwm_cgw(2)),
        ("send_NWM_WAKEUP_3", lambda: sendCan.send_nwm_cgw(3)),
    ]

    for i, (text, func) in enumerate(CAN_buttons):
        btn = ttk.Button(parent, text=text, command=func)
        btn.grid(row=(i // 4) + 8, column=i % 4, padx=1, pady=1, sticky='nsew')

    #메뉴선 추가
    ttk.Label(parent, text="MFS CAN Command", font=('Arial', 10, 'bold')).grid(row=12, column=0, columnspan=2, sticky="ew")

    MCU_Model = tk.StringVar(value='X70')
    x70_radio = ttk.Radiobutton(parent, text="X70", variable=MCU_Model, value='X70')
    x50_radio = ttk.Radiobutton(parent, text="X50", variable=MCU_Model, value='X50')
    x70_radio.grid(column=2, row=12, sticky=tk.W)
    x50_radio.grid(column=3, row=12, sticky=tk.W)

    wechat_button = ttk.Button(parent, text="Wechat Press")
    wechat_button.grid(row=13, column=0, padx=1, pady=1, sticky='nsew')

    menu_button = ttk.Button(parent, text="Menu/User Press")
    menu_button.grid(row=13, column=1, padx=1, pady=1, sticky='nsew')

    left_up_button = ttk.Button(parent, text="LEFT_UP Press")
    left_up_button.grid(row=13, column=2, padx=1, pady=1, sticky='nsew')

    left_down_button = ttk.Button(parent, text="LEFT_DOWN Press")
    left_down_button.grid(row=13, column=3, padx=1, pady=1, sticky='nsew')

    left_left_button = ttk.Button(parent, text="LEFT_LEFT Press")
    left_left_button.grid(row=14, column=0, padx=1, pady=1, sticky='nsew')

    left_right_button = ttk.Button(parent, text="LEFT_RIGHT Press")
    left_right_button.grid(row=14, column=1, padx=1, pady=1, sticky='nsew')

    confirm_button = ttk.Button(parent, text="Confirm/L_OK Press")
    confirm_button.grid(row=14, column=2, padx=1, pady=1, sticky='nsew')

    mute_button = ttk.Button(parent, text="Mute/User Press")
    mute_button.grid(row=14, column=3, padx=1, pady=1, sticky='nsew')

    voice_button = ttk.Button(parent, text="Voice Press")
    voice_button.grid(row=15, column=0, padx=1, pady=1, sticky='nsew')

    voice_add_button = ttk.Button(parent, text="Voice Add Press")
    voice_add_button.grid(row=15, column=1, padx=1, pady=1, sticky='nsew')

    voice_jian_button = ttk.Button(parent, text="Voice Jian Press")
    voice_jian_button.grid(row=15, column=2, padx=1, pady=1, sticky='nsew')

    answer_hangup_button = ttk.Button(parent, text="Phone/R_OK Press")
    answer_hangup_button.grid(row=15, column=3, padx=1, pady=1, sticky='nsew')

    previous_button = ttk.Button(parent, text="Previous Press")
    previous_button.grid(row=16, column=0, padx=1, pady=1, sticky='nsew')

    next_button = ttk.Button(parent, text="Next Press")
    next_button.grid(row=16, column=1, padx=1, pady=1, sticky='nsew')

    def update_bindings():
        if MCU_Model.get() == 'X70':
            menu_button.bind("<ButtonPress-1>", lambda e: threading.Thread(sendCan.send_mfs_menu(1)).start())
            menu_button.bind("<ButtonRelease-1>", lambda e: threading.Thread(sendCan.send_mfs_menu(0)).start())
            wechat_button.bind("<ButtonPress-1>", lambda e: threading.Thread(sendCan.send_mfs_wechat(1)).start())
            wechat_button.bind("<ButtonRelease-1>", lambda e: threading.Thread(sendCan.send_mfs_wechat(0)).start())
            left_up_button.bind("<ButtonPress-1>", lambda e: threading.Thread(sendCan.send_mfs_left_up(1)).start())
            left_up_button.bind("<ButtonRelease-1>", lambda e: threading.Thread(sendCan.send_mfs_left_up(0)).start())
            left_down_button.bind("<ButtonPress-1>", lambda e: threading.Thread(sendCan.send_mfs_left_down(1)).start())
            left_down_button.bind("<ButtonRelease-1>", lambda e: threading.Thread(sendCan.send_mfs_left_down(0)).start())
            left_left_button.bind("<ButtonPress-1>", lambda e: threading.Thread(sendCan.send_mfs_left_left(1)).start())
            left_left_button.bind("<ButtonRelease-1>", lambda e: threading.Thread(sendCan.send_mfs_left_left(0)).start())
            left_right_button.bind("<ButtonPress-1>", lambda e: threading.Thread(sendCan.send_mfs_left_right(1)).start())
            left_right_button.bind("<ButtonRelease-1>", lambda e: threading.Thread(sendCan.send_mfs_left_right(0)).start())
            confirm_button.bind("<ButtonPress-1>", lambda e: threading.Thread(sendCan.send_mfs_confirm(1)).start())
            confirm_button.bind("<ButtonRelease-1>", lambda e: threading.Thread(sendCan.send_mfs_confirm(0)).start())
            mute_button.bind("<ButtonPress-1>", lambda e: threading.Thread(sendCan.send_mfs_mute(1)).start())
            mute_button.bind("<ButtonRelease-1>", lambda e: threading.Thread(sendCan.send_mfs_mute(0)).start())
            voice_button.bind("<ButtonPress-1>", lambda e: threading.Thread(sendCan.send_mfs_voice(1)).start())
            voice_button.bind("<ButtonRelease-1>", lambda e: threading.Thread(sendCan.send_mfs_voice(0)).start())
            voice_add_button.bind("<ButtonPress-1>", lambda e: threading.Thread(sendCan.send_mfs_voice_add(1)).start())
            voice_add_button.bind("<ButtonRelease-1>", lambda e: threading.Thread(sendCan.send_mfs_voice_add(0)).start())
            voice_jian_button.bind("<ButtonPress-1>", lambda e: threading.Thread(sendCan.send_mfs_voice_jian(1)).start())
            voice_jian_button.bind("<ButtonRelease-1>", lambda e: threading.Thread(sendCan.send_mfs_voice_jian(0)).start())
            answer_hangup_button.bind("<ButtonPress-1>", lambda e: threading.Thread(sendCan.send_mfs_answer_hangup_phone(1)).start())
            answer_hangup_button.bind("<ButtonRelease-1>", lambda e: threading.Thread(sendCan.send_mfs_answer_hangup_phone(0)).start())
            previous_button.bind("<ButtonPress-1>", lambda e: threading.Thread(sendCan.send_mfs_previous(1)).start())
            previous_button.bind("<ButtonRelease-1>", lambda e: threading.Thread(sendCan.send_mfs_previous(0)).start())
            next_button.bind("<ButtonPress-1>", lambda e: threading.Thread(sendCan.send_mfs_next(1)).start())
            next_button.bind("<ButtonRelease-1>", lambda e: threading.Thread(sendCan.send_mfs_next(0)).start())
        else:
            menu_button.bind("<ButtonPress-1>", lambda e: threading.Thread(sendCan.send_L_USER_SW(1)).start())
            menu_button.bind("<ButtonRelease-1>", lambda e: threading.Thread(sendCan.send_L_USER_SW(0)).start())
            wechat_button.bind("<ButtonPress-1>", lambda e: threading.Thread(sendCan.send_L_WECHAT_SW(1)).start())
            wechat_button.bind("<ButtonRelease-1>", lambda e: threading.Thread(sendCan.send_L_WECHAT_SW(0)).start())
            left_up_button.bind("<ButtonPress-1>", lambda e: threading.Thread(sendCan.send_L_UP_SW(1)).start())
            left_up_button.bind("<ButtonRelease-1>", lambda e: threading.Thread(sendCan.send_L_UP_SW(0)).start())
            left_down_button.bind("<ButtonPress-1>", lambda e: threading.Thread(sendCan.send_L_DW_SW(1)).start())
            left_down_button.bind("<ButtonRelease-1>", lambda e: threading.Thread(sendCan.send_L_DW_SW(0)).start())
            left_left_button.bind("<ButtonPress-1>", lambda e: threading.Thread(sendCan.send_L_LEFT_SW(1)).start())
            left_left_button.bind("<ButtonRelease-1>", lambda e: threading.Thread(sendCan.send_L_LEFT_SW(0)).start())
            left_right_button.bind("<ButtonPress-1>", lambda e: threading.Thread(sendCan.send_L_RIGHT_SW(1)).start())
            left_right_button.bind("<ButtonRelease-1>", lambda e: threading.Thread(sendCan.send_L_RIGHT_SW(0)).start())
            confirm_button.bind("<ButtonPress-1>", lambda e: threading.Thread(sendCan.send_L_OK_SW(1)).start())
            confirm_button.bind("<ButtonRelease-1>", lambda e: threading.Thread(sendCan.send_L_OK_SW(0)).start())
            mute_button.bind("<ButtonPress-1>", lambda e: threading.Thread(sendCan.send_L_USER_SW(1)).start())
            mute_button.bind("<ButtonRelease-1>", lambda e: threading.Thread(sendCan.send_L_USER_SW(0)).start())
            voice_button.bind("<ButtonPress-1>", lambda e: threading.Thread(sendCan.send_R_SPEECH_SW(1)).start())
            voice_button.bind("<ButtonRelease-1>", lambda e: threading.Thread(sendCan.send_R_SPEECH_SW(0)).start())
            voice_add_button.bind("<ButtonPress-1>", lambda e: threading.Thread(sendCan.send_R_UP_SW(1)).start())
            voice_add_button.bind("<ButtonRelease-1>", lambda e: threading.Thread(sendCan.send_R_UP_SW(0)).start())
            voice_jian_button.bind("<ButtonPress-1>", lambda e: threading.Thread(sendCan.send_R_DW_SW(1)).start())
            voice_jian_button.bind("<ButtonRelease-1>", lambda e: threading.Thread(sendCan.send_R_DW_SW(0)).start())
            answer_hangup_button.bind("<ButtonPress-1>", lambda e: threading.Thread(sendCan.send_R_OK_SW(1)).start())
            answer_hangup_button.bind("<ButtonRelease-1>", lambda e: threading.Thread(sendCan.send_R_OK_SW(0)).start())
            previous_button.bind("<ButtonPress-1>", lambda e: threading.Thread(sendCan.send_R_LEFT_SW(1)).start())
            previous_button.bind("<ButtonRelease-1>", lambda e: threading.Thread(sendCan.send_R_LEFT_SW(0)).start())
            next_button.bind("<ButtonPress-1>", lambda e: threading.Thread(sendCan.send_R_RIGHT_SW(1)).start())
            next_button.bind("<ButtonRelease-1>", lambda e: threading.Thread(sendCan.send_R_RIGHT_SW(0)).start())

    MCU_Model.trace_add("write", lambda *args: update_bindings())

    # 초기 실행 시 MFS 버튼의 bind 설정
    update_bindings()

    sendCan.set_send_can_messages_callback(send_can_messages)

if __name__ == "__main__":
    parent = tk.Tk()
    parent.title("ADB Controller")
    main_adbcontroller(parent)
    parent.mainloop()
