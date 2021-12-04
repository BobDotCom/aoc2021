import math
import os
from collections import UserDict
from typing import Optional, Dict

from .helpers import *


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


def compile_method_name(day: int = None, part: Optional[int] = None):
    return f"day_{day}" + (f"_part_{part}" if part else "")


class AOC:
    def __init__(self):
        self.inputs = Inputs()

    def run(self, day: int = None, part: Optional[int] = None, *args, **kwargs):
        return self.__getattribute__(compile_method_name(day, part))(*args, **kwargs)

    @wrap_input(1, 1)
    def day_1_part_1(self, data: str) -> int:
        """Day 1: Sonar Sweep - Part 1

        We need to count the number of times a measurement increases from the previous measurement, and return the sum
        of that count.

        .. code-block::

            199 (N/A - no previous measurement)
            200 (increased)
            208 (increased)
            210 (increased)
            200 (decreased)
            207 (increased)
            240 (increased)
            269 (increased)
            260 (decreased)
            263 (increased)

        In this example, there are 7 measurements that are larger than the previous measurement.

        Parameters
        ----------
        data: str
            The input data.

        Returns
        -------
        int
            The sum of the number of measurements that are larger than the previous measurement.
        """
        data = data.strip().splitlines()
        return sum(int(x) > int(y) for x, y in zip(data[1:], data))

    @wrap_input(1, 1)
    def day_1_part_2(self, data: str) -> int:
        """Day 1: Sonar Sweep - Part 2

        We need to do the same thing as before, but use a sliding window of size 3, and compare those groups.

        .. code-block::

            199  A
            200  A B
            208  A B C
            210    B C D
            200  E   C D
            207  E F   D
            240  E F G
            269    F G H
            260      G H
            263        H

        .. code-block::

            A: 607 (N/A - no previous sum)
            B: 618 (increased)
            C: 618 (no change)
            D: 617 (decreased)
            E: 647 (increased)
            F: 716 (increased)
            G: 769 (increased)
            H: 792 (increased)

        In this example, there are 5 sums that are larger than the previous sum.

        Parameters
        ----------
        data: str
            The input data.

        Returns
        -------
        int
            The sum of the number of sums that are larger than the previous sum.
        """

        data = [sum(int(i) for i in win) for win in Day1.triplewise(data.strip().splitlines())]

        return sum(int(x) > int(y) for x, y in zip(data[1:], data))

    def day_1(self):
        # noinspection PyArgumentList
        return self.day_1_part_1(), self.day_1_part_2()

    @wrap_input(2, 1)
    def day_2_part_1(self, data: str) -> int:
        """Day 2: Dive! - Part 1


        """
        data = data.strip().splitlines()

        position = {
            "horizontal": 0,
            "vertical": 0,
        }

        for entry in data:
            action, amount = entry.split()
            match action:
                case "forward":
                    position["horizontal"] += int(amount)
                case "down":
                    position["vertical"] += int(amount)
                case "up":
                    position["vertical"] -= int(amount)

        return math.prod(position.values())

    @wrap_input(2, 1)
    def day_2_part_2(self, data: str) -> int:
        """Day 2: Dive! - Part 2
        """
        data = data.strip().splitlines()

        position = {
            "horizontal": 0,
            "vertical": 0,
            "aim": 0,
        }

        for entry in data:
            action, amount = entry.split()
            match action:
                case "down":
                    position["aim"] += int(amount)
                case "up":
                    position["aim"] -= int(amount)
                case "forward":
                    position["horizontal"] += int(amount)
                    position["vertical"] += position["aim"] * int(amount)

        del position["aim"]

        return math.prod(position.values())

    def day_2(self):
        # noinspection PyArgumentList
        return self.day_2_part_1(), self.day_2_part_2()

    @wrap_input(3, 1)
    def day_3_part_1(self, data: str) -> int:
        """Day 3: Binary Diagnostic - Part 1
        """
        data = data.strip().splitlines()
        gamma = Day3.gamma(data)
        epsilon = Day3.epsilon(data)

        return Day3.to_decimal(gamma) * Day3.to_decimal(epsilon)

    @wrap_input(3, 1)
    def day_3_part_2(self, data: str) -> int:
        """Day 3: Binary Diagnostic - Part 2
        """
        data = data.strip().splitlines()

        oxygen_rating = Day3.check_criteria(data, Day3.Rating.OXYGEN)
        co2_rating = Day3.check_criteria(data, Day3.Rating.CO2)

        return Day3.to_decimal(oxygen_rating) * Day3.to_decimal(co2_rating)

    def day_3(self):
        # noinspection PyArgumentList
        return self.day_3_part_1(), self.day_3_part_2()
