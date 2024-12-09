import can
import time

# CAN 통신 초기화
#bus = can.interface.Bus(bustype='kvaser', app_name='CANoe', channel=0, bitrate=500000)
bus = can.interface.Bus(bustype='vector', app_name='CANoe', channel=0, bitrate=500000)

# 메시지 ID 정의
diag_req_id = 0x74A
diag_res_id = 0x75A

# VIN 데이터
VINDataIdentifier_Write = [0x2E, 0xF1, 0x90, 0x45, 0x43, 0x33, 0x44, 0x4C, 0x55, 0x47, 0x44, 0x35, 0x52, 0x30, 0x30, 0x30, 0x30, 0x32, 0x30, 0x37]


# 키 값
key = 0xFD
sub_key = 0x6C

def send_message(message_id, data):
    message = can.Message(arbitration_id=message_id, data=data, is_extended_id=False)
    bus.send(message)
    print(f"Sent message: {message}")

def recv_messages():
    msg = bus.recv(timeout=1)
    if msg.arbitration_id == diag_res_id:
        print(f"Received message: {msg}")

def send_extended_session():
    send_message(diag_req_id, [0x02, 0x10, 0x03])

def send_key_request():
    send_message(diag_req_id, [0x02, 0x27, 0x03])

def send_key_send():
    send_message(diag_req_id, [0x04, 0x27, 0x04, key, sub_key])

def send_vin_write():
    # 첫 프레임 전송
    first_frame = [0x10, len(VINDataIdentifier_Write)] + VINDataIdentifier_Write[:6]
    send_message(diag_req_id, first_frame)
    time.sleep(0.03)
    
    # 연속 프레임 전송
    remaining_data = VINDataIdentifier_Write[6:]
    sequence_number = 1
    while remaining_data:
        chunk = remaining_data[:7]
        remaining_data = remaining_data[7:]
        consecutive_frame = [0x20 + sequence_number] + chunk
        send_message(diag_req_id, consecutive_frame)
        sequence_number = (sequence_number + 1) % 16
        time.sleep(0.1)
    return True

def send_vin_read():
    send_message(diag_req_id, [0x03, 0x22, 0xF1, 0x90])

def send_hardreset():
    send_message(diag_req_id, [0x02, 0x11, 0x01])

while True:
    sleeptime = 30
    # 진단 세션 시작
    send_extended_session()
    time.sleep(0.1)

    # 키 요청 및 전송
    send_key_request()
    time.sleep(0.1)
    send_key_send()
    time.sleep(0.1)

    # VIN 데이터 작성
    if not send_vin_write():
        print("Failed to write VIN")
        continue
    time.sleep(1)

    # VIN 데이터 읽기
    send_vin_read()
    recv_messages()
    time.sleep(1)

    # 하드 리셋
    send_hardreset()

    # 30초 대기
    print(f"Wait for {sleeptime} sec")
    time.sleep(sleeptime)
