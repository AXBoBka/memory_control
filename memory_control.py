import requests
import psutil
import json
import time
import sys
import os


def load_json_config_from_file(json_config_file: str):
    with open(json_config_file, 'r') as config_file:
        data = json.load(config_file)
    return data

def memory_control(json_config: json) -> tuple:
    memory_info = psutil.virtual_memory()
    # print('System memory:', memory_info)
    if memory_info[2] > json_config['MAX_MEMORY_USAGE']:
        print('Send request to API')
        return False, memory_info[2]
    return True, memory_info[2]


if __name__ == "__main__":
    if len(sys.argv) > 2:
        json_config = load_json_config_from_file(sys.argv[1])
        sleep_between_mem_check = int(sys.argv[2])
    else:
        print(f'Usage: python3 {sys.argv[0]} <json_config_file> <sleep_between_mem_check>')
        exit(1)

    while True:
        status, memory_info = memory_control(json_config)
        if status is not True:
            err = 'Ошибка - потребление памяти привысило максимальное значение!'
            print(err)
            url_req = "https://api.telegram.org/bot" + os.getenv('BOT_TOKEN') + "/sendMessage" + "?chat_id=" + os.getenv('CHAT_ID') + "&text=" + err 
            result = requests.get(url_req)
            if result.status_code != 200:
                err = f"Ошибка во время отправки уведомления: bot_id: {os.getenv('BOT_TOKEN')}, chat_id: {os.getenv('CHAT_ID')} - error: {result.status_code} - {result.reason}"
                print(err)
                exit(1)
        print(memory_info)

        time.sleep(sleep_between_mem_check)
