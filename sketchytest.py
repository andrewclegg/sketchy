import unittest
import random
from array import array
import sketchy


def random_sparse_vector(dim, lbound, ubound):
    set_count = random.randint(0, dim - 1)
    set_idxs = random.sample(xrange(dim), set_count)
    sv = []
    for i in set_idxs:
        sv.append((i, random.randint(lbound, ubound)))
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
        dp1 = sketchy.mixed_dot_product(sv, dv)
        # 0.4 * 1 + -0.1 * 1 + 0.8 * -1 + 0 * -1
        self.assertEqual(-0.5, dp1)

        array.reverse(dv)
        dp2 = sketchy.mixed_dot_product(sv, dv)
        # 0.4 * -1 + -0.1 * -1 + 0.8 * 1 + 0 * 1
        self.assertEqual(0.5, dp2)

    def test_sparse_random_projection_binary_vector(self):
        size = 31
        dim = 100
        seed = 42
        instances = 1000
        vectors = []
        hashes = []
        ham1_cos_sims = []
        ham2_cos_sims = []
        for i in xrange(instances):
            sv = random_sparse_vector(dim, 0, 1)
            h = sketchy.sparse_random_projection(sv, size, dim, seed)
            vectors.append(sv)
            hashes.append(h)
        for i in xrange(instances):
            for j in xrange(i + 1, instances):
                ham_dist = sketchy.hamming32(hashes[i], hashes[j])
                if ham_dist == 1:
                    ham1_cos_sims.append(sketchy.sparse_cos_sim(vectors[i], vectors[j]))
                elif ham_dist == 2:
                    ham2_cos_sims.append(sketchy.sparse_cos_sim(vectors[i], vectors[j]))
        ham1_mean = sum(ham1_cos_sims) / len(ham1_cos_sims)
        ham2_mean = sum(ham2_cos_sims) / len(ham2_cos_sims)
        self.assert_(ham1_mean > ham2_mean)

 
# TODO: no unsigned ints in Java makes conversion slightly annoying, hmmm.


if __name__ == '__main__':
    unittest.main()

