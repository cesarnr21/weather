
# need to find API
# find the location, maybe using IP address, or find a way to get location
# figure out a way to add options when calling the python scrip


def main():
    targetLocation = input("Enter either a City or Zip Code to get weather information: ")
    print(targetLocation)
    # if there is no location selected use IP function to get location


def getData():
    """
    Uses API to find weather data for the selected location
    """
    pass

def getLocation():
    """
    In case no location is selected, find the IP address location and use that instead
    """
    pass

if __name__ == '__main__':
    main()
