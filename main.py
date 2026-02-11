import requests
import datetime as dt
import smtplib
import dotenv
import os
import time


dotenv.load_dotenv()
MY_PASSWORD = os.getenv(key="MY_PASSWORD")
MY_EMAIL = os.getenv(key="MY_MAIL")
MY_LAT = -26.204103
MY_LONG = 28.047304
ENDPOINT = "https://api.sunrise-sunset.org/json"


def check():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if (iss_latitude >= MY_LAT-5 and iss_latitude <= MY_LAT+5) and (iss_longitude >= MY_LONG-5 and iss_longitude <= MY_LONG +5):
        return True


def check_night():
    parameter = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0 
    }

    response = requests.get(ENDPOINT, params=parameter)
    response.raise_for_status()
    data = response.json()
    # print(data)

    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    now_time = dt.datetime.now().hour
    if now_time >= sunrise and now_time <= sunset:
         return True

    

# print(type(now_time))
send = False
while not send:
     
    time.sleep(5)
    if check() and check_night():
        # check if now is under sunrise and not oversunrise and go see the iss pass
            with smtplib.SMTP(host="smtp.gmail.com", port=587) as connection:
                connection.starttls()
                connection.login(user=MY_EMAIL, password=MY_PASSWORD)

                message = "Go outside to see the ISS pass on your current location \n Look up\nBy\nNjabs" 
                connection.sendmail(
                    from_addr=MY_EMAIL, to_addrs=MY_EMAIL, msg=f"Subject: ISS passing \n\n{message}"
                )

            send = True



    else:print("none")
#     else:
#         print("its not the write time to go outside")
# else:
#     print("its not there yet")