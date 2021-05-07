import json
from pathlib import Path
from colorama import Fore, init, deinit
import requests
import datetime
import time
import winsound


def read_district(file_path: Path):
    with file_path.open('r') as f:
        districts = json.load(f)['districts']
    return districts


# def fetch_by_pin(pin):
#     pin_code_url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?" \
#                    f"pincode={pin}&date={date}"
#     pass


def fetch_by_district(district_id: str, date: str):     # noqa
    district_url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?" \
                   f"district_id={district_id}&date={date}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/50.0.2661.102 Safari/537.36',
        'Accept': 'application/json'}

    res = requests.get(district_url, headers=headers)
    if res.status_code != 200:
        print(Fore.RED + f'API Error. Reason: {res.reason}' + Fore.RESET)
        return None

    return res.json()['centers']


if __name__ == '__main__':
    try:
        init()
        district_list = read_district(Path('district_code.json'))
        district_ids = {}

        print(Fore.BLUE)
        print("Below is the mapping of each district with their district id:\n")
        for center in district_list:
            print(f"{center['district_name']:<35}: {center['district_id']}")
            district_ids[str(center['district_id'])] = center['district_name']

        # enter district id
        print(Fore.RESET)
        district_id = input('\nEnter district id for your district: ').strip()
        if district_id not in district_ids:
            raise Exception('Invalid district_id entered !')

        # enter min-age limit
        min_age = int(input('Enter min-age limit (18 or 45): ').strip())
        if min_age != 18 and min_age != 45:
            raise Exception('Invalid age limit entered !')

        print()
        available_centers = {'centers': []}
        check_count = 1
        while True:
            print(Fore.YELLOW + f'CHECK {check_count}' + Fore.RESET)
            date = datetime.datetime.now().strftime('%d-%m-%Y')
            centers = fetch_by_district(district_id, date)
            if not centers:
                time.sleep(3)
                check_count += 1
                continue
            for center in centers:
                for session in center["sessions"]:
                    if session["available_capacity"] > 0 and session["min_age_limit"] == min_age:
                        available_centers['centers'].append({
                            'center': center["name"],
                            'pin_code':  center["pincode"],
                            'date': session["date"],
                            'capacity': session["available_capacity"],
                            'min_age_limit': session["min_age_limit"],
                            'vaccine': session["vaccine"]
                        })
            if available_centers['centers']:
                for center in available_centers['centers']:
                    print(Fore.GREEN)
                    print(f'{"Center":<35}: {center["center"]}')
                    print(f'{"Pin Code":<35}: {center["pin_code"]}')
                    print(f'{"Available Date":<35}: {center["date"]}')
                    print(f'{"Available Capacity":<35}: {center["capacity"]}')
                    print(f'{"Minimum Age Limit":<35}: {center["min_age_limit"]}')
                    print(f'{"Vaccine":<35}: {center["vaccine"]}')
                    print(Fore.RESET)
                    print('-'*50)

                print(Fore.YELLOW)
                print(f'\nTime: {datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")}')
                print(f'Above centers are available for booking. Book Now !!')
                print(Fore.RESET)
                winsound.Beep(800, 2500)
                break
            check_count += 1
            time.sleep(3)

    except Exception as e:
        print(Fore.RED)
        print(f'Oops...Something went wrong')
        print(f'Error: {e}')
        print(Fore.RESET)
    except KeyboardInterrupt:
        pass
    finally:
        input('Press ENTER to exit terminal')
        print(Fore.MAGENTA + '\nBYE')
        print(Fore.RESET)
        deinit()
        time.sleep(1)