from concurrent.futures import ThreadPoolExecutor
from threading import Lock


class BatchCounter:
    _instance = None
    _creation_lock = Lock()

    def __new__(cls):
        # ponytail: 每次构造都加锁；有性能证据时优先在入口创建后传递实例。
        with cls._creation_lock:
            if cls._instance is None:
                instance = super().__new__(cls)
                instance._value = 0
                instance._state_lock = Lock()
                cls._instance = instance
            return cls._instance

    def __init_subclass__(cls, **kwargs):
        raise TypeError("本教学单例不支持继承")

    def finish_batch(self) -> int:
        with self._state_lock:
            self._value += 1
            return self._value

    def value(self) -> int:
        with self._state_lock:
            return self._value


def demo() -> None:
    shared = BatchCounter()
    before = shared.value()

    def work(_: int) -> tuple[bool, int]:
        counter = BatchCounter()
        return counter is shared, counter.finish_batch()

    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(work, range(100)))

    same_instance = all(same for same, _ in results)
    numbers = sorted(number for _, number in results)
    if not same_instance or numbers != list(range(before + 1, before + 101)):
        raise AssertionError("实例唯一性或累计操作不正确")
    if BatchCounter().value() != before + 100:
        raise AssertionError("重复构造不应重置状态")
    print(f"所有线程拿到同一实例：{same_instance}")
    print(f"本轮累计完成批次：{shared.value() - before}")
    print("自检通过")


if __name__ == "__main__":
    demo()
