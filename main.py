import datetime
import time

import fake_useragent
import requests
import urllib3

DIST_ID = int(input("Please enter your District ID:\n"))  # Your District ID
num_days = int(input("Please enter the range of days to check:\n"))  # No of days to check. 5 days is ideal within the API Query limit
age = int(input("Please enter your Age:\n"))  # Your Age
my_agent = fake_useragent.UserAgent()
response_json = {}
new_response_json = {}


def cur_time():
    current_time = "(" + (
            datetime.datetime.now().utcnow() +
            datetime.timedelta(hours=5.5)).strftime("%d/%m/%Y %H:%M:%S") + ")"
    return current_time


def countdown(t):
    while t:
        timer = f'{t} Seconds '
        print("Waking up in " + timer, end="\r")
        time.sleep(1)
        t -= 1


def get_dates():
    base = datetime.datetime.today().utcnow() + datetime.timedelta(hours=5.5)
    date_list = [base + datetime.timedelta(days=x) for x in range(num_days)]
    date_str = [x.strftime("%d-%m-%Y") for x in date_list]
    return date_str


def telegram_bot_send_text(bot_message):
    bot_token = '5145209465:AAHgft1dbdxHX6nM-SiIfXNQ-R4dGyqbsow'  # Your Bot token. See Readme.md for more details
    channel_id = '1500144876'  # Your Channel ID. See Readme.md for more details
    # For example, if your ID is -1001234567890, Enter "1234567890"(without quotes)
    send_channel = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=-100' + channel_id + '&parse_mode=HTML&text=' + bot_message
    response = requests.get(send_channel)
    if 400 <= response.status_code <= 499:
        print("Client Side Error encountered ", response.status_code)
    elif 500 <= response.status_code <= 599:
        print("Server Side Error encountered ", response.status_code)
    return response.json()


def get_header():
    try:
        my_agent = fake_useragent.UserAgent(use_cache_server=False)
        browser_header = {'User-Agent': my_agent.random}
    except fake_useragent.errors.FakeUserAgentError:
        browser_header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/62.0.3202.94 Safari/537.36'}
    except fake_useragent.errors:
        browser_header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/62.0.3202.94 Safari/537.36'}
    except:
        browser_header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/62.0.3202.94 Safari/537.36'}
    return browser_header


def get_response(date_str, browser_header, json):
    for each_date in date_str:
        url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={DIST_ID}&date={each_date}"
        try:
            response = requests.get(url,
                                    headers=browser_header,
                                    timeout=(7, 12.5))
            if response.ok:
                resp_json = response.json()
                json[each_date] = resp_json
                response.close()
            elif response.status_code == 403:
                print("Request Forbidden by Server ", cur_time())
                response.close()
            else:
                print("Weird Response from Server ", cur_time())
                print(response.text)
                response.close()
        except TimeoutError:
            print("Timeout Error ", cur_time())
            break
        except requests.exceptions.ConnectionError as e:
            print("Connection Error ", cur_time())
            print(e)
            break
        except urllib3.exceptions.TimeoutError:
            print("Socket timeout error ", cur_time())
            break
        except urllib3.exceptions.RequestError:
            print("Urllib3 Requests error ", cur_time())
            break


def print_slots(resp_json, center_name, the_date):
    if resp_json["sessions"]:
        for center in resp_json["sessions"]:
            if center["name"] == center_name:
                if center["min_age_limit"] <= age:
                    if center["available_capacity"] > 0:
                        if center["available_capacity_dose1"] == 0:
                            result = f"""
    1) Name: <b><i>{center["name"]}</i></b>
    2) Area: <i>{center["block_name"]}</i>
    3) Address: <i>{center["address"]}</i>
    4) Availability date: <i>{the_date}</i>
    5) Price: <i>₹.{center["fee"]}/-</i>
    6) Total Available Capacity: <b>{center["available_capacity"]}</b>
        (Dose 1 - <b><i>{center["available_capacity_dose1"]}</i></b>; Dose 2 - <b><i>{center["available_capacity_dose2"]}</i></b>)
    <b>Dose 1</b> is not available
    7) Vaccine: <b><i>{center["vaccine"]}</i></b>

    Data Retrieved from CO-WIN Portal on {cur_time()}
    Access Co-WIN here : https://selfregistration.cowin.gov.in
        """
                        elif center["available_capacity_dose2"] == 0:
                            result = f"""
    1) Name: <b><i>{center["name"]}</i></b>
    2) Area: <i>{center["block_name"]}</i>
    3) Address: <i>{center["address"]}</i>
    4) Availability date: <i>{the_date}</i>
    5) Price: <i>₹.{center["fee"]}/-</i>
    6) Total Available Capacity: <b>{center["available_capacity"]}</b>
        (Dose 1 - <b><i>{center["available_capacity_dose1"]}</i></b>; Dose 2 - <b><i>{center["available_capacity_dose2"]}</i></b>)
    <b>Dose 2</b> is not available
    7) Vaccine: <b><i>{center["vaccine"]}</i></b>

    Data Retrieved from CO-WIN Portal on {cur_time()}
    Access Co-WIN here : https://selfregistration.cowin.gov.in
    """
                        else:
                            result = f"""
    1) Name: <b><i>{center["name"]}</i></b>
    2) Area: <i>{center["block_name"]}</i>
    3) Address: <i>{center["address"]}</i>
    4) Availability date: <i>{the_date}</i>
    5) Price: <i>₹.{center["fee"]}/-</i>
    6) Total Available Capacity: <b>{center["available_capacity"]}</b>
        (Dose 1 - <b><i>{center["available_capacity_dose1"]}</i></b>; Dose 2 - <b><i>{center["available_capacity_dose2"]}</i></b>)
    7) Vaccine: <b><i>{center["vaccine"]}</i></b>

    Data Retrieved from CO-WIN Portal on {cur_time()}
    Access Co-WIN here : https://selfregistration.cowin.gov.in
                                """
                        # print(result) # For more details, Head to FAQ-1 of Readme.md
                        telegram_bot_send_text(result)  # FAQ-1
                        print("Message Sent to telegram channel ", cur_time())  # FAQ-1
    else:
        print(f"No available slots on {the_date}")


def change_to_readable_format(resp1):
    available_centres = {
        centre["name"]: centre["available_capacity"]
        for centre in resp1['sessions']
    }
    return available_centres


if __name__ == "__main__":
    Header = get_header()
    while True:
        dates = get_dates()
        get_response(dates, Header, response_json)
        print("Response received.", cur_time())
        for date in dates:
            try:
                total_centers = change_to_readable_format(response_json[date])
                if len(total_centers) == 0:
                    print(f"No slots are available on {date} ", cur_time())
                else:
                    for each_centre in total_centers:
                        print_slots(response_json[date], each_centre, date)
                        countdown(5)
            except KeyError:
                print("Handling Key Error ", cur_time())
                continue
