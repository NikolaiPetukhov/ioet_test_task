import unittest

from collections import namedtuple

from main import run, meet, read_schedules
from main import CorruptedDataException


Timeframe = namedtuple("Timeframe", ["day", "start", "finish"])


class TestReadSchedules(unittest.TestCase):
    def test_read_schedules_1(self):
        """Test read_schedules() on correct input"""
        input = (
            "RENE=MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00",
            "ASTRID=MO10:00-12:00,TH12:00-14:00,SU20:00-21:00",
            "ANDRES=MO10:00-12:00,TH12:00-14:00,SU20:00-21:00",
        )
        output = {
            "RENE": [
                (0, 600, 720),
                (1, 600, 720),
                (3, 60, 180),
                (5, 840, 1080),
                (6, 1200, 1260),
            ],
            "ASTRID": [(0, 600, 720), (3, 720, 840), (6, 1200, 1260)],
            "ANDRES": [(0, 600, 720), (3, 720, 840), (6, 1200, 1260)],
        }
        result = read_schedules(input)
        self.assertEqual(set(result), set(output))

    def test_read_schedules_2(self):
        """Test read_schedules() on correct input with intersecting timeframes"""
        input = (
            "RENE=MO10:00-12:22,MO12:00-13:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00",
            "ASTRID=MO10:00-12:00,TH12:00-14:00TH14:00-15:30,SU20:00-21:00,TH12:30-15:00",
            "ANDRES=MO10:00-12:00,TH12:00-14:00,SU20:00-21:00",
        )
        output = {
            "RENE": [
                (0, 600, 720),
                (1, 600, 720),
                (3, 60, 180),
                (5, 840, 1080),
                (6, 1200, 1260),
            ],
            "ASTRID": [(0, 600, 780), (3, 720, 930), (6, 1200, 1260)],
            "ANDRES": [(0, 600, 720), (3, 720, 840), (6, 1200, 1260)],
        }
        result = read_schedules(input)
        self.assertEqual(set(result), set(output))

    def test_read_schedules_3(self):
        """Test read_schedules() on correct input with repeated names and intersecting timeframes"""
        input = (
            "RENE=MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00",
            "ASTRID=MO10:00-12:00,TH12:00-14:00,SU20:00-21:00",
            "ANDRES=MO10:00-12:00,TH12:00-14:00,SU20:00-21:00",
            "RENE=MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00,SU20:30-20:35",
            "ANDRES=MO10:00-12:00,TH14:00-15:00,SU20:00-21:00",
        )
        output = {
            "RENE": [
                (0, 600, 720),
                (1, 600, 720),
                (3, 60, 180),
                (5, 840, 1080),
                (6, 1200, 1260),
            ],
            "ASTRID": [(0, 600, 720), (3, 720, 840), (6, 1200, 1260)],
            "ANDRES": [(0, 600, 720), (3, 720, 900), (6, 1200, 1260)],
        }
        result = read_schedules(input)
        self.assertEqual(set(result), set(output))


class TestMeet(unittest.TestCase):
    def test_meet_1(self):
        """test meet() on Timeframe input"""
        inputs = (
            (Timeframe(0, 0, 1440), Timeframe(0, 1, 2)),
            (Timeframe(0, 1, 2), Timeframe(0, 0, 1440)),
            (Timeframe(1, 500, 900), Timeframe(0, 230, 550)),
            (Timeframe(0, 100, 500), Timeframe(1, 250, 750)),
            (Timeframe(0, 120, 240), Timeframe(0, 240, 360)),
            (Timeframe(4, 120, 240), Timeframe(4, 241, 360)),
            (Timeframe(5, 543, 782), Timeframe(5, 666, 1440)),
            (Timeframe(6, 666, 888), Timeframe(6, 555, 777)),
            (Timeframe(2, 666, 1440), Timeframe(3, 0, 777)),
            (Timeframe(1, 666, 1440), Timeframe(3, 0, 777)),
        )
        output = (True, True, False, False, True, False, True, True, True, False)
        for i, input in enumerate(inputs):
            self.assertEqual(meet(*input), output[i])

    def test_meet_2(self):
        """test meet() on tuple input"""
        inputs = (
            ((0, 0, 1440), (0, 1, 2)),
            ((0, 1, 2), (0, 0, 1440)),
            ((1, 500, 900), (0, 230, 550)),
            ((0, 100, 500), (1, 250, 750)),
            ((0, 120, 240), (0, 240, 360)),
            ((4, 120, 240), (4, 241, 360)),
            ((5, 543, 782), (5, 666, 1440)),
            ((6, 666, 888), (6, 555, 777)),
            ((2, 666, 1440), (3, 0, 777)),
            ((1, 666, 1440), (3, 0, 777)),
        )
        output = (True, True, False, False, True, False, True, True, True, False)
        for i, input in enumerate(inputs):
            self.assertEqual(meet(*input), output[i])


class TestRun(unittest.TestCase):
    def test_run_1(self):
        """
        Test run() on correct data
        """
        input = (
            "RENE=MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00",
            "ASTRID=MO10:00-12:00,TH12:00-14:00,SU20:00-21:00",
            "ANDRES=MO10:00-12:00,TH12:00-14:00,SU20:00-21:00",
        )
        output = {("RENE", "ASTRID", 2), ("RENE", "ANDRES", 2), ("ANDRES", "ASTRID", 3)}
        results = {i for i in run(input)}
        for i in results:
            self.assertTrue(i in output or (i[1], i[0], i[2]) in output)
        for i in output:
            self.assertTrue(i in results or (i[1], i[0], i[2]) in results)

    def test_run_2(self):
        """
        Test run() on correct data
        """
        input = (
            "RENE=MO10:15-12:00,TU10:00-12:00,TH13:00-13:15,SA14:00-18:00,SU20:00-21:00",
            "ASTRID=MO10:00-12:00,TH12:00-14:00,SU20:00-21:00",
        )
        output = {("RENE", "ASTRID", 3)}
        results = {i for i in run(input)}
        for i in results:
            self.assertTrue(i in output or (i[1], i[0], i[2]) in output)
        for i in output:
            self.assertTrue(i in results or (i[1], i[0], i[2]) in results)

    def test_run_3(self):
        """
        Test run() on correct data with one line
        """
        input = (
            "RENE=MO10:15-12:00,TU10:00-12:00,TH13:15-14:00,SA14:00-18:00,SU20:00-21:00",
        )
        output = set()
        results = {i for i in run(input)}
        for i in results:
            self.assertTrue(i in output or (i[1], i[0], i[2]) in output)
        for i in output:
            self.assertTrue(i in results or (i[1], i[0], i[2]) in results)

    def test_run_4(self):
        """
        Test run() on correct data without coincidences
        """
        input = (
            "RENE=MO10:15-12:00,TU10:00-12:00,TH13:15-14:00,SA14:00-18:00,SU20:00-21:00",
            "ASTRID=MO12:15-13:00,TH12:00-13:00,SU21:01-22:21",
            "ANDRES=TU08:00-09:00,TH08:00-09:00,FR20:00-21:00",
        )
        output = {("RENE", "ASTRID", 0), ("RENE", "ANDRES", 0), ("ASTRID", "ANDRES", 0)}
        results = {i for i in run(input)}
        for i in results:
            self.assertTrue(i in output or (i[1], i[0], i[2]) in output)
        for i in output:
            self.assertTrue(i in results or (i[1], i[0], i[2]) in results)

    def test_run_5(self):
        """
        Test run() on correct data
        """
        input = (
            "RENE=MO10:00-12:00,TU10:00-12:00,TH00:00-03:00,SA14:00-18:00,SU20:00-21:00",
            "ASTRID=MO10:00-12:00,TH12:00-14:00,SU20:00-21:00",
            "ANDRES=MO10:00-12:00,TH12:00-14:00,SU20:00-21:00",
            "DIEGO=MO08:00-09:00,WE10:00-24:00,FR01:00-03:00,SA14:00-18:00,SU20:00-21:00",
        )
        output = {
            ("RENE", "ASTRID", 2),
            ("RENE", "ANDRES", 2),
            ("ANDRES", "ASTRID", 3),
            ("DIEGO", "ASTRID", 1),
            ("DIEGO", "RENE", 3),
            ("DIEGO", "ANDRES", 1),
        }
        results = {i for i in run(input)}
        for i in results:
            self.assertTrue(i in output or (i[1], i[0], i[2]) in output)
        for i in output:
            self.assertTrue(i in results or (i[1], i[0], i[2]) in results)

    def test_run_empty_input(self):
        """Test run() on empty input"""
        input = ()
        results = {i for i in run(input)}
        self.assertTrue(results == set())

    def test_run_broken_input(self):
        """Test run() on broken input data"""
        input = (
            "RENE=MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00",
            "abracadabra",
            "ANDRES=MO10:00-12:00,TH12:00-14:00,SU20:00-21:00",
        )
        with self.assertRaises(CorruptedDataException):
            for _ in run(input):
                continue

    def test_run_wrong_input_type(self):
        """Test run() on wrong input type"""
        input = (123456789, True, 3.141592)
        with self.assertRaises(TypeError):
            for i in input:
                next(run(i))


if __name__ == "__main__":
    unittest.main()
