class FlightData:
    # This class is responsible for structuring the flight data.
    def __init__(self, locations: dict, dates: dict, codes: dict, prices: dict, stop_overs: int, via_city=""):
        """
        Constructor.
        This class defines objects which represent a flight
        from point A to B.
        :param locations: Destination and current location.
        :param dates: When does the flight leave.
        :param codes: IATA for each city airport.
        """
        self.dep = locations['dep_city']
        self.dest = locations['dest_city']
        self.dates = dates
        self.codes = codes
        self.prices = prices
        # Additional:
        self.stop_overs = stop_overs
        self.via_city = via_city

