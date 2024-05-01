import socket
from protocol import parse_message, construct_message
from functions.terminal_registration import handle_terminal_registration, db_check
import json

def start_server(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Server listening on {host}:{port}")
        db_check()
        while True:
            conn, addr = s.accept()
            print(f"Connection from {addr}")
            try:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    response = handle_recv_message(data)
                    conn.sendall(response.encode())
            finally:
                conn.close()

def handle_recv_message(data):

    parsed_data = parse_message(data=data, private_key=None)

    if parsed_data['message_id'] == 0x0100:
        response = handle_terminal_registration(parsed_data['message_id'], parsed_data['serial_number'], parsed_data['phone_number'], parsed_data['body'])
    elif parsed_data['message_id'] == 0x0102:
        response = handle_authontication(parsed_data['serial_number'], parsed_data['phone_number'])
    elif parsed_data['message_id'] == 0x8300:
        response = handle_information_distribution()
    
    return response

def handle_authontication(serial_number,phone_number):
    message_id = 0x0102
    reply_id = 0x0102
    bear_fruit = 0 # 0:Success/confirmation 1: failure
    response_data = serial_number.to_bytes(2, byteorder='big') + reply_id.to_bytes(2, byteorder='big') + bear_fruit.to_bytes(1, byteorder='big')
    return construct_message(message_id, phone_number, response_data, serial_number=0, public_key=None, encryption_method=0, is_subpackage=False, total_packages=1, package_number=1)

def handle_information_distribution():
    message_id = 0x8300
    phone_number = ''
    sign = 0x0001
    text_info = 'this is text information!'
    response_data = sign.to_bytes(1, byteorder='big') + text_info.encode(1, "gbk")
    return construct_message(message_id, phone_number, response_data, serial_number=0, public_key=None, encryption_method=0, is_subpackage=False, total_packages=1, package_number=1)

def handle_location(body):

    warning_mark =  body[0:4].decode('utf-8')
    status_flag = body[4:8].decode('utf-8')
    acc_flag = (status_flag[0] >> 7) & 1 # 0 Acc Off 1 Acc On
    pos_flag = (status_flag[0] >> 6) & 1 # 0: Not positioned; 1: positioned
    

    latitude = body[8:12].decode('utf-8')
    longitude = body[12:16].decode('utf-8')
    altitude = body[16:18].decode('utf-8')
    velocity = body[18:20].decode('utf-8')
    
    direction = body[20:22].decode('utf-8')
    direction_value = direction # 0 ~ 360'

    time = body[22:28].decode('utf-8')
    time_year = body[22:23].decode('utf-8') # 24-04-12-15-20-33 date sample
    time_month = body[23:24].decode('utf-8')
    time_day = body[24:25].decode('utf-8')
    time_hour = body[25:26].decode('utf-8')
    time_minute = body[26:27].decode('utf-8')
    time_second = time[27:28].decode('utf-8')
    time = time_year + '-' + time_month + '-' + time_day + '-' + time_hour + '-' + time_minute + '-' + time_second

def handle_ad_voltage(body):

    default_pre = body[0:2].decode('little')
    instruction = body[2:4].decode('little')
    ad_voltage = int.from_bytes(body[4:7].decode('little')) 

def handle_battery_value(body):
    default_pre = body[0:2].decode('little')
    instruction = body[2:4].decode('little')
    battery_percent = int.from_bytes(body[4:6].decode('little'))/1500

def handle_version_information(body):
   
    default_pre = int.from_bytes(body[0:2].decode('little')) - 2
    instruction = body[2:4].decode('little')
    data = body[4:default_pre].decode('utf-8')

def handle_alarm_state(body):
    default_pre = body[0:2].decode('little')
    instruction = body[2:4].decode('little')
    data = body[4:8].decode('little')

def handle_battery_value(body):
    default_pre = body[0:2].decode('little')
    instruction = body[2:4].decode('little')
    data = int.from_bytes(body[4:7].decode('little')) 

def handle_base_station(body):
    default_pre = body[0:2].decode('little')
    instruction = body[2:4].decode('little')
    data = body[4:13].decode('utf-8')
    country_num = data[0:2]
    operater_num = data[2:4]
    base_num = data[4:5]
    area_code = data[5:7]
    tower_number = data[7:9]
    sign_intensity = data[9:10]

    shifted_default_pre = default_pre.to_bytes(2, byteorder='little')
    shifted_instruction = instruction.to_bytes(2, byteorder='little')

def handle_wifi_data(body):

    instruction = body[2:4].decode('little')
    default_pre = int.from_bytes(body[0:2].decode('little')) - 3 
    data = body[4:default_pre].decode('utf-8')
    host_spot = data[0]
    wifi_format = data[1:default_pre]
     
def handle_sim_iccid(body):
    default_pre = body[0:2].decode('little')
    instruction = body[2:4].decode('little')
    data = body[4:24].decode('utf-8')

def handle_location_status(body):
    default_pre = body[0:2].decode('little')
    instruction = body[2:4].decode('little')
    data = body[4:8].decode('utf-8')
    location_state = ''

    if data[3] == '1' and data[4] == '0':
        location_state = 'GPS localization'
    elif data[3] == '0' and data[4] == '0':
        location_state = 'not posited'
    elif data[3] == '0' and data[4] == '1':
        location_state = 'WIFI localization'

def handle_base_station(body):
    
    instruction = body[2:4].decode('little')
    
    default_pre = int.from_bytes(body[0:2].decode('little')) - 2
    data = body[4:default_pre].decode('utf-8')
    
def handle_base_station_4G(body):
    
    instruction = body[2:4].decode('little')
    default_pre = int.from_bytes(body[0:2].decode('little')) - 2
    data = body[4:default_pre].decode('utf-8')

def handle_power_remain(body):
    default_pre = body[0:2].decode('little')    
    instruction = body[2:4].decode('little')
    data = int.from_bytes(body[4:5].decode('utf-8'))

def handle_voltage_value(body):
    default_pre = body[0:2].decode('little')
    instruction = body[2:4].decode('little')
    data = int.from_bytes(body[4:5].decode('utf-8'))


start_server("127.0.0.1", 1234)