from random import random


class SignaalObserver(object):
    def signaal(self) -> float:
        return .0

    def step_dt(self, dt: float):
        pass


class SignaalRuis(float):
    def white_noise(self) -> float:
        return (self * (random() - .5))