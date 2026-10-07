from dataclasses import dataclass
from typing import Protocol


class Beverage(Protocol):
    def description(self) -> str: ...
    def cost(self) -> int: ...  # 金额单位：分。


class Espresso:
    def description(self) -> str:
        return "浓缩咖啡"

    def cost(self) -> int:
        return 1800


@dataclass(frozen=True)
class Mocha:
    beverage: Beverage

    def description(self) -> str:
        return self.beverage.description() + " + 摩卡"

    def cost(self) -> int:
        return self.beverage.cost() + 300


@dataclass(frozen=True)
class Whip:
    beverage: Beverage

    def description(self) -> str:
        return self.beverage.description() + " + 奶泡"

    def cost(self) -> int:
        return self.beverage.cost() + 200


def demo() -> None:
    base = Espresso()
    drink: Beverage = Whip(Mocha(Mocha(base)))
    expected_name = "浓缩咖啡 + 摩卡 + 摩卡 + 奶泡"
    if drink.cost() != 2600 or drink.description() != expected_name:
        raise AssertionError("包装链计算错误")
    if base.cost() != 1800:
        raise AssertionError("包装不应修改基础饮料")
    print(drink.description())
    print(f"价格：{drink.cost() / 100:.2f} 元")
    print("自检通过")


if __name__ == "__main__":
    demo()
