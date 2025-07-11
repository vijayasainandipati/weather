from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "your_secret_key_here"

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    error_message = None

    if request.method == 'POST':
        city_input = request.form['city'].strip()
        if city_input:
            # Split city and country code if provided
            parts = city_input.split(',')
            city = parts[0].strip()
            country_code = parts[1].strip() if len(parts) > 1 else None

            # Construct geocoding URL
            geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}"
            if country_code:
                geo_url += f",{country_code}"
            geo_url += f"&limit=1&appid={API_KEY}"

            try:
                geo_response = requests.get(geo_url).json()

                if geo_response:
                    lat = geo_response[0]['lat']
                    lon = geo_response[0]['lon']

                    # Get weather data using coordinates
                    weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
                    weather_response = requests.get(weather_url).json()

                    if weather_response.get("cod") == 200:
                        weather_data = {
                            'city': geo_response[0]['name'],
                            'country': geo_response[0]['country'],
                            'temperature': round(weather_response['main']['temp'], 1),
                            'description': weather_response['weather'][0]['description'].capitalize(),
                            'humidity': weather_response['main']['humidity'],
                            'wind': weather_response['wind']['speed'],
                            'icon': weather_response['weather'][0]['icon']
                        }
                    else:
                        error_message = "Weather data not found."
                else:
                    error_message = "City not found. Please check the name and try again."
            except Exception as e:
                error_message = "An error occurred while fetching weather data."

    return render_template('index.html', weather=weather_data, error=error_message)

if __name__ == '__main__':
    app.run(debug=True) 