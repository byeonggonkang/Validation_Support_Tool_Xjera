import can  # python-can
import CAN_Contents
import adb_control as madb
import time 

send_can_messages_callback = None
log_message_callback = None

def set_send_can_messages_callback(callback):
    global send_can_messages_callback
    send_can_messages_callback = callback

def set_log_message_callback(callback):
    global log_message_callback
    log_message_callback = callback

def send_can_messages(messages, channel, bustype):
    try:
        bus = can.interface.Bus(channel=channel, bustype=bustype, app_name='CANoe', bit_rate=500000)
        for msg in messages:
            bus.send(msg)
            print(msg)
            time.sleep(0.01)
        if log_message_callback:
            log_message_callback(f"Message sent successfully")
    except can.CanError as e:
        if log_message_callback:
            log_message_callback(f"CAN Error: {e}")
    except ValueError as e:
        if log_message_callback:
            log_message_callback(f"Invalid channel number: {e}")
    finally:
        if 'bus' in locals():
            bus.shutdown()

################################## diagnostics
def diag_usb_Enable():
    messages = [
        can.Message(arbitration_id=CAN_Contents.diag_req_id, data=CAN_Contents.diagExtendedSession, is_extended_id=False),
        can.Message(arbitration_id=CAN_Contents.diag_req_id, data=CAN_Contents.diagkeyReq, is_extended_id=False),
        can.Message(arbitration_id=CAN_Contents.diag_req_id, data=CAN_Contents.diagkeysend, is_extended_id=False),
        can.Message(arbitration_id=CAN_Contents.diag_req_id, data=CAN_Contents.diagusbEnable, is_extended_id=False)
    ]
    if send_can_messages_callback:
        send_can_messages_callback(messages)

def diag_usb_Disable():
    messages = [
        can.Message(arbitration_id=CAN_Contents.diag_req_id, data=CAN_Contents.diagExtendedSession, is_extended_id=False),
        can.Message(arbitration_id=CAN_Contents.diag_req_id, data=CAN_Contents.diagkeyReq, is_extended_id=False),
        can.Message(arbitration_id=CAN_Contents.diag_req_id, data=CAN_Contents.diagkeysend, is_extended_id=False),
        can.Message(arbitration_id=CAN_Contents.diag_req_id, data=CAN_Contents.diagusbDisable, is_extended_id=False)
    ]
    if send_can_messages_callback:
        send_can_messages_callback(messages)

def send_ExtdSession():
    messages = [
            can.Message(arbitration_id=CAN_Contents.diag_req_id, data=CAN_Contents.diagExtendedSession, is_extended_id=False)
        ]
    if send_can_messages_callback:
            send_can_messages_callback(messages)

def send_keyReq():
    messages = [
        can.Message(arbitration_id=CAN_Contents.diag_req_id, data=CAN_Contents.diagkeyReq, is_extended_id=False)
    ]
    if send_can_messages_callback:
        send_can_messages_callback(messages)

def send_keysend():
    messages = [
        can.Message(arbitration_id=CAN_Contents.diag_req_id, data=CAN_Contents.diagkeysend, is_extended_id=False)
    ]
    if send_can_messages_callback:
        send_can_messages_callback(messages)

def send_configwrite():
    messages = [
        can.Message(arbitration_id=CAN_Contents.diag_req_id, data=CAN_Contents.diagconfigwrite, is_extended_id=False)
    ]
    if send_can_messages_callback:
        send_can_messages_callback(messages)

def send_vinwrite():
    messages = [
        can.Message(arbitration_id=CAN_Contents.diag_req_id, data=CAN_Contents.diagVinwrite, is_extended_id=False)
    ]
    if send_can_messages_callback:
        send_can_messages_callback(messages)

def send_reset():
    messages = [
        can.Message(arbitration_id=CAN_Contents.diag_req_id, data=CAN_Contents.diagreset, is_extended_id=False)
    ]
    if send_can_messages_callback:
        send_can_messages_callback(messages)

################################## #CGW_TCU_G

def send_gear_position(position):
    gear_positions = {
        0: CAN_Contents.Gear_0,
        1: CAN_Contents.Gear_1,
        2: CAN_Contents.Gear_2,
        3: CAN_Contents.Gear_3,
        4: CAN_Contents.Gear_4,
        5: CAN_Contents.Gear_5,
        6: CAN_Contents.Gear_6,
        7: CAN_Contents.Gear_7,
        8: CAN_Contents.Gear_8
    }
    if position in gear_positions:
        message = can.Message(arbitration_id=CAN_Contents.CGW_TCU_G, data=gear_positions[position], is_extended_id=False)
        if send_can_messages_callback:
            send_can_messages_callback([message])
    else:
        print(f"Invalid gear position: {position}")

################################## ##MFS_3 for x70
def send_mfs_wechat(command):
    if command == 1:
        message = can.Message(arbitration_id=CAN_Contents.MFS_3, data=CAN_Contents.MFS_WEchat_Press, is_extended_id=False)
    elif command == 0:
        message = can.Message(arbitration_id=CAN_Contents.MFS_3, data=CAN_Contents.MFS_WEchat_Release, is_extended_id=False)
    else:
        print(f"Invalid command: {command}")
        return
    if send_can_messages_callback:
        send_can_messages_callback([message])

################################## ##MFS_3 for x50
def send_L_UP_SW(command):
    if command == 1:
        message = can.Message(arbitration_id=CAN_Contents.MFS_3, data=CAN_Contents.MFS_3_L_UP_SW_Press, is_extended_id=False)
    elif command == 0:
        message = can.Message(arbitration_id=CAN_Contents.MFS_3, data=CAN_Contents.MFS_3_L_UP_SW_Release, is_extended_id=False)
    else:
        print(f"Invalid command: {command}")
        return
    if send_can_messages_callback:
        send_can_messages_callback([message])

def send_L_DW_SW(command):
    if command == 1:
        message = can.Message(arbitration_id=CAN_Contents.MFS_3, data=CAN_Contents.MFS_3_L_DW_SW_Press, is_extended_id=False)
    elif command == 0:
        message = can.Message(arbitration_id=CAN_Contents.MFS_3, data=CAN_Contents.MFS_3_L_DW_SW_Release, is_extended_id=False)
    else:
        print(f"Invalid command: {command}")
        return
    if send_can_messages_callback:
        send_can_messages_callback([message])

def send_L_LEFT_SW(command):
    if command == 1:
        message = can.Message(arbitration_id=CAN_Contents.MFS_3, data=CAN_Contents.MFS_3_L_LEFT_SW_Press, is_extended_id=False)
    elif command == 0:
        message = can.Message(arbitration_id=CAN_Contents.MFS_3, data=CAN_Contents.MFS_3_L_LEFT_SW_Release, is_extended_id=False)
    else:
        print(f"Invalid command: {command}")
        return
    if send_can_messages_callback:
        send_can_messages_callback([message])

def send_L_RIGHT_SW(command):
    if command == 1:
        message = can.Message(arbitration_id=CAN_Contents.MFS_3, data=CAN_Contents.MFS_3_L_RIGHT_SW_Press, is_extended_id=False)
    elif command == 0:
        message = can.Message(arbitration_id=CAN_Contents.MFS_3, data=CAN_Contents.MFS_3_L_RIGHT_SW_Release, is_extended_id=False)
    else:
        print(f"Invalid command: {command}")
        return
    if send_can_messages_callback:
        send_can_messages_callback([message])

def send_L_OK_SW(command):
    if command == 1:
        message = can.Message(arbitration_id=CAN_Contents.MFS_3, data=CAN_Contents.MFS_3_L_OK_SW_Press, is_extended_id=False)
    elif command == 0:
        message = can.Message(arbitration_id=CAN_Contents.MFS_3, data=CAN_Contents.MFS_3_L_OK_SW_Release, is_extended_id=False)
    else:
        print(f"Invalid command: {command}")
        return
    if send_can_messages_callback:
        send_can_messages_callback([message])

def send_L_WECHAT_SW(command):
    if command == 1:
        message = can.Message(arbitration_id=CAN_Contents.MFS_3, data=CAN_Contents.MFS_3_L_WECHAT_SW_Press, is_extended_id=False)
    elif command == 0:
        message = can.Message(arbitration_id=CAN_Contents.MFS_3, data=CAN_Contents.MFS_3_L_WECHAT_SW_Release, is_extended_id=False)
    else:
        print(f"Invalid command: {command}")
        return
    if send_can_messages_callback:
        send_can_messages_callback([message])

def send_L_USER_SW(command):
    if command == 1:
        message = can.Message(arbitration_id=CAN_Contents.MFS_3, data=CAN_Contents.MFS_3_L_USER_SW_Press, is_extended_id=False)
    elif command == 0:
        message = can.Message(arbitration_id=CAN_Contents.MFS_3, data=CAN_Contents.MFS_3_L_USER_SW_Release, is_extended_id=False)
    else:
        print(f"Invalid command: {command}")
        return
    if send_can_messages_callback:
        send_can_messages_callback([message])

def send_R_UP_SW(command):
    if command == 1:
        message = can.Message(arbitration_id=CAN_Contents.MFS_3, data=CAN_Contents.MFS_3_R_UP_SW_Press, is_extended_id=False)
    elif command == 0:
        message = can.Message(arbitration_id=CAN_Contents.MFS_3, data=CAN_Contents.MFS_3_R_UP_SW_Release, is_extended_id=False)
    else:
        print(f"Invalid command: {command}")
        return
    if send_can_messages_callback:
        send_can_messages_callback([message])

def send_R_DW_SW(command):
    if command == 1:
        message = can.Message(arbitration_id=CAN_Contents.MFS_3, data=CAN_Contents.MFS_3_R_DW_SW_Press, is_extended_id=False)
    elif command == 0:
        message = can.Message(arbitration_id=CAN_Contents.MFS_3, data=CAN_Contents.MFS_3_R_DW_SW_Release, is_extended_id=False)
    else:
        print(f"Invalid command: {command}")
        return
    if send_can_messages_callback:
        send_can_messages_callback([message])

def send_R_LEFT_SW(command):
    if command == 1:
        message = can.Message(arbitration_id=CAN_Contents.MFS_3, data=CAN_Contents.MFS_3_R_LEFT_SW_Press, is_extended_id=False)
    elif command == 0:
        message = can.Message(arbitration_id=CAN_Contents.MFS_3, data=CAN_Contents.MFS_3_R_LEFT_SW_Release, is_extended_id=False)
    else:
        print(f"Invalid command: {command}")
        return
    if send_can_messages_callback:
        send_can_messages_callback([message])

def send_R_RIGHT_SW(command):
    if command == 1:
        message = can.Message(arbitration_id=CAN_Contents.MFS_3, data=CAN_Contents.MFS_3_R_RIGHT_SW_Press, is_extended_id=False)
    elif command == 0:
        message = can.Message(arbitration_id=CAN_Contents.MFS_3, data=CAN_Contents.MFS_3_R_RIGHT_SW_Release, is_extended_id=False)
    else:
        print(f"Invalid command: {command}")
        return
    if send_can_messages_callback:
        send_can_messages_callback([message])

def send_R_OK_SW(command):
    if command == 1:
        message = can.Message(arbitration_id=CAN_Contents.MFS_3, data=CAN_Contents.MFS_3_R_OK_SW_Press, is_extended_id=False)
    elif command == 0:
        message = can.Message(arbitration_id=CAN_Contents.MFS_3, data=CAN_Contents.MFS_3_R_OK_SW_Release, is_extended_id=False)
    else:
        print(f"Invalid command: {command}")
        return
    if send_can_messages_callback:
        send_can_messages_callback([message])

def send_R_RETURN_SW(command):
    if command == 1:
        message = can.Message(arbitration_id=CAN_Contents.MFS_3, data=CAN_Contents.MFS_3_R_RETURN_SW_Press, is_extended_id=False)
    elif command == 0:
        message = can.Message(arbitration_id=CAN_Contents.MFS_3, data=CAN_Contents.MFS_3_R_RETURN_SW_Release, is_extended_id=False)
    else:
        print(f"Invalid command: {command}")
        return
    if send_can_messages_callback:
        send_can_messages_callback([message])

def send_R_SPEECH_SW(command):
    if command == 1:
        message = can.Message(arbitration_id=CAN_Contents.MFS_3, data=CAN_Contents.MFS_3_R_SPEECH_SW_Press, is_extended_id=False)
    elif command == 0:
        message = can.Message(arbitration_id=CAN_Contents.MFS_3, data=CAN_Contents.MFS_3_R_SPEECH_SW_Release, is_extended_id=False)
    else:
        print(f"Invalid command: {command}")
        return
    if send_can_messages_callback:
        send_can_messages_callback([message])


################################## #MFS_4

def send_mfs_menu(command):
    if command == 1:
        message = can.Message(arbitration_id=CAN_Contents.MFS_4, data=CAN_Contents.MFS_Menu_Press, is_extended_id=False)
    elif command == 0:
        message = can.Message(arbitration_id=CAN_Contents.MFS_4, data=CAN_Contents.MFS_Menu_Release, is_extended_id=False)
    else:
        print(f"Invalid command: {command}")
        return
    if send_can_messages_callback:
        send_can_messages_callback([message])

def send_mfs_left_up(command):
    if command == 1:
        message = can.Message(arbitration_id=CAN_Contents.MFS_4, data=CAN_Contents.MFS_LEFT_UP_Press, is_extended_id=False)
    elif command == 0:
        message = can.Message(arbitration_id=CAN_Contents.MFS_4, data=CAN_Contents.MFS_LEFT_UP_Release, is_extended_id=False)
    else:
        print(f"Invalid command: {command}")
        return
    if send_can_messages_callback:
        send_can_messages_callback([message])

def send_mfs_left_down(command):
    if command == 1:
        message = can.Message(arbitration_id=CAN_Contents.MFS_4, data=CAN_Contents.MFS_LEFT_DOWN_Press, is_extended_id=False)
    elif command == 0:
        message = can.Message(arbitration_id=CAN_Contents.MFS_4, data=CAN_Contents.MFS_LEFT_DOWN_Release, is_extended_id=False)
    else:
        print(f"Invalid command: {command}")
        return
    if send_can_messages_callback:
        send_can_messages_callback([message])

def send_mfs_left_left(command):
    if command == 1:
        message = can.Message(arbitration_id=CAN_Contents.MFS_4, data=CAN_Contents.MFS_LEFT_LEFT_Press, is_extended_id=False)
    elif command == 0:
        message = can.Message(arbitration_id=CAN_Contents.MFS_4, data=CAN_Contents.MFS_LEFT_LEFT_Release, is_extended_id=False)
    else:
        print(f"Invalid command: {command}")
        return
    if send_can_messages_callback:
        send_can_messages_callback([message])

def send_mfs_left_right(command):
    if command == 1:
        message = can.Message(arbitration_id=CAN_Contents.MFS_4, data=CAN_Contents.MFS_LEFT_RIGHT_Press, is_extended_id=False)
    elif command == 0:
        message = can.Message(arbitration_id=CAN_Contents.MFS_4, data=CAN_Contents.MFS_LEFT_RIGHT_Release, is_extended_id=False)
    else:
        print(f"Invalid command: {command}")
        return
    if send_can_messages_callback:
        send_can_messages_callback([message])

def send_mfs_confirm(command):
    if command == 1:
        message = can.Message(arbitration_id=CAN_Contents.MFS_4, data=CAN_Contents.MFS_Confirm_Press, is_extended_id=False)
    elif command == 0:
        message = can.Message(arbitration_id=CAN_Contents.MFS_4, data=CAN_Contents.MFS_Confirm_Release, is_extended_id=False)
    else:
        print(f"Invalid command: {command}")
        return
    if send_can_messages_callback:
        send_can_messages_callback([message])

def send_mfs_mute(command):
    if command == 1:
        message = can.Message(arbitration_id=CAN_Contents.MFS_4, data=CAN_Contents.MFS_Mute_Press, is_extended_id=False)
    elif command == 0:
        message = can.Message(arbitration_id=CAN_Contents.MFS_4, data=CAN_Contents.MFS_Mute_Release, is_extended_id=False)
    else:
        print(f"Invalid command: {command}")
        return
    if send_can_messages_callback:
        send_can_messages_callback([message])

def send_mfs_voice(command):
    if command == 1:
        message = can.Message(arbitration_id=CAN_Contents.MFS_4, data=CAN_Contents.MFS_Voice_Press, is_extended_id=False)
    elif command == 0:
        message = can.Message(arbitration_id=CAN_Contents.MFS_4, data=CAN_Contents.MFS_Voice_Release, is_extended_id=False)
    else:
        print(f"Invalid command: {command}")
        return
    if send_can_messages_callback:
        send_can_messages_callback([message])

def send_mfs_voice_add(command):
    if command == 1:
        message = can.Message(arbitration_id=CAN_Contents.MFS_4, data=CAN_Contents.MFS_Voice_ADD_Press, is_extended_id=False)
    elif command == 0:
        message = can.Message(arbitration_id=CAN_Contents.MFS_4, data=CAN_Contents.MFS_Voice_ADD_Release, is_extended_id=False)
    else:
        print(f"Invalid command: {command}")
        return
    if send_can_messages_callback:
        send_can_messages_callback([message])

def send_mfs_voice_jian(command):
    if command == 1:
        message = can.Message(arbitration_id=CAN_Contents.MFS_4, data=CAN_Contents.MFS_Voice_Jian_Press, is_extended_id=False)
    elif command == 0:
        message = can.Message(arbitration_id=CAN_Contents.MFS_4, data=CAN_Contents.MFS_Voice_Jian_Release, is_extended_id=False)
    else:
        print(f"Invalid command: {command}")
        return
    if send_can_messages_callback:
        send_can_messages_callback([message])

def send_mfs_answer_hangup_phone(command):
    if command == 1:
        message = can.Message(arbitration_id=CAN_Contents.MFS_4, data=CAN_Contents.MFS_AnswerHangupPhone_Press, is_extended_id=False)
    elif command == 0:
        message = can.Message(arbitration_id=CAN_Contents.MFS_4, data=CAN_Contents.MFS_AnswerHangupPhone_Release, is_extended_id=False)
    else:
        print(f"Invalid command: {command}")
        return
    if send_can_messages_callback:
        send_can_messages_callback([message])

def send_mfs_previous(command):
    if command == 1:
        message = can.Message(arbitration_id=CAN_Contents.MFS_4, data=CAN_Contents.MFS_Previous_Press, is_extended_id=False)
    elif command == 0:
        message = can.Message(arbitration_id=CAN_Contents.MFS_4, data=CAN_Contents.MFS_Previous_Release, is_extended_id=False)
    else:
        print(f"Invalid command: {command}")
        return
    if send_can_messages_callback:
        send_can_messages_callback([message])

def send_mfs_next(command):
    if command == 1:
        message = can.Message(arbitration_id=CAN_Contents.MFS_4, data=CAN_Contents.MFS_NEXT_Press, is_extended_id=False)
    elif command == 0:
        message = can.Message(arbitration_id=CAN_Contents.MFS_4, data=CAN_Contents.MFS_NEXT_Release, is_extended_id=False)
    else:
        print(f"Invalid command: {command}")
        return
    if send_can_messages_callback:
        send_can_messages_callback([message])

################################## #CGW_SAM_G

def send_steering_angle(angle):
    angles = {
        0: CAN_Contents.SteeringAngle0degree,
        120: CAN_Contents.SteeringAngle120degree,
        -120: CAN_Contents.SteeringAnglem120degree
    }
    if angle in angles:
        message = can.Message(arbitration_id=CAN_Contents.CGW_SAM_G, data=angles[angle], is_extended_id=False)
        if send_can_messages_callback:
            send_can_messages_callback([message])
    else:
        print(f"Invalid steering angle: {angle}")


################################## #CEM_BCM_2

def send_alarm_mode_on_off(command):
    if command == 1:
        messages = [
            can.Message(arbitration_id=CAN_Contents.CEM_BCM_2, data=CAN_Contents.AlarmMode_On, is_extended_id=False)
        ]
        if send_can_messages_callback:
            send_can_messages_callback(messages)
    elif command == 0:
        messages = [
            can.Message(arbitration_id=CAN_Contents.CEM_BCM_2, data=CAN_Contents.AlarmMode_Off, is_extended_id=False)
        ]
        if send_can_messages_callback:
            send_can_messages_callback(messages)

def send_driver_door_open_close(command):
    if command == 1:
        messages = [
            can.Message(arbitration_id=CAN_Contents.CEM_BCM_2, data=CAN_Contents.DriverDoor_Open, is_extended_id=False)
        ]
        if send_can_messages_callback:
            send_can_messages_callback(messages)
    elif command == 0:
        messages = [
            can.Message(arbitration_id=CAN_Contents.CEM_BCM_2, data=CAN_Contents.DriverDoor_Close, is_extended_id=False)
        ]
        if send_can_messages_callback:
            send_can_messages_callback(messages)
    
def send_KeySts_on_off(command):
    if command == 1:
        messages = [
            can.Message(arbitration_id=0x392, data=CAN_Contents.KeySts_On, is_extended_id=False)
        ]
        if send_can_messages_callback:
            send_can_messages_callback(messages)
    elif command == 0:
        messages = [
            can.Message(arbitration_id=0x392, data=CAN_Contents.KeySts_Off, is_extended_id=False)
        ]
        if send_can_messages_callback:
            send_can_messages_callback(messages)

################################## #PLG

def send_plg_sas_sts(sts):
    statuses = {
        0: CAN_Contents.PLGSASSts_0,
        52: CAN_Contents.PLGSASSts_52,
        100: CAN_Contents.PLGSASSts_100,
        150: CAN_Contents.PLGSASSts_150
    }
    if sts in statuses:
        message = can.Message(arbitration_id=CAN_Contents.PLG, data=statuses[sts], is_extended_id=False)
        if send_can_messages_callback:
            send_can_messages_callback([message])
    else:
        print(f"Invalid PLG SAS status: {sts}")

################################### NWM_CGW
def send_nwm_cgw(command):
    commands = {
        0: CAN_Contents.NM_WAKEUP_0,
        1: CAN_Contents.NM_WAKEUP_1,
        2: CAN_Contents.NM_WAKEUP_2,
        3: CAN_Contents.NM_WAKEUP_3
    }
    if command in commands:
        message = can.Message(arbitration_id=CAN_Contents.NWM_CGW, data=commands[command], is_extended_id=False)
        if send_can_messages_callback:
            send_can_messages_callback([message])
    else:
        print(f"Invalid NWM CGW command: {command}")