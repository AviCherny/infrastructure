class BodyBuilder:
    def __init__(self):
        self._body = {}

    def set(self, key: str, value) -> "BodyBuilder":
        self._body[key] = value
        return self

    def build(self) -> dict:
        return {
            key: value.build() if isinstance(value, BodyBuilder) else value
            for key, value in self._body.items()
        }
