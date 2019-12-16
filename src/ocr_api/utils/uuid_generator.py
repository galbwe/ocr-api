from uuid import uuid4

class UuidGenerator:
    def __init__(self):
        self._generate_uuid = uuid4

    def __next__(self):
        return str(self._generate_uuid())
