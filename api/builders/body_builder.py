class BodyBuilder:
    def __init__(self):
        self._body = {}

    def set(self, key: str, value) -> "BodyBuilder":
        self._body[key] = value
        return self

    def build(self) -> dict:
        return self._body.copy()
