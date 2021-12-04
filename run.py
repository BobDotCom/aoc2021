import datetime
import time
import traceback

from aoc import AOC, compile_method_name

aoc = AOC()

for day in range(1, 26):
    if not hasattr(aoc, compile_method_name(day)):
        current_day = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-5))).day
        if current_day < day:
            raise AttributeError(f"Could't find code for day {day}. It looks like this puzzle hasn't been released yet."
                                 " Check back once it releases!")
        elif current_day == day:
            raise AttributeError(f"Could't find code for day {day}. It looks like this puzzle was just released today. "
                                 "Solutions to puzzles won't be updated until the day after it's released. Check back "
                                 "tomorrow!")
        elif current_day > day:
            try:
                raise AttributeError(f"Could't find code for day {day}. It looks like this puzzle has been released. "
                                     "Let the developers know to update the code!")
            except AttributeError:
                traceback.print_exc()
    start = time.perf_counter()
    out = aoc.run(day)
    end = time.perf_counter()

    print(f"Day {day}: {out} (Calculated in {(end - start) * 1000:.2f}ms)")
