import itertools
from enum import Enum
from typing import List, Iterable, Union


class Day1:
    @staticmethod
    def triplewise(iterable):
        for (a, _), (b, c) in itertools.pairwise(itertools.pairwise(iterable)):
            yield a, b, c


class Day3:
    class Rating(Enum):
        """Enum for rating"""
        OXYGEN = 0
        CO2 = 1

        def convert(self, data, index=None):
            if self.name == "OXYGEN":
                return Day3.gamma_at(data, index)
            elif self.name == "CO2":
                return Day3.epsilon_at(data, index)
            else:
                raise RuntimeError("Unknown rating")

    @staticmethod
    def chunk(data: Iterable[str]):
        return (tuple(map(lambda value: bool(int(value)), chunk)) for chunk in zip(*data))

    @classmethod
    def gamma(cls, data: Iterable[str]) -> str:
        """Most common bit for each column"""
        return "".join(map(lambda chunk: str(int(chunk.count(True) >= chunk.count(False))), cls.chunk(data)))

    @classmethod
    def gamma_at(cls, data: Iterable[str], index) -> str:
        """Most common bit at index"""
        return cls.gamma((value[index] for value in data))

    @classmethod
    def epsilon_at(cls, data: Iterable[str], index) -> str:
        """Inverse of gamma at index"""
        return cls.epsilon((value[index] for value in data))

    @classmethod
    def epsilon(cls, data: Iterable[str]) -> str:
        """Inverse of gamma"""
        return "".join(map(lambda chunk: str(int(chunk.count(False) > chunk.count(True))), cls.chunk(data)))

    @staticmethod
    def to_decimal(value_in: str) -> int:
        """Convert binary to decimal"""
        return int(value_in, 2)

    @classmethod
    def check_criteria(cls, data: Union[Iterable[str], List[str]], target_type: Rating, index=-1) -> str:
        """Find an entry that matches the criteria"""
        index += 1
        if len(data) == 1 or index == len(data[0]):
            return data[0]
        else:
            target = target_type.convert(data, index)
            return cls.check_criteria(tuple(value for value in data if value[index] == target), target_type, index)
