from dataclasses import dataclass
from typing import Callable

Behavior = Callable[[], str]


def fly_with_wings() -> str:
    return "用翅膀飞行"


def fly_no_way() -> str:
    return "不会飞"


def fly_with_rocket() -> str:
    return "用火箭飞行"


def quack() -> str:
    return "嘎嘎叫"


def squeak() -> str:
    return "吱吱叫"


@dataclass
class Duck:
    name: str
    fly_behavior: Behavior
    quack_behavior: Behavior

    def perform_fly(self) -> str:
        return self.fly_behavior()

    def perform_quack(self) -> str:
        return self.quack_behavior()


def demo() -> None:
    mallard = Duck("绿头鸭", fly_with_wings, quack)
    model = Duck("模型鸭", fly_no_way, squeak)
    before = model.perform_fly()
    model.fly_behavior = fly_with_rocket
    after = model.perform_fly()

    actual = (mallard.perform_fly(), before, after, model.perform_quack())
    expected = ("用翅膀飞行", "不会飞", "用火箭飞行", "吱吱叫")
    if actual != expected:
        raise AssertionError(actual)
    print("绿头鸭：", actual[0], sep="")
    print("模型鸭换装前：", before, sep="")
    print("模型鸭换装后：", after, sep="")
    print("模型鸭叫声：", actual[3], sep="")
    print("自检通过")


if __name__ == "__main__":
    demo()
