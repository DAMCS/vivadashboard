"""
Deals with all things GeoLocation
"""

from util.geolocation.geolocationutils import GeoLocationUtils
import requests

class GeoLocationAPI:
    """
    Class for handling all request for GeoLocation API
    """

    __GEOLOCATION_SECRET_KEY = "AIzaSyCk041GXSnc_GSUcdAQo6TBT7QVfGYkFC4"

    def __init__(self, location_url):
        self.location_url = location_url
        self.location_coords = GeoLocationUtils.get_coordinates_from_url(self.location_url)

    def get_city_from_location(self):
        """
        Method that performs the GET api request and returns the City
        """
        json_data = self.__perform_get_request()
        return self.__parse_json_data(json_data)

    def __parse_json_data(self, json_data):
        """
        Parses the JSON data from the GET request to get the address
        """
        if json_data['status'] != 'OK':
            raise Exception("API Call Failed. Status : {0}".format(json_data['status']))
        #  Find the address item with the address_type of localiy
        admin_area_level_2_node = None
        for address in json_data['results']:
            # Check locality
            if 'locality' in address['types']:
                # Get the address
                return address['address_components'][0]['long_name']
            if 'administrative_area_level_2' in address['types']:
                admin_area_level_2_node = address
        # If locality is not found then we look for administrative_area_level_1
        if admin_area_level_2_node != None:
            return admin_area_level_2_node['address_components'][0]['long_name']
        # If all else fails
        return json_data['results'][0]['address_components'][4]['long_name']

    def __perform_get_request(self):
        """
        Sends the GET request and returns the Result
        """
        response = requests.get(self.__build_api_url())
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("The GET Request failed with error code : {0}".format(
                response.status_code))

    def __build_api_url(self):
        """
        Creates the required url with the data embedded into the request.
        """
        url_str = "https://maps.googleapis.com/maps/api/geocode/json?latlng={0}&key={1}".format(
            self.location_coords,
            GeoLocationAPI.__GEOLOCATION_SECRET_KEY
        )
        return url_str

if __name__ == '__main__':
    # MY_LOC = GeoLocationAPI("https://www.google.co.in/maps/@11.0013284,77.0445327,16.75z?hl=en")
    MY_LOC = GeoLocationAPI("https://goo.gl/maps/7ECDXPFxo2S2")
    print(MY_LOC.location_coords)
    print(MY_LOC.get_city_from_location())
