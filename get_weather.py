
from distutils.command.config import config
import sys
import json
import urllib.request
from urllib.error import HTTPError


def get_ip_location():
    try:
        response = urllib.request.urlopen("http://checkip.dyndns.org").read()
        response = response.decode("utf-8")
        response = response.partition("IP Address: ")
        ip_address = response[2].partition("<")
        print("IP Address:", ip_address[0])

    except HTTPError as error:
        if error.code == 502:
            print("Network Error. Please try again")

        else:
            print("Error not recognized. Here is error HTTTP Error Code: ", error.code)

        exit(0)

    try:
        location_data = urllib.request.urlopen("http://ip-api.com/json/" + ip_address[0]).read()
        location_data = location_data.decode("utf-8")
        location = json.loads(location_data)
        return location

    except HTTPError as error:
        if error.code == 502:
            print("Network Error. Please try again")

        else:
            print("Error not recognized. Here is error HTTTP Error Code: ", error.code)

        exit(0)


def get_data(location, info):
    api = 'https://api.openweathermap.org/data/2.5/weather?'
    api_link = api + 'lat=' + str(location['lat']) + '&lon=' + str(location['lon']) + '&units=' + \
    info['report_unit'] + '&appid=' + info['api_key']

    try:
        weather_data = urllib.request.urlopen(api_link).read()
        weather_data = weather_data.decode("utf-8")
        weather = json.loads(weather_data)

        return weather

    except HTTPError as error:
        if error.code == 502:
            print("Network Error. Please try again")

        elif error.code == 401:
            print("OpenWeatherMap declined the request. Use '--status' option to check API key on file" \
                + "or '--help' to see instructions")

        else:
            print("Error not recognized. Here is error HTTTP Error Code: ", error.code)

        exit(0)


def save_config(settings):
    print("If you do not have an API key for OpenWeather then go to https://openweathermap.org/" \
    + " and sign up for one. Then enter you API key below.")

    api_key = input("Enter your API Key: ")
    print("The weather can reported in Farenheit, Celsius, or Kelvin\
    \nFor Kelvin enter 'standard', Celsius: 'metric', Fahrenheit: 'imperial'")

    unit = input("Enter desired weather unit: ")
    config = {'api_key' : api_key, 'report_unit' : unit}

    # this still needs more work
    with open(settings, 'w+') as file:
        output = json.dumps(config, indent = 4)
        file.write(output)


def load_config(settings):
    try:
        with open(settings, 'r') as file:
            config = json.load(file)

        return config

    except FileNotFoundError:
        print("Creating configuration file to store API key and settings\n")
        save_config(settings)
        load_config(settings)


# need find a better wait to format the output
def display_data(weather):
    print("Weather in", weather['name'], weather['sys']['country'], \
        "\nTemperature:", weather['main']['temp'], "F\nFeels Like:", weather['main']['feels_like'], "F")


def select_task(settings):
    args = sys.argv
    args.pop(0)
    if len(args) == 0:
        return None
    elif args[0] == '--help':
        print("Help Message and Instructions:")
        print("This is a Weather Utility. If you do not have an API key for OpenWeather then go to " \
        + "https://openweathermap.org/ and sign up for one.")
        print("To add your API Key and Configure your unit settings run 'python get_weather.py --config'")
        print("\nThank you to these free services that made this project possible:\n" \
        + "OpenWeather Map API: https://openweathermap.org/api\n" + "IP-API: https://ip-api.com/\n" \
        + "checkip: http://checkip.dyndns.org/")
        exit(0)

    elif args[0] == "--status":
        info = load_config(settings)
        print("From File:", settings)
        print("API Key in file is:", info['api_key'])
        print("Weather Data will be reported using", info['report_unit'], "units")
        exit(0)

    elif args[0] == "--config":
        save_config(settings)
        exit(0)

    else:
        print("The argument was not recognized. Try again.")
        print("arguments available:")
        print("Use '--help' to show intructions on using this utility\n" \
                + "Use '--config' to add an API key and configure the settings on file\n" \
                + "Use '--status' to check the current API key and settings on file")
        exit(0)


def main():
    settings = "backup.json"
    select_task(settings)
    weather_data = get_data(get_ip_location(), load_config(settings))
    display_data(weather_data)


if __name__ == '__main__':
    main()
