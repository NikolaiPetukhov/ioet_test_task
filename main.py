import argparse

from collections import namedtuple


Timeframe = namedtuple("Timeframe", ["day", "start", "finish"])


class CorruptedDataException(Exception):
    def __init__(self, line_n, line):
        self.line_n = line_n
        self.line = line
        msg = (
            f'[ERROR] Input file data corrupted on line {line_n}: "{line}"\n'
            'Example: "RENE=MO10:00-12:00,TU10:00-12:00"'
        )
        super().__init__(msg)


class WrongTimeException(Exception):
    def __init__(self, line_n=None, line=""):
        self.line_n = line_n
        self.line = line
        msg = "[ERROR] Wrong time"
        if line_n or line:
            msg = msg + " on line"
        if line_n:
            msg = msg + f" {line_n}"
        if line:
            msg = msg + f': "{line}"'
        msg = msg + '\nExample: "RENE=MO10:00-12:00,TU13:00-18:00"'
        super().__init__(msg)


def _meet_in_day(timeframe_1, timeframe_2):
    if not timeframe_1.day == timeframe_2.day:
        return False
    if timeframe_1.finish < timeframe_2.start:
        return False
    if timeframe_2.finish < timeframe_1.start:
        return False
    return True


def meet(timeframe_1, timeframe_2):
    timeframe_1 = Timeframe(*timeframe_1)
    timeframe_2 = Timeframe(*timeframe_2)

    if timeframe_1.day - timeframe_2.day == 1:
        if timeframe_1.start == 0 and timeframe_2.finish == 1440:
            return True
    if timeframe_2.day - timeframe_1.day == 1:
        if timeframe_2.start == 0 and timeframe_1.finish == 1440:
            return True
    return _meet_in_day(timeframe_1, timeframe_2)


def _add_timeframe(frames, timeframe):
    for i, frame in enumerate(frames):
        if _meet_in_day(frame, timeframe):
            frames[i] = Timeframe(
                frame.day,
                min(frame.start, timeframe.start),
                max(frame.finish, timeframe.finish),
            )
            return
    frames.append(timeframe)


def read_schedule(line):
    day_to_digit = {"MO": 0, "TU": 1, "WE": 2, "TH": 3, "FR": 4, "SA": 5, "SU": 6}
    name, sched = line.split("=")
    frames = []
    for frame in sched.split(","):
        day = day_to_digit[frame[:2]]
        start = int(frame[2:4]) * 60 + int(frame[5:7])
        finish = int(frame[8:10]) * 60 + int(frame[11:13])
        if start < 0 or start > 1440 or finish < 0 or finish > 1440 or start > finish:
            raise (WrongTimeException(line=line))
        _add_timeframe(frames, Timeframe(day, start, finish))
    return name, frames


def _add_schedule(schedule, name, timeframes):
    if name in schedule.keys():
        for frame in timeframes:
            _add_timeframe(schedule[name], frame)
    else:
        schedule[name] = timeframes


def read_schedules(input):
    """It takes iterable as an argument and returns dict where keys are names and
    values are lists of tuples with time frames of employees.
    First element of tuple represents day of week (0 == Monday, 6 == Sunday).
    Second element of tuple represents start of timeframe in minutes (10:00 == 600).
    Third element of tuple represents end of timeframe in minutes (12:00 == 720).
    Example:
    For input ("RENE=MO10:00-12:00,TH01:00-03:00",) it returns
    {
        'RENE': [
            (0, 600, 720),
            (3, 60, 180),
        ]
    }"""
    schedule = {}
    for line_n, line in enumerate(input):
        try:
            name, frames = read_schedule(line)
        except WrongTimeException:
            raise (WrongTimeException(line_n + 1, line))
        except Exception:
            raise (CorruptedDataException(line_n + 1, line))
        _add_schedule(schedule, name, frames)
    return schedule


def _count_coincidences(schedule, name_1, name_2):
    count = 0
    for timeframe_1 in schedule[name_1]:
        for timeframe_2 in schedule[name_2]:
            if meet(timeframe_1, timeframe_2):
                count += 1
    return count


def run(input):
    """Geneartor function. It takes iterable as an argument and yields tuples where
    first and second elements are names and third is number of coincendences.
    for input (
        "RENE=MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00",
        "ASTRID=MO10:00-12:00,TH12:00-14:00,SU20:00-21:00"
    )
    it yields ("RENE", "ASTRID", 2)"""
    schedule = read_schedules(input)
    names = [name for name in schedule.keys()]
    n = len(names)
    for i in range(n - 1):
        for j in range(i + 1, n):
            name_1 = names[i]
            name_2 = names[j]
            coincidences = _count_coincidences(schedule, name_1, name_2)
            yield (name_1, name_2, coincidences)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input", default="INPUT", help='input file name e.g. "INPUT"'
    )
    parser.add_argument(
        "-o", "--output", default="OUTPUT", help='output file name e.g. "OUTPUT"'
    )
    args = parser.parse_args()
    input_filename = args.input
    output_filename = args.output
    try:
        input = open(f"{input_filename}.txt", "r")
        print(f"Started. Input file: {input.name}")
    except:
        raise

    open(f"{output_filename}.txt", "w").close()
    with open(f"{output_filename}.txt", "a") as output:
        for line in run(input):
            output.write(f"{line[0]}-{line[1]}: {line[2]}\n")

    print(f"Finished. Output file: {output_filename}.txt")
