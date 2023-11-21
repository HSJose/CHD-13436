from appium import webdriver
from appium.options.android import UiAutomator2Options
from rich import print
import os
from dotenv import load_dotenv


# Load environmental variables from .env file
load_dotenv()  

# Get the value of the API_KEY variable from the .env file
api_key = os.getenv('API_KEY')  
headspin_header = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {api_key}'
}
base_api_url = f'https://{api_key}@api-dev.headspin.io'


def main() -> None:
    # Device to target
    # DUT
    dut_device_id = os.getenv('DUT_DEVICE_ID_1')
    dut_hostname = os.getenv('DUT_HOSTNAME_1')
    dut_device_address = os.getenv('DUT_DEVICE_ADDRESS_1')

    #Load Balancer Web Driver URL
    wd_url = f'https://appium-dev.headspin.io:443/v0/{api_key}/wd/hub'

    # Desired Capabilities
    my_caps = {
        "appium:automationName": "uiautomator2",
        "platformName": "android",
        "appium:deviceName": "Android",
        "appium:newCommandTimeout": 600,
        "headspin:capture": True,
        "headspin:capture.networkConfig": {
            "shaping": {
                "down": 20,
                "up": 20
            }
        },
        "headspin:controlLock": True,
        "udid": dut_device_id
    }

    app_options = UiAutomator2Options().load_capabilities(caps=my_caps)

    try:
        driver = webdriver.Remote(command_executor=wd_url, options=app_options)

        input("Press Enter to continue...")
        print(f'https://ui.headspin.io/sessions/{driver.session_id}/waterfall')

    except Exception as e:
        print(e)
    finally:
        if driver:
            driver.quit()
        

if __name__ == '__main__':
    main()
