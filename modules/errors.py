class UnauthorizedSignature(Exception):
    def __init__(self, description):
        self.description = description
        super().__init__(description)

class UnauthorizedAccess(Exception):
    def __init__(self, description):
        self.description = description
        super().__init__(description)

class RequestFailed(Exception):
    def __init__(self, description):
        self.description = description
        super().__init__(description)


class Unauthorized(Exception):
    def __init__(self, description):
        self.description = description
        super().__init__(description)

