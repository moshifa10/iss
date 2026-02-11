import requests
import datetime as dt
import smtplib
import dotenv
import os


dotenv.load_dotenv()
MY_PASSWORD = os.getenv(key="MY_PASSWORD")
MY_EMAIL = os.getenv(key="MY_MAIL")
MY_LAT = -26.204103
MY_LONG = 28.047304
ENDPOINT = "https://api.sunrise-sunset.org/json"



response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])


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


def check(current_iss_la, current_iss_lng):
    print("current iss :",current_iss_la,current_iss_lng)
    print("my lat and lng:",MY_LAT, MY_LONG)
    if (current_iss_la >= MY_LAT-5 and current_iss_la <= MY_LAT+5) and (current_iss_lng >= MY_LONG-5 and current_iss_lng <= MY_LONG +5):
        return True
    
now_time = dt.datetime.now().hour
# print(type(now_time))
if check(iss_latitude, iss_longitude):
    # check if now is under sunrise and not oversunrise and go see the iss pass

    if now_time >= sunrise and now_time <= sunset:
        
        with smtplib.SMTP(host="smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login()