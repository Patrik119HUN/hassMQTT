class TopicBuilder:
    _list: list[str] = []

    def __init__(self) -> None:
        self._list = list()
        pass

    def add(self, value: str):
        self._list.append(value)
        return self

    def single_level(self):
        self._list += "+"
        return self

    def multi_level(self):
        self._list += "#"
        return self

    def __str__(self) -> str:
        temp: str = ""
        for x in self._list:
            temp += x + "/"
        return temp


if __name__ == "__main__":
    valami = TopicBuilder()
    valami.add("alma").multi_level()
    print(valami)
