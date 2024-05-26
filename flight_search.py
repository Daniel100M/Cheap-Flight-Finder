import os
import requests

TEQUILA_API_KEY = os.environ['TEQ_API_KEY']

# For how long should I remain at the destination:
MIN_LEN_STAY = 7
MAX_LEN_STAY = 28

CURRENCY = "ILS"

class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.endpoint = 'https://api.tequila.kiwi.com'
        self.header = {
            "apikey": TEQUILA_API_KEY
        }

    def get_code(self, location_name: str) -> str:
        """
        Using the Tequila Locations API, acquires the
        code value (IATA) of specified city name.
        :return:
        """
        url = f"{self.endpoint}/locations/query"
        parameters = {
            "term": location_name,
            "locale": 'en-US',
            "location_types": 'city'
        }
        response = requests.get(url=url, headers=self.header, params=parameters)
        # print(response.status_code)
        # print(response.text)
        location_data = response.json()
        return location_data['locations'][0]['code']

    def get_flights_data(self, codes: dict, dates: dict) -> dict:
        """
        Using the Tequila Search API, acquires one-way or return itineraries (JSON Objects).
        Basically, gets info on flights from one specified city to another.
        :return: A dictionary (will be empty if API request failed).
        """
        search_url = f"{self.endpoint}/v2/search"
        parameters = {
            "fly_from": codes['dep_city'],
            "fly_to": codes['dest_city'],
            "date_from": dates['first'],
            "date_to": dates['last'],
            "nights_in_dst_from": MIN_LEN_STAY,
            "nights_in_dst_to": MAX_LEN_STAY,
            "one_for_city": 1,
            "max_stopovers": 1,
            "curr": CURRENCY
        }
        response = requests.get(url=search_url, params=parameters, headers=self.header)
        if response.status_code != 200:
            return {}
        # print(response.status_code)
        print(f"Flight Search Data:\n"
              f"{response.text}")
        return response.json()['data']
