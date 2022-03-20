from simulatie import *
from scipy.io import loadmat


class EncoderData:
    def __init__(self):
        mat_data = loadmat('data/pulses.mat')
        self.data_t = mat_data.get('pulse_t')
        self.pulse_dt = mat_data.get('pulse_dt')


class FixedTijdSensor(SignaalObserver):
    def __init__(self, encoder_data: EncoderData, delta_tijd=0.01):
        self.encoder_data = encoder_data
        self.delta_tijd = delta_tijd

        self.t = 0.
        self.idx = 0
        self.nr_pulses = 0.

    def signaal(self) -> float:
        return self.nr_pulses

    def step_dt(self, dt: float):
        nr_pulses = 0
        self.t += self.delta_tijd

        for t in self.encoder_data.data_t[self.idx:]:
            if t < self.t:
                nr_pulses += 1
            else:
                break

        self.idx += nr_pulses
        self.nr_pulses = float(nr_pulses)


class FixedPulsesSensor(SignaalObserver):
    def __init__(self, encoder_data: EncoderData, fixed_pulses=4):
        self.encoder_data = encoder_data
        self.pulse_buf = [None] * fixed_pulses
        self.t = 0.
        self.idx = 0

    def signaal(self) -> float:
        try:
            return sum(self.pulse_buf) / len(self.pulse_buf)
        except TypeError:
            return .0

    def step_dt(self, dt: float):
        self.t += dt
        idx = self.idx

        try:
            for t, pulse_dt in zip(self.encoder_data.data_t[idx:], self.encoder_data.pulse_dt[idx:]):
                if t < self.t:
                    self.pulse_buf.pop(0)
                    self.pulse_buf.append(pulse_dt[0])
                    self.idx += 1
                else:
                    break
        except IndexError:
            pass


def test_example() -> SimulatieResultaat:
    fs = 100

    encoder_data = EncoderData()
    fixed_tijd_sensor = FixedTijdSensor(encoder_data, delta_tijd=1/fs)
    fixed_pulses_sensor = FixedPulsesSensor(encoder_data, fixed_pulses=4)

    simulatie = Simulatie(
        signaal_observers=[fixed_pulses_sensor],
        lengte=5.,
        dt=float(1/fs)
    )

    return simulatie.simuleer()

if __name__ == '__main__':
    resultaat = test_example()

    print(resultaat.tijdstippen())
    # print(resultaat.toestanden())
    print(resultaat.signalen())
    #
    # print(simulatie.signaal_observers[0].pulse_window)