import unittest
from saso.sliceType import SliceType
from saso.valueType import ValueType


class MathTests(unittest.TestCase):
    def test_add(self):
        v1 = ValueType(value=5, count=3)
        v2 = ValueType(value=5, count=4)
        sum_ = v1 + v2
        self.assertEqual(sum_.count, v1.count + v2.count)

    def test_true_divide(self):
        v1 = ValueType(value=5, count=6)
        v2 = ValueType(value=5, count=3)
        div_ = v1 / v2
        self.assertEqual(div_.count, v1.count / v2.count)

    def test_lt_value(self):
        v1 = ValueType(value=5, count=6)
        v2 = ValueType(value=6, count=3)
        self.assertLess(v1, v2)

    def test_gt_value(self):
        v1 = ValueType(value=5, count=6)
        v2 = ValueType(value=6, count=3)
        self.assertGreater(v2, v1)

    def test_equal_slices(self):
        s1 = SliceType([ValueType(3, 4), ValueType(3, 2), ValueType(1, 2), ValueType(0, 4)])
        s2 = SliceType([ValueType(3, 4), ValueType(3, 2), ValueType(1, 2), ValueType(0, 4)])
        self.assertEqual(s1, s2)

    def test_slice_add(self):
        s1 = SliceType([ValueType(1, 2), ValueType(3, 4)])
        s2 = SliceType([ValueType(3, 4), ValueType(3, 2), ValueType(1, 2), ValueType(0, 4)])
        self.assertEqual(s1 + s2, SliceType(array=[ValueType(0, 4), ValueType(1, 4), ValueType(3, 10)]))

    def test_slice_sum(self):
        s1 = SliceType([ValueType(1, 2), ValueType(3, 4)])
        self.assertEqual(sum([x.count for x in s1]), 6)


if __name__ == '__main__':
    unittest.main()
