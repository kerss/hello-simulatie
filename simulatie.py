from model import *
from observer import *
from typing import List
import math


class SimulatieResultaat(dict):
    def tijdstippen(self) -> List[float]:
        return self.get('t')

    def toestanden(self) -> List[float]:
        return self.get('toestanden')

    def signalen(self) -> List[float]:
        return self.get('signalen')


class Simulatie:
    def __init__(
            self,
            simulatie_objecten: List[DynamischModel] = None,
            signaal_observers: List[SignaalObserver] = None,
            t0=0.,
            lengte=1.,
            dt=.01
    ):
        self.t = t0
        self.dt = dt
        self.lengte = lengte

        self.simulatie_objecten = simulatie_objecten or []
        self.signaal_observers = signaal_observers or []

    def simulatie_stap(self):
        self.t += self.dt
        [sim_obj.step_dt(self.dt) for sim_obj in self.simulatie_objecten]
        [sgn_obs.step_dt(self.dt) for sgn_obs in self.signaal_observers]

    def simuleer(self) -> SimulatieResultaat:
        ts, ys, yests = [], [], []
        t_start = self.t

        ts.append(self.t)
        ys += [sim_obj.toestand() for sim_obj in self.simulatie_objecten]
        yests += [sgn_observer.signaal() for sgn_observer in self.signaal_observers]

        while self.t < t_start + self.lengte:
            self.simulatie_stap()

            ts.append(self.t)
            ys += [sim_obj.toestand() for sim_obj in self.simulatie_objecten]
            yests += [sgn_observer.signaal() for sgn_observer in self.signaal_observers]

        return SimulatieResultaat({
            't': ts,
            'toestanden': ys,
            'signalen': yests,
        })


# from scipy.io import loadmat
# class SimInput(DynamischModel):
#     def __init__(self, file: str):
#         mat_data = loadmat(file)
#         self.data_t = mat_data.get('pulse_t')
#         self.pulse_dt = mat_data.get('pulse_dt')
#
#         self.idx = 0
#         self.t = 0.
#
#     # Returns tijdstip van laatste pulse
#     def toestand(self) -> float:
#         return self.data_t[self.idx][0]
#
#     def step_dt(self, dt: float):
#         self.t += dt
#         if self.t > self.data_t[self.idx]:
#             self.idx += 1
