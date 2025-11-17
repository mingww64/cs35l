import re


class Location:
    """Represents a geographic location with city, state, and country.
    
    Validates location format: "City, ST, CC" where:
    - City: alphabetic characters
    - ST: 2-letter uppercase state code
    - CC: 2-letter uppercase country code
    """
    def __init__(self, city: str, state: str, country: str):
        """Initialize a Location instance.
        
        Args:
            city: City name (alphabetic)
            state: 2-letter uppercase state code
            country: 2-letter uppercase country code
        """
        self.city = city
        self.state = state
        self.country = country
        
    def valid_location(self) -> bool:
        """Validate location format matches expected pattern.
        
        Format must be: "City, ST, CC" (e.g., "LosAngeles, CA, US")
        
        Returns:
            True if location format is valid, False otherwise
        """
        pattern = r"^(?P<city>[a-zA-Z]+), (?P<state>[A-Z]{2}), (?P<country>[A-Z]{2})$"
        location_string = f"{self.city}, {self.state}, {self.country}"
        return re.fullmatch(pattern, location_string) is not None