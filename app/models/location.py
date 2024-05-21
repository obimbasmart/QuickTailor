

class Location:
    """Represents a geographical location
    """
    def __init__(self, state: str,
                 city: str, street: str) -> None:
        self.state = state
        self.city = city
        self.street = street