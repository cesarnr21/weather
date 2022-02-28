
import sys
import configparser
import json
import urllib.request

__version__ = '1.0'

def get_ip_location():
    """
    In case no location is selected, find the IP address location and use that instead
    """
    url = "http://checkip.dyndns.org"
    ip_address = urllib.request.urlopen(url).read()
    ip_address = ip_address[-30:-16]
    return(ip_address)


def get_data(location, api_key, unit):
    """
    Uses API to find weather data for the selected location
    """
    api = 'http://api.openweathermap.org/data/2.5/forecast?id=524901&appid='
    api_link = api + api_key + str(location) + unit
    urllib.request.urlopen(api_link)
    pass

def load_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    api_key = config.get('DEFAULT', 'api_key')
    unit = config.get('DEFAULT', 'report_unit')
    info = [api_key, unit]
    return info

def save_config():
    print("Go to https://openweathermap.org/ and sign up for a free API Key.\n \
    Afterwards enter it below.")
    api_key = input("Enter your API Key:")

    # need to make changes to unit selection
    unit = 'f'
    config = configparser.ConfigParser()
    config['DEFAULT'] = {'api_key': api_key,
                         'report_unit': unit}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def print_data():
    print("Weather in <insert location> \nTemperature: \n Temperature Feels Like: ")

def create_task():
    args = sys.argv
    args.pop(0)
    if len(args) == 0:
        target = get_ip_location()
    else:
        def command_select(input):
            def help():
                print("Help Message and Instructions")
                exit(0)

            def status():
                info = load_config()
                print("API Key in file is " + info[0])
                exit(0)

            def config():
                save_config()
                exit(0)

            commands = { "--help" : help,
                         "--status" : status,
                         "--config" : config,
            }

            return commands.get(input, "Unknown Command, available commands: --help --config")

        command_select(args)
    return target

def main():
    target_location = create_task()
    # target_location = input("Enter either a City or Zip Code to get weather information: ")
    get_data(target_location, load_config())

    # if there is no location selected use IP function to get location

if __name__ == '__main__':
    main()
