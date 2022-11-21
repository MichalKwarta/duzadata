#!/usr/bin/env python3

from enum import Enum
from sys import stdin
import typing as t
from functools import partial, reduce


class Columns(Enum):
    DATE = 0
    ZIP_CODE = 2
    ON_STREET_NAME = 6
    CROSS_STREET_NAME = 7
    OFF_STREET_NAME = 8
    PEDESTRIANS_INJURED = 11
    PEDESTRIANS_KILLED = 12
    CYCLIST_INJURED = 13
    CYCLIST_KILLED = 14
    MOTORIST_INJURED = 15
    MOTORIST_KILLED = 16


STREET_COLUMNS = (Columns.ON_STREET_NAME.value,
                  Columns.CROSS_STREET_NAME.value, Columns.OFF_STREET_NAME.value)


def clear_line(line: str) -> t.List[str]:
    return line.strip().split(',')


def validate(line: t.List[str],
             predicates: t.List[t.Callable[[t.List[str]], bool]] = []) -> t.List[str]:
    return line if all([predicate(line) for predicate in predicates]) else []


def past_2012(line: t.List[str]) -> bool:
    date = line[Columns.DATE.value].split('/')[-1]
    return int(date) > 2012 if date.isdecimal() else False


def zip_code_non_empty(line: t.List[str]) -> bool:
    return line[Columns.ZIP_CODE.value] != ''


is_interesting = partial(validate, predicates=[
    past_2012, zip_code_non_empty
])


def create_mapping(line: t.List[str]):
    if line == []:
        return
    zip_code = line[Columns.ZIP_CODE.value]
    streets = [line[i] for i in STREET_COLUMNS if line[i] != '']
    data_range = range(Columns.PEDESTRIANS_INJURED.value, Columns.MOTORIST_KILLED.value + 1)
    cols_with_data = [i for i in data_range if line[i] != '0']
    for column in cols_with_data:
        for street in streets:
            print(f"{' '.join(street.upper().split())}_{zip_code}_{Columns(column).name}\t{line[column]}")




compose = lambda *F: reduce(lambda f, g: lambda x: f(g(x)), F)

processing = compose(create_mapping,is_interesting,clear_line)


for line in stdin:
    try:
        processing(line)
    except:
        pass

