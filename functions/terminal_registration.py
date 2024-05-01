import sqlite3
import struct
from protocol import construct_message

def parse_terminal_registration_message(data):

    provincial_id = int.from_bytes(data[0:2], byteorder='little')
    area_id = int.from_bytes(data[2:4], byteorder='little')
    manufacturer_id = data[4:9].decode('utf-8')
    terminal_model = data[9:29].decode('utf-8')
    terminal_id = data[29:36].decode('utf-8')
    license_plate_color = data[36:37].decode('utf-8')
    plate_number = data[37:len(data)-1].decode('utf-8')

    return {
        'province_id': provincial_id,
        'city_id': area_id,
        'manufacturer_id': manufacturer_id,
        'terminal_model': terminal_model,
        'terminal_id': terminal_id,
        'license_plate_color': license_plate_color,
        'plate_number': plate_number
    }

def save_location_database(registration_info):
    connection = sqlite3.connect('vehicle_data.db')
    cursor = connection.cursor()

    cursor.execute('select max(id) from location')

    result = cursor.fetchone()
    max_id = result[0] if result[0]  else 0
    max_id += 1

    cursor.execute('''
        INSERT INTO location (id,warning_mark, acc_flag, pos_flag, latitude, longitude, velocity, plate_number, direction, time)
        VALUES (?,?, ?, ?, ?, ?, ?, ?, ?,?)
    ''', (
        max_id,
        registration_info['warning_mark'],
        registration_info['acc_flag'] if 1 else 0,
        registration_info['pos_flag'] if 1 else 0,
        registration_info['latitude'],
        registration_info['longitude'],
        registration_info['altitude'],
        registration_info['velocity'],
        registration_info['plate_number'],
        registration_info['direction'],
        registration_info['time']
    ))
    connection.commit()
    connection.close()

def construct_terminal_registration_response(serial_number, result, auth_code=''):
    message_id = 0x8100
    response_body = struct.pack('>HB', serial_number, result)
    if result == 0:
        response_body += auth_code.encode('ascii')

    return response_body

def handle_terminal_registration(message_id,  serial_number, phone_num , data):
    registration_info = parse_terminal_registration_message(data)
    
    save_to_database(registration_info)

    result = 0
    auth_code = 'some_auth_code'  # Generate or retrieve an appropriate auth code
    response_data = serial_number.to_bytes(2, byteorder='big') + result.to_bytes(1, byteorder='big') + auth_code.encode('utf-8')
    response = construct_message(message_id, phone_num, response_data, serial_number=0, public_key=None, encryption_method=0, is_subpackage=False, total_packages=1, package_number=1)
    return response


def save_to_database(registration_info):
    connection = sqlite3.connect('vehicle_data.db')
    cursor = connection.cursor()
    cursor.execute('select max(id) from vehicles')

    result = cursor.fetchone()
    print(f"data result {result}")
    max_id = result[0] if result[0]  else 0
    max_id += 1
    cursor.execute('''
        INSERT INTO vehicles (id,province_id, city_id, manufacturer_id, terminal_model, terminal_id, license_plate_color, plate_number)
        VALUES (?,?, ?, ?, ?, ?, ?, ?)
    ''', (
        max_id,
        registration_info['province_id'],
        registration_info['city_id'],
        registration_info['manufacturer_id'],
        registration_info['terminal_model'],
        registration_info['terminal_id'],
        registration_info['license_plate_color'],
        registration_info['plate_number']
    ))
    connection.commit()
    connection.close()

def db_check():

    vecicle_table = 'CREATE TABLE IF NOT EXISTS vehicles (id INT AUTO_INCREMENT,\
                    province_id INT,\
                    city_id INT,\
                    manufacturer_id INT,\
                    terminal_model VARCHAR(100),\
                    terminal_id INT,\
                    license_plate_color VARCHAR(50),\
                    plate_number VARCHAR(50),\
                    PRIMARY KEY (id)\
                    )'
    location_table =  'CREATE TABLE IF NOT EXISTS location (\
                        id INT AUTO_INCREMENT,\
                        warning_mark INT,\
                        acc_flag TINYINT,\
                        pos_flag TINYINT,\
                        latitude DECIMAL(10, 7),\
                        longitude DECIMAL(10, 7),\
                        altitude VARCHAR(255),\
                        velocity VARCHAR(255),\
                        plate_number VARCHAR(50),\
                        direction INT,\
                        time TIMESTAMP,\
                        PRIMARY KEY (id))'
    
    connection = sqlite3.connect('vehicle_data.db')
    cursor = connection.cursor()
    cursor.execute(vecicle_table)
    cursor.execute(location_table)
    connection.commit()
    connection.close()


