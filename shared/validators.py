from abc import ABCMeta, abstractmethod

"""
Validators are based on python descriptors.
https://docs.python.org/3/howto/descriptor.html#custom-validators
"""


class Validator(metaclass=ABCMeta):

    def __set_name__(self, owner, name):
        self.private_name = '_' + name

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        self.validate(value)
        setattr(obj, self.private_name, value)

    @abstractmethod
    def validate(self, value): pass


class String(Validator):
    def __init__(self, minsize=None, maxsize=None, predicate=None):
        self.minsize = minsize
        self.maxsize = maxsize
        self.predicate = predicate

    def validate(self, value):
        # TODO change exception message, like this -> 'MinSizeValueError'
        if not isinstance(value, str):
            raise TypeError(f'Expected {value!r} to be an str')
        if self.minsize is not None and len(value) < self.minsize:
            raise ValueError(
                f'Expected {value!r} to be no smaller than {self.minsize!r}'
            )
        if self.maxsize is not None and len(value) > self.maxsize:
            raise ValueError(
                f'Expected {value!r} to be no bigger than {self.maxsize!r}'
            )
        if self.predicate is not None and not self.predicate(value):
            raise ValueError(
                f'Expected {self.predicate} to be true for {value!r}'
            )


class Number(Validator):

    def __init__(self, minvalue=None, maxvalue=None):
        self.minvalue = minvalue
        self.maxvalue = maxvalue

    def validate(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError(f'Expected {value!r} to be an int or float')
        if self.minvalue is not None and value < self.minvalue:
            raise ValueError(
                f'Expected {value!r} to be at least {self.minvalue!r}'
            )
        if self.maxvalue is not None and value > self.maxvalue:
            raise ValueError(
                f'Expected {value!r} to be no more than {self.maxvalue!r}'
            )


class List(Validator):
    def __init__(self, minlength=None, maxlength=None):
        self.minlength = minlength
        self.maxlength = maxlength

    def validate(self, value):
        if not isinstance(value, list):
            raise TypeError(f'Expected value to be an list')
        if self.minlength is not None and len(value) < self.minlength:
            raise ValueError(
                f'Expected list to be no smaller than {self.minlength!r}'
            )
        if self.maxlength is not None and len(value) > self.maxlength:
            raise ValueError(
                f'Expected list to be no bigger than {self.maxlength!r}'
            )


class Timestamp(Number):
    def __init__(self, **kwargs):
        super().__init__(minvalue=kwargs.pop('minvalue', 1), **kwargs)
