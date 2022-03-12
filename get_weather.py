
import sys
import json
import urllib.request

__version__ = '1.0'

def get_ip_location():
    """
    Get the users location using the IP address
    """
    ip_address = urllib.request.urlopen("http://checkip.dyndns.org").read() 
    ip_address = ip_address[-30:-16]
    ip_address = ip_address.decode("utf-8")
    print("IP Address is: " + ip_address)

    location_data = urllib.request.urlopen("http://ip-api.com/json/" + ip_address).read()
    location_data = location_data.decode("utf-8")
    location = json.loads(location_data)
    return location

def get_data(location, info):
    """
    Uses API to find weather data for the selected location
    """
    api = 'https://api.openweathermap.org/data/2.5/weather?'
    api_link = api + 'lat=' + str(location['lat']) + '&lon=' + str(location['lon']) + '&units=' + \
        info['report_unit'] + '&appid=' + info['api_key']
    weather_data = urllib.request.urlopen(api_link).read()
    weather_data = weather_data.decode("utf-8")
    weather = json.loads(weather_data)
    return weather

# add if config file is not created then call on save_config
def load_config():
    """
    Loads the data from the configuration file
    """
    #with open('testing.json', 'r') as file:
    with open('config.json', 'r') as file:
        config = json.load(file)
    return config

def save_config():
    """
    Allows the user to 
    """
    print("If you do not have an API key for OpenWeather then go to https://openweathermap.org/ \
        and sign up for a free API Key, then enter it below.")
    api_key = input("Enter your API Key: ")
    print("The weather can reported in Farenheit, Celsius, or Kelvin\
        \nFor Kelvin enter 'standard', Celsius: 'metric', Fahrenheit: 'imperial'")
    unit = input("Enter desired weather unit: ")
    #unit = 'imperial' # can also be either standard or metric
    config = {'api_key' : api_key, 'report_unit' : unit}
    # this still needs more work
    with open('config.json', 'w') as file:
        output = json.dumps(config, indent = 4)
        file.write(output)

# need find a better wait to format the output
def display_data(weather):
    print("Weather in", weather['name'], weather['sys']['country'], \
        "\nTemperature:", weather['main']['temp'], "F\nFeels Like: ", weather['main']['feels_like'], "F")

def select_task():
    args = sys.argv
    args.pop(0)
    if len(args) == 0:
        return None
    elif args[0] == '--help':
        print("Help Message and Instructions")
        exit(0)

    elif args[0] == "--status":
        info = load_config()
        print("API Key in file is: " + info['api_key'])
        print("Weather Data will be reported using " + info['report_unit'] + " units")
        exit(0)

    elif args[0] == "--config":
        save_config()
        exit(0)

    else:
        print(args[0], "command not avialable. Try again.")
        exit(0)

def main():
    select_task()
    weather_data = get_data(get_ip_location(), load_config())
    display_data(weather_data)

if __name__ == '__main__':
    main()
