import requests

from util.geolocation.phantomjsdriver import PhantomJSDriver

class GeoLocationUtils:
    """
    Static helper methods for Geolocation classs
    """
    @staticmethod
    def get_coordinates_from_url(url):
        """
        Method to retrieve the coordinates from the given url string.
        Args
        param: url 'str' URL
        :return: string Coordinates in the URL
        """
        url = GeoLocationUtils.get_base_url(url)
        at_location = url.find('@')
        if -1 == at_location:
            raise Exception("Geolocation URL does not contain the coordinates identified by @.")
        at_location += 1
        next_comma_loc = url.find(',', at_location)
        end_location = url.find(',', next_comma_loc + 1)
        return url[at_location: end_location]

    @staticmethod
    def get_base_url(url):
        """
        Follows the various redirects to find a base url.
        Something to do with URL shortening
        """
        if 'maps' in url:
            # Special situation in which a JS redirect is present
            url = PhantomJSDriver().get_final_url(url)
            return url

        while True:
            prev_url = url
            response = requests.head(url)
            # Response with a 30x is a redirect response.
            # Check the Location header for the actual url.
            if response.status_code >= 300 and response.status_code < 310:
                url = response.headers['Location']
            if url == prev_url:
                break
        print("Ending URL : {0}".format(url))
        return url
