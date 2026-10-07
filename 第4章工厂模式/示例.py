from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Protocol


@dataclass(frozen=True)
class Dough:
    name: str


@dataclass(frozen=True)
class Sauce:
    name: str


@dataclass
class Pizza:
    name: str
    dough: Dough
    sauce: Sauce
    steps: list[str] = field(default_factory=list)


# 1. 简单工厂：创建选择集中在一个函数中。
def simple_factory(kind: str) -> Pizza:
    if kind == "cheese":
        return Pizza("芝士比萨", Dough("普通面团"), Sauce("番茄酱"))
    if kind == "veggie":
        return Pizza("素食比萨", Dough("普通面团"), Sauce("番茄酱"))
    raise ValueError(f"不支持的比萨类型：{kind}")


# 2. 工厂方法：子类创建，父类使用产品完成共同流程。
class PizzaStore(ABC):
    def order_pizza(self) -> Pizza:
        pizza = self.create_pizza()
        pizza.steps.extend(["准备", "烘焙", "切片", "装盒"])
        return pizza

    @abstractmethod
    def create_pizza(self) -> Pizza:
        raise NotImplementedError


class NYStore(PizzaStore):
    def create_pizza(self) -> Pizza:
        return Pizza("纽约芝士比萨", Dough("薄饼面团"), Sauce("番茄酱"))


class ChicagoStore(PizzaStore):
    def create_pizza(self) -> Pizza:
        return Pizza("芝加哥芝士比萨", Dough("厚饼面团"), Sauce("李子番茄酱"))


# 3. 抽象工厂：客户向一个工厂索取相互匹配的产品家族。
class IngredientFactory(Protocol):
    def create_dough(self) -> Dough: ...
    def create_sauce(self) -> Sauce: ...


class NYIngredients:
    def create_dough(self) -> Dough:
        return Dough("薄饼面团")

    def create_sauce(self) -> Sauce:
        return Sauce("番茄酱")


class ChicagoIngredients:
    def create_dough(self) -> Dough:
        return Dough("厚饼面团")

    def create_sauce(self) -> Sauce:
        return Sauce("李子番茄酱")


def make_regional_pizza(factory: IngredientFactory) -> Pizza:
    return Pizza("地区比萨", factory.create_dough(), factory.create_sauce())


def demo() -> None:
    simple = simple_factory("cheese")
    veggie = simple_factory("veggie")
    ny = NYStore().order_pizza()
    chicago = ChicagoStore().order_pizza()
    family_ny = make_regional_pizza(NYIngredients())
    family_chicago = make_regional_pizza(ChicagoIngredients())
    checks = [
        simple.name == "芝士比萨",
        veggie.name == "素食比萨",
        ny.name == "纽约芝士比萨",
        chicago.name == "芝加哥芝士比萨",
        ny.steps == chicago.steps == ["准备", "烘焙", "切片", "装盒"],
        (family_ny.dough.name, family_ny.sauce.name) == ("薄饼面团", "番茄酱"),
        (family_chicago.dough.name, family_chicago.sauce.name)
        == ("厚饼面团", "李子番茄酱"),
    ]
    if not all(checks):
        raise AssertionError("工厂产品或流程不正确")
    try:
        simple_factory("unknown")
    except ValueError:
        pass
    else:
        raise AssertionError("未知类型应该明确失败")
    print("简单工厂：", simple.name, sep="")
    print("工厂方法：", ny.name, " / ", chicago.name, sep="")
    print("共同流程：", " → ".join(ny.steps), sep="")
    print("抽象工厂：", family_chicago.dough.name, " + ", family_chicago.sauce.name, sep="")
    print("自检通过")


if __name__ == "__main__":
    demo()
