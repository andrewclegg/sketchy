import unittest
from array import array
import __builtin__

# Kludge around the function decorators that Pig injects.
# I feel strangely dirty.
__builtin__.outputSchema = lambda(x) : lambda(y) : y

import sketchy

class TestSketchy(unittest.TestCase):
    
    def test_make_planes(self):
        size = 32
        dim = 10
        seed = 23
        planes = sketchy.make_planes(size, dim, seed)

        # For checking that results are consistent
        planes2 = sketchy.make_planes(size, dim, seed)

        self.assertEqual(size, len(planes))
        for i in xrange(len(planes)):
            plane = planes[i]
            self.assertEqual(dim, len(plane))
            for j in xrange(len(plane)):
                val = plane[j]
                self.assert_(val in [1, -1])
                self.assertEqual(val, planes2[i][j])

    def test_sparse_dot_product(self):
        dim = 10
        sv = [(1, 0.4), (3, -0.1), (6, 0.8), (9, 0)]

        dv = array('b', [1, 1, 1, 1, 1, -1, -1, -1, -1, -1])
        dp1 = sketchy.sparse_dot_product(sv, dv)
        # 0.4 * 1 + -0.1 * 1 + 0.8 * -1 + 0 * -1
        self.assertEqual(-0.5, dp1)

        array.reverse(dv)
        dp2 = sketchy.sparse_dot_product(sv, dv)
        # 0.4 * -1 + -0.1 * -1 + 0.8 * 1 + 0 * 1
        self.assertEqual(0.5, dp2)

    def test_sparse_random_projection(self):
        sv = [(1, 0.4), (3, -0.1), (6, 0.8), (9, 0)]
        size = 32
        dim = 10
        seed = 23
        hashcode = sketchy.sparse_random_projection(sv, size, dim, seed)

if __name__ == '__main__':
    unittest.main()

