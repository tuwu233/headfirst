from dataclasses import dataclass
from math import isfinite
from typing import Callable


@dataclass(frozen=True)
class Weather:
    temperature: float
    humidity: float


Observer = Callable[[Weather], None]


class WeatherStation:
    def __init__(self) -> None:
        self.latest: Weather | None = None
        self._observers: list[Observer] = []

    def subscribe(self, observer: Observer) -> None:
        if not callable(observer):
            raise TypeError("观察者必须可调用")
        if observer not in self._observers:
            self._observers.append(observer)

    def unsubscribe(self, observer: Observer) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def publish(self, temperature: float, humidity: float) -> None:
        if not isfinite(temperature) or not isfinite(humidity):
            raise ValueError("测量值必须是有限数")
        if not 0 <= humidity <= 100:
            raise ValueError("湿度必须在 0 到 100 之间")
        event = Weather(temperature, humidity)
        self.latest = event
        # ponytail: 单线程同步通知；需要并发发布时再设计队列与调度。
        for observer in tuple(self._observers):
            observer(event)


def demo() -> None:
    station = WeatherStation()
    screen: list[Weather] = []
    history: list[Weather] = []

    def show(weather: Weather) -> None:
        screen.append(weather)
        print(f"屏幕：{weather.temperature:.0f}°C / {weather.humidity:.0f}%")

    station.subscribe(show)
    station.subscribe(history.append)
    station.subscribe(show)  # 重复订阅不会重复通知。
    station.publish(25, 60)
    station.unsubscribe(show)
    station.publish(28, 65)

    if len(screen) != 1 or history != [Weather(25, 60), Weather(28, 65)]:
        raise AssertionError("订阅或退订行为不正确")
    try:
        station.publish(20, 101)
    except ValueError:
        pass
    else:
        raise AssertionError("必须拒绝非法湿度")
    if station.latest != Weather(28, 65):
        raise AssertionError("非法数据不应覆盖有效状态")
    print(f"历史记录：{len(history)} 条")
    print("自检通过")


if __name__ == "__main__":
    demo()
