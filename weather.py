import requests
import time
from flask import render_template, Flask, jsonify, request

app = Flask(__name__)


def getWeather(city):
    api = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=f908ec81b480e2e5814c7e6dfe2df714"
    json_data = requests.get(api).json()

    if json_data.get('cod') != 200:
        return {'error': 'City not found'}

    condition = json_data['weather'][0]['main']
    temp = int(json_data['main']['temp'] - 273.15)
    min_temp = int(json_data['main']['temp_min'] - 273.15)
    max_temp = int(json_data['main']['temp_max'] - 273.15)
    pressure = json_data['main']['pressure']
    humidity = json_data['main']['humidity']
    wind = json_data['wind']['speed']
    sunrise = time.strftime("%H:%M:%S", time.gmtime(json_data['sys']['sunrise'] - 21600))
    sunset = time.strftime("%H:%M:%S", time.gmtime(json_data['sys']['sunset'] - 21600))

    final_info = f"{condition}, {temp}°C"
    final_data = {
        "Condition": condition,
        "Temperature": f"{temp}°C",
        "Min Temperature": f"{min_temp}°C",
        "Max Temperature": f"{max_temp}°C",
        "Pressure": f"{pressure} hPa",
        "Humidity": f"{humidity}%",
        "Wind Speed": f"{wind} m/s",
        "Sunrise": sunrise,
        "Sunset": sunset
    }

    return {"summary": final_info, "details": final_data}



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/Prediction', methods = ['GET'])
def prediction():
    return render_template("Prediction.html")


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            weather_data = getWeather(city)
            if 'error' in weather_data:
                return render_template("Prediction.html", error=weather_data['error'])
            return render_template("Prediction.html", weather=weather_data, city = city)
        else:
            return render_template("Prediction.html", error="Please enter a city name.")
    return render_template("Prediction.html")



if __name__ == '__main__':
    app.run(debug=True)
