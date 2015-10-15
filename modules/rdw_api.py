import requests


class RdwApi(object):
    """A class that can be used to retrieve information about a car using a numberplate
    It needs to be initialized with a api token to connect with the government API.

    Attributes:
        api_token   The token used to connect with the government API
        url         The url that directs to one of the government API endpoints
    """
    api_token = ''
    url = 'http://overheid.io/api/voertuiggegevens/'

    def __init__(self, token=None):
        """Initialize the class with given the token

        :param token:
        """
        self.api_token = token

    def request_information(self, number_plate=None):
        """Request the information from the government API based on the given number plate

        :param number_plate:
        :return:
            If the numberplate was invalid
             return 'no data found'
            Else
             return the json object with a added field if the vehicle is allowed or not
        """
        request = requests.get(self.url+number_plate, {'ovio-api-key': self.api_token})
        json = request.json()

        if 'headers' in json:
            return "No data found"

        json['parkerentoegestaan'] = 'Ja' if self.vehicle_allowed(json) else "nee"
        return json

    def vehicle_allowed(self, information=None):
        """Returns if the vehicle is allowed drive in this area based on fuel and date of first issue

        :param information:
        :return:
            False if not allowed
            True if allowed
        """
        date_of_first_issue = information['datumeersteafgiftenederland']
        year_of_first_issue = int(date_of_first_issue.split('-')[0])
        fuel = information['hoofdbrandstof']

        if year_of_first_issue < 2001 and fuel == 'Diesel':
            return False
        else:
            return True
