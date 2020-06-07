#!/usr/bin/env python3

from sqlite3 import dbapi2 as sqlite
import datetime
import unittest
import collections

DB = "cached.db"
SQL = """SELECT day, cases FROM cases_log ORDER BY day;"""


# tuple generator augmenter
#
# take:
#   a generator, which yields tuples
#   a callback for getting the date from these tuples
#   a callback for getting the value to be appended to the tuple
#
# make a new generator which sorts all this out

class Augmenter:
    def __init__(self, source_generator):
        self.source = source_generator
        self.prev = None
        self.current = None

    def __iter__(self):
        return self

    def __next__(self):
        c = next(self.source)
        self.current = c
        current_date = self.date()
        aug = self.augmentation()
        i = tuple(list(c) + [aug])
        self.prev = c
        return i

    # override this
    def date(self):
        return self.current[0]

    # override this
    def augmentation(self):
        return None


class DateAugmenter(Augmenter):
    def date(self):
        idx = 0
        if self.prev is None:
            return None
        prev = self.prev[idx]
        cur  = self.current[idx]

        diff = (cur - prev).days
        assert diff == 1
        return cur


class CasesAugmenter(DateAugmenter):
    def augmentation(self):
        idx = -1
        if self.prev is None:
            return None
        prev_cases = self.prev[idx]
        cur_cases  = self.current[idx]
        return cur_cases - prev_cases


class RxAugmenter(DateAugmenter):
    def augmentation(self):
        idx = -1
        if self.prev is None:
            return None
        prev_rate = self.prev[idx]
        cur_rate  = self.current[idx]
        if prev_rate is None:
            return None
        return cur_rate * 1.0 / prev_rate


class AvgAugmenter(DateAugmenter):
    def __init__(self, aug, size):
        self.lru = collections.deque(maxlen=size)
        super().__init__(aug)

    def __next__(self):
        c = next(self.source)
        self.current = c

        self.prev = c
        if c[-1] is not None:
            self.lru.append(c[-1])

        aug = self.augmentation()
        i = tuple(list(c) + [aug])

        return i

    def augmentation(self):
        if len(self.lru) <= 0:
            return None
        return sum(self.lru) / len(self.lru)

class TestAugmenter(unittest.TestCase):
    def test_basic(self):
        gen = ( (datetime.datetime(2020, 1, i), i) for i in range(1, 10) )
        a = DateAugmenter(gen)
        total = 0
        for d, i, aug in a:
            total += i
        self.assertEqual(45, total)


def get_raw_cases():
    db = sqlite.connect(DB)
    c = db.cursor()
    results = c.execute(SQL)
    for day, cases in results.fetchall():
        d = datetime.datetime.strptime(day, '%Y-%m-%d')
        yield d, cases

def run():
    # calculate_rx()
    cases = CasesAugmenter(get_raw_cases())
    rx = RxAugmenter(cases)
    avg = AvgAugmenter(rx, 7)
    for datetime, cases, daily_increase, growth, avg_growth in avg:
        print(datetime, cases, daily_increase, growth, avg_growth)


if __name__ == '__main__':
   run()
