import requests
import smtplib
from email.mime.multipart import  MIMEMultipart
from email.mime.text import MIMEText


API_KEY = "<>" # Your own api key
LAT = "<>"
LON = "<>"
OMW_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
MY_EMAIL = "<>"
TO_EMAIL = "<>"
PASSWORD = "<>"
params = {
    "lat":LAT,
    "lon":LON,
    "appid":API_KEY,
    "units":"metric",
    "cnt":4,
}


response = requests.get(url=OMW_Endpoint, params=params)
response.raise_for_status()
weather_data = response.json()["list"]
weather_info = []
weather_id = []
weather_time = []
will_rain = False
for hour_data in weather_data:
    weather_info.append((hour_data['weather'],hour_data['dt_txt'],hour_data['main']))
    weather_id.append(hour_data['weather'][0]['id'])

def worse_condition(weather : list):
    global will_rain
    for wid in weather:
        if wid < 700:
            will_rain = True

    return weather.index(max(weather))

today = weather_info[worse_condition(weather_id)]
print(today)

cleaned_message = (f"Today it's going to be {today[0][0]["description"]} at {today[1].split()[1]} UTC\n"
      f"Temperature is {today[2]['temp']}C, will feel like {today[2]['feels_like']}C\n"
      f"Minimum temp will be {today[2]['temp_min']} C and Maximum will be {today[2]['temp_max']} C \n"
      f"Humidity is {today[2]['humidity']}%")
image = f"https://openweathermap.org/img/wn/{today[0][0]['icon']}@2x.png"
html = f"""
        <html>
          <body>
            <img src={image} alt="Birthday Card" style="width:100px;">
          </body>
        </html>
        """



if will_rain:
    message = MIMEMultipart()
    message['From'] = MY_EMAIL
    message['To'] = TO_EMAIL
    message['Subject'] = "Today's Weather Forecast"
    message.attach(MIMEText(html, "html"))
    message.attach(MIMEText(cleaned_message, 'plain'))

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:

        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs=TO_EMAIL,
                            msg=message.as_string())





