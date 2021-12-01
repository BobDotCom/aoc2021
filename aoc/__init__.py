import collections
import itertools
import os
from collections import UserDict
from typing import Optional, Dict


class Inputs(UserDict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_inputs()

    def load_inputs(self) -> None:
        for day in range(1, 26):
            input_data = self.load_day(day)
            if input_data:
                self[day] = input_data

    def load_day(self, day: int) -> Dict[int, str]:
        dirname = f"day-{day}"
        rel_path = os.path.join("inputs", dirname)
        abs_path = os.path.join(os.path.dirname(__file__), rel_path)
        data = {}
        if os.path.exists(abs_path):
            for filename in os.listdir(abs_path):
                if filename.startswith("part-") and filename.endswith(".txt") and filename[5:-4].isdigit():
                    part = int(filename[5:-4])
                    part_data = self.load_part(day, part)
                    if part_data:
                        data[part] = part_data
        return data

    @staticmethod
    def load_part(day: int, part: int) -> Optional[str]:
        filename = f"part-{part}.txt"
        dirname = f"day-{day}"
        rel_path = os.path.join("inputs", dirname, filename)
        abs_path = os.path.join(os.path.dirname(__file__), rel_path)
        if os.path.exists(abs_path):
            with open(abs_path) as f:
                return f.read()
        else:
            return None


def wrap_input(day, part):
    def wrap(func):
        def wrapper(self, *args, **kwargs):
            data = Inputs.load_part(day, part)
            return func(self, data, *args, **kwargs)
        return wrapper
    return wrap


def sliding_window(iterable, n):
    it = iter(iterable)
    window = collections.deque(itertools.islice(it, n), maxlen=n)
    if len(window) == n:
        yield tuple(window)
    for x in it:
        window.append(x)
        yield tuple(window)


class AOC:
    def __init__(self):
        self.inputs = Inputs()

    def run(self, day: int = None, part: Optional[int] = None, *args, **kwargs):
        return self.__getattribute__(f"day_{day}" + (f"_part_{part}" if part else ""))(*args, **kwargs)
