import os

import requests


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.endpoint = os.environ['SHEETY_ENDPOINT']
        self.header = {
            "Authorization": f"Bearer {os.environ['SECRET_TOKEN']}"
        }

# --------------------- USER SPREADSHEET FUNCTIONS ------------------------------
    def add_row(self, first_name: str, last_name: str, email: str) -> bool:
        """
        Applicable to the user spreadsheet.
        :return: True if the request was successful, False otherwise.
        """
        parameters = {
            "user": {
                "firstName": first_name,
                "lastName": last_name,
                "email": email
            }
        }
        response = requests.post(url=f"{self.endpoint}/users",
                                 headers=self.header,
                                 params=parameters)
        print(response.text)
        return response.status_code == 200

    def get_users_data(self) -> dict:
        """
        Retrieves all rows from the users spreadsheet.
        :return: A dictionary (will be empty if API request failed).
        """
        response = requests.get(url=f"{self.endpoint}/users", headers=self.header)
        if response.status_code == 200:
            return response.json()['users']

        print(f"Invalid request:\n"
              f"{response.text}")
        return {}
# ----------------------- PRICES SPREADSHEET FUNCTIONS --------------------------

    def update_row(self, city_name: str, airport_code: str, prices: dict):
        """
        Modifies a row in the spreadsheet.
        :param airport_code: IATA Code.
        :param prices:
        :param city_name:
        :return:
        """
        body = {
            "price": {
                "city": city_name,
                "iataCode": airport_code,
                "lowestPrice": prices['lowest'],
                "currentPrice": prices['current'],
            }
        }
        row_num = self.get_row_id(city_name)
        response = requests.put(url=f"{self.endpoint}/prices/{row_num}", json=body, headers=self.header)
        response.raise_for_status()
        # print(response.text)

    def get_prices_data(self) -> dict:
        """
        Retrieves all rows from prices spreadsheet.
        :return:
        """
        response = requests.get(url=f"{self.endpoint}/prices", headers=self.header)
        if response.status_code != 200:
            print(f"Invalid request:\n"
                  f" {response.text}")
            return {}
        data = response.json()
        return data['prices']

    def get_row_data(self, city_name: str) -> dict:
        """
        Grabs an entry in the spreadsheet based on the city name specified.
        If no entry corresponds to that city, an empty dictionary will be
        returned instead.
        :param city_name:
        :return:
        """
        rows_data = self.get_prices_data()
        for item in rows_data:
            if item['city'] == city_name:
                return item
        return {}

    def get_lowest_price(self, city_name: str) -> int:
        """
        Retrieves (from spreadsheet) the lowest price of a city.
        :return: The lowest price of a flight ticket, or -1 to indicate an error.
        """
        item = self.get_row_data(city_name)
        if ((item == {}) or ('lowestPrice' not in item.keys())) or (item['lowestPrice'] == ''):
            return -1
        return int(item['lowestPrice'])

    def get_row_id(self, city_name: str) -> int:
        """
        Retrieves the row number (integer) based on given city name.
        :param city_name:
        :return: The row id, or -1 if specified city isn't found.
        """
        item = self.get_row_data(city_name)
        if item == {}:
            return -1
        return item['id']

    def get_destinations(self) -> list:
        """
        Grabs names of cities from spreadsheet.
        :return:
        """
        sheet_data = self.get_prices_data()
        return [row['city'] for row in sheet_data]
