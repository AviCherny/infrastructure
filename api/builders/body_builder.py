class BodyBuilder:
    def __init__(self):
        self._body = {}

    def set(self, path: str, value) -> "BodyBuilder":
        keys = path.split(".")
        d = self._body
        for key in keys[:-1]:
            d = d.setdefault(key, {})
        d[keys[-1]] = value
        return self

    def build(self) -> dict:
        return self._body.copy()
