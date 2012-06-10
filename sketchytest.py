import unittest
import random
from array import array
import sketchy


def random_sparse_ints(dim, lbound, ubound):
    set_count = random.randint(0, dim - 1)
    set_idxs = random.sample(xrange(dim), set_count)
    sv = []
    for i in set_idxs:
        sv.append(i, random.randint(lbound, ubound))
    return sv


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

    def test_mixed_dot_product(self):
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

    def test_sparse_random_projection_binary_vector(self):
        size = 32
        dim = 100
        seed = 42
        instances = 100
        vectors = []
        ham_dists = []
        cos_sims = []
        for i in xrange():
            sv = random_sparse_vector(dim, 0, 1)
            hashcode = sketchy.sparse_random_projection(sv, size, dim, seed)



if __name__ == '__main__':
    unittest.main()

