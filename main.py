# This file will need to use the DataManager,FlightSearch,
# FlightData, NotificationManager classes to achieve the
# program requirements.
from data_manager import DataManager
from flight_data import FlightData
from flight_gui import FlightGUI
from flight_search import FlightSearch
from notification_manager import NotificationManager
from datetime import datetime, timedelta


def get_dates() -> dict:
    """
    Grabs two dates:
    Today, and six months from today.
    :return:
    """
    today = datetime.now()
    # Grabbing the date in six months.
    future = today + timedelta(days=180)
    return {
        "first": today.strftime(format="%d/%m/%Y"),
        "last": future.strftime(format="%d/%m/%Y")
    }


DATES = get_dates()
print(DATES)

data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()

DEPARTURE_CITY = "Tel Aviv"
DEPARTURE_CITY_CODE = flight_search.get_code(DEPARTURE_CITY)

DESTINATIONS = data_manager.get_destinations()  # A list of all destination cities.
if not DESTINATIONS:
    DESTINATIONS = ["Paris", "London", "Rome"]
print(f"Destinations: {DESTINATIONS}")


def get_destination_codes() -> str:
    """
    Constructs a string of IATA codes, separated by commas.
    :return:
    """
    codes_str = ""
    for dest in DESTINATIONS:
        codes_str += f"{flight_search.get_code(dest)},"
    last_pos = len(codes_str) - 1

    print(f"City codes: '{codes_str[:last_pos]}'")
    return codes_str[:last_pos]


def create_flight_objects() -> list:
    """
    Creates a list of flights to all destinations.
    In case of some error, the list will be empty.
    :return:
    """
    flight_objects = []

    codes = {
        "dep_city": DEPARTURE_CITY_CODE,
        "dest_city": get_destination_codes()
    }

    data = flight_search.get_flights_data(codes, DATES)  # JSON response from search API.

    for item in data:
        # Creating a flight data object for each itinerary.
        locations = {
            "dep_city": item['cityFrom'],
            "dest_city": item['cityTo']
        }
        dates = {
            "dep": item['local_departure'].split('T')[0],
            "arrival": item['local_arrival'].split('T')[0]
        }
        prices = {
            "current": item['price'],
            "lowest": item['price']
        }
        # Grabbing the lowest price from spreadsheet:
        lowest_price = data_manager.get_lowest_price(item['cityTo'])
        if lowest_price != -1:
            prices['lowest'] = lowest_price

        codes['dest_city'] = item['cityCodeTo']

        # Checking for any additional stops before arriving at destination:

        flight_data = FlightData(locations, dates, codes, prices, item['technical_stops'])  # Creating the object.

        flight_objects.append(flight_data)
        print(f"Flight object: {flight_data.dest}, completed.")

    return flight_objects


def populate_spreadsheet(flight_objects: list):
    """
    Populates spreadsheet with up-to-date data.
    :return:
    """
    print("\nPopulating spreadsheet...\n")
    for flight in flight_objects:
        data_manager.update_row(flight.dest, flight.codes['dest_city'], flight.prices)


def check_prices(flight_objects: list):
    """
    Compares prices of each flight.
    Sends SMS if and only if price is cheaper than usual.
    :param flight_objects:
    :return:
    """
    for flight in flight_objects:
        if flight.prices['current'] <= flight.prices['lowest']:
            # Cheaper than usual.
            text = ("\n\nLow Price Alert!\n\n"
                    f"Fly from: {flight.dep}-{flight.codes['dep_city']}\n"
                    f"To: {flight.dest}-{flight.codes['dest_city']}"
                    f"\n\nDeparture Dates:\n"
                    f"From - {flight.dates['first']}\n"
                    f"To - {flight.dates['last']}"
                    f"\n\nFor only: {flight.prices}")
            # Send the notification:
            print(f"Sending text for {flight.dest}")
            # sms_manager.send_sms(body=text)


flights = create_flight_objects()
# populate_spreadsheet(flights)
# check_prices(flights)
flight_gui = FlightGUI(data_manager, notification_manager, flights)
