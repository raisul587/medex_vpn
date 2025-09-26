import subprocess
import time
import requests

# Set to store used IPs (kept consistent with original; currently not enforced)
used_ips = set()


def reconnect_vpn(max_attempts: int = 5) -> bool:
    try:
        vpn_path = 'C:\\Program Files (x86)\\hide.me VPN\\Hide.me.exe'

        attempt = 0
        while attempt < max_attempts:
            attempt += 1

            # Kill any existing VPN process
            print("Closing VPN...")
            subprocess.run(['taskkill', '/F', '/IM', 'Hide.me.exe'], capture_output=True, check=False)
            time.sleep(5)

            # Start VPN (it will auto-connect)
            print("Starting VPN...")
            subprocess.Popen([vpn_path])
            time.sleep(20)

            # Verify connection and check IP
            try:
                response = requests.get('https://api.myip.com', timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    current_ip = data.get('ip')
                    print(f"VPN connected successfully with new IP: {current_ip}")
                    return True
                else:
                    print("VPN connection verification failed")
            except Exception as e:
                print(f"Error verifying VPN connection: {e}")

            print(f"Attempt {attempt}/{max_attempts} failed. Retrying...")
            time.sleep(5)

        print(f"Failed to get a new IP after {max_attempts} attempts")
        return False

    except subprocess.CalledProcessError as e:
        print(f"Error with VPN command: {e}")
        print(f"Command output: {e.output if hasattr(e, 'output') else 'No output'}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False


def check_vpn_status() -> bool:
    try:
        response = requests.get('https://api.myip.com', timeout=5)
        return response.status_code == 200
    except Exception:
        return False


def wait_for_vpn(timeout: int = 60) -> bool:
    print("Waiting for VPN to connect...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        if check_vpn_status():
            print("VPN is connected!")
            return True
        time.sleep(5)
    print("VPN connection timeout")
    return False
