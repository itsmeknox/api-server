


class NoResponse(Exception):
    def __init__(self, description="Failed to send Request"):
        self.description = description
        super().__init__(description)



class HandledError(Exception):
    def __init__(self, message: str):
        self.message = message