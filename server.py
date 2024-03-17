from waitress import serve
from flask import Flask, jsonify
from flask_restx import Resource, Api
import datetime
import random
import json

app = Flask(__name__)
api = Api(app)

weather_ns = api.namespace("weather","API's to work with weather data")

@weather_ns.route('/forcast/<zipcode>', methods=["GET"])
class WeatherForcast(Resource):
    weather_details = dict()
    weather_details_validity = dict()

    def get(this, zipcode):
        return jsonify(this.get_weather_details(zipcode))
    
    def get_weather_details(this, zipcode):
        if zipcode not in this.weather_details_validity or this.weather_details_validity.get(zipcode) < datetime.datetime.now():
            this.weather_details[zipcode] = this.generate_wather_details(zipcode)
            this.weather_details_validity[zipcode] = datetime.datetime.now() + datetime.timedelta(minutes=30)

        return this.weather_details.get(zipcode)

    def generate_wather_details(this, zipcode):
        output = {
            'zipcode': zipcode,
            'unit': 'Celcius',
            'summary': {},
            'data': [],
            'forecast': []
        }

        def get_summary_temp():
            low = random.randint(-13, 36)
            high = random.randint(low, 36)
            temp = random.randint(low, high)

            return {
                'low': low,
                'high': high,
                'temp': temp
            }
        
        output['summary'] = get_summary_temp()
        for index in range(1,7):
            output['forecast'].append({'date': (datetime.datetime.now() + datetime.timedelta(days=index)).date().isoformat()} | get_summary_temp())

        #historic data
        for index in range(1,12):
            output['data'].append({'datetime': (datetime.datetime.now() - datetime.timedelta(hours=index)).isoformat(timespec="minutes"), 'temperature': random.randint(output['summary']['low'], output['summary']['high'])})

        #forcast data
        for index in range(1,12):
            output['data'].append({'datetime': (datetime.datetime.now() + datetime.timedelta(hours=index)).isoformat(timespec="minutes"), 'temperature': random.randint(-13, 36)})

        return output

if __name__ == '__main__':
    print("Bringing up Server at 0.0.0.0:9002")
    serve(app, host='0.0.0.0', port='9002')