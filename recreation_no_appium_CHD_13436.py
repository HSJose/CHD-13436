import httpx
from dotenv import load_dotenv
from rich import print
import os

load_dotenv()  # Load environmental variables from .env file

api_key = os.getenv('API_KEY')  # Get the value of the API_KEY variable from the .env file
headspin_header = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {api_key}'
}
base_api_url = f'https://{api_key}@api-dev.headspin.io'


def call_api(url: str, data: dict = None, headers: dict = None):
    try:
        response = httpx.post(url, json=data, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(response.json())
            raise Exception(f"API call failed with status code {response.status_code}")
    except Exception as e:
        print(e)
        return None


def main() -> None:
    # Device to target
    # DUT
    dut_device_id = os.getenv('DUT_DEVICE_ID')
    dut_hostname = os.getenv('DUT_HOSTNAME')
    dut_device_address = os.getenv('DUT_DEVICE_ADDRESS')
    # CD
    cd_device_id = os.getenv('CD_DEVICE_ID')
    cd_hostname = os.getenv('CD_HOSTNAME')
    cd_device_address = os.getenv('CD_DEVICE_ADDRESS')

    # Session ID
    session_id = None

    # Shaping dict
    network_shaping = {
        "down": 20,
        "up": 20
    }

    # Capture dict
    session_capture_settings = {
        "session_type": "capture",
        "device_address": dut_device_address,
        "capture_video": True,
        "capture_network": False,
        "network_shaping": network_shaping
    }

    # List of API endpoints

    lock = f'/v0/devices/lock'
    lock_data = {"hostname": dut_hostname, "device_id": dut_device_id}
    unlock = f'/v0/devices/unlock'
    session_start = f'/v0/sessions'
    session_end = f'/v0/sessions/{session_id}'

    # List of steps

    # Step 1 Lock Device
    print("Locking Device")
    device_lock = call_api(f'{base_api_url}{lock}', data=lock_data, headers=headspin_header)
    print("Device Locked")
    print(device_lock)

    # Step 2 Start session recording
    print("Starting session recording")
    session_start_api_call = call_api(f'{base_api_url}{session_start}', data=session_capture_settings, headers=headspin_header)
    print("Session recording started")
    print(session_start_api_call)
    try:
        session_id = session_start_api_call['session_id']
    except Exception as e:
        print('No session started') 
        print(f'Error: {e}')
        pass


    # Step 3 Manually check network shaping
    input("Press Enter to continue...")

    # Step 4 End session recording
    if session_id:
        print("Ending session recording")
        session_end_api_call = call_api(f'{base_api_url}{session_end}', headers=headspin_header)
        print("Session recording ended")
        print(session_end_api_call)

    # Step 5 Unlock device
    device_unlock = call_api(f'{base_api_url}{unlock}', data=lock_data, headers=headspin_header)
    print(device_unlock)


if __name__ == '__main__':
    main()
