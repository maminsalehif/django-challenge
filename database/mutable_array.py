from typing import Iterable

from sqlalchemy.ext.mutable import Mutable


class MutableList(Mutable, list):
    def append(self, value):
        list.append(self, value)
        self.changed()

    def extend(self, __iterable) -> None:
        list.extend(self, __iterable)
        self.changed()

    @classmethod
    def coerce(cls, key, value):
        if not isinstance(value, MutableList):
            if isinstance(value, list):
                return MutableList(value)
            return Mutable.coerce(key, value)
        else:
            return value
