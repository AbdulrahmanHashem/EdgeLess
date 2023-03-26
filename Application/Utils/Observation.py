import time


class Observable(object):
    def __init__(self):
        super().__init__()
        self._observers = []
        self._value = None
        # self.context = context

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        for obs in self._observers:
            obs(new=self._value)

    def add_observer(self, observer):
        self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def remove_all_observers(self):
        self._observers.clear()


# # Test
# do = Observable()
# do.value = False
# do.add_observer(lambda e: print("5") if not e else print(2))
#
# do.value = True
