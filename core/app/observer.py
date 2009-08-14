from __future__ import with_statement

class Observer:
    __datatypes__ = {}
    @staticmethod
    def register(name, pointer):
        Observer.__datatypes__[name] = pointer

    @staticmethod
    def list():
        return Observer.__datatypes__

    @staticmethod
    def get(name):
        if name in Observer.__datatypes__:
            return Observer.__datatypes__[name]
        else:
            return -1