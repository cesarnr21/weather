
# need to find API
# find the location, maybe using IP address, or find a way to get location
# figure out a way to add options when calling the python scrip

import sys

def create_target():
    args = sys.argv
    args.pop(0)
    if len(args) = 0:
        get_ip()
    else:
        pass # switch-function: https://www.geeksforgeeks.org/switch-case-in-python-replacement/
    pass

def get_location(target):
    """
    In case no location is selected, find the IP address location and use that instead
    """
    print(target)
    pass


def get_data(location):
    """
    Uses API to find weather data for the selected location
    """
    pass

def main():
    target_location = create_target()
    # target_location = input("Enter either a City or Zip Code to get weather information: ")
    target_location = get_location(target_location)
    get_data(target_location)

    # if there is no location selected use IP function to get location

if __name__ == '__main__':
    main()
