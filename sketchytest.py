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
        instances = 100
        vectors = []
        hashes = []
        ham_dists = []
        cos_sims = []
        spearman = Spearman()
        for i in xrange(instances):
            sv = random_sparse_vector(dim, 0, 1)
            h = sketchy.sparse_random_projection(sv, size, dim, seed)
            vectors.append(sv)
            hashes.append(h)
        for i in xrange(instances):
            for j in xrange(i + 1, instances):
                ham_dists.append(sketchy.hamming32(hashes[i], hashes[j]))
                cos_sims.append(sketchy.sparse_cos_sim(vectors[i], vectors[j]))
        print spearman.Calculate(cos_sims, ham_dists) # This doesn't look so good, why?

 
# TODO: no unsigned ints in Java makes conversion slightly annoying, hmmm.

# Found at:
# http://www.morezilla.net/?q=blog&s=23
class Spearman:
	def __init__(self):
		pass
		
	def __Sort1( self, a, b ):
		if a[0] < b[0]: return -1
		if a[0] > b[0]: return 1
		return 0
	
	def __Sort2( self, a, b ):
		if a[1] < b[1]: return -1
		if a[1] > b[1]: return 1
		return 0	

	def Calculate( self, dataX, dataY ):
		table = []
		n = len(dataX)
		i = 0		
		while( i < n ):
			table.append([int(dataX[i]), int(dataY[i]), 0, 0])
			i+=1		
		
		table2 = []
		table.sort(self.__Sort1)
		i = 1
		for item in table:
			table2.append([item[0], item[1], i, 0])
			i+=1
			
			
		table3 = []
		table2.sort(self.__Sort2)
		i = 1
		for item in table2:
			table3.append([item[0], item[1], item[2], i])
			i+=1
		
		di = []
		for item in table3:
			di.append(item[2] - item[3])
		
		di2 = []
		sum = 0
		for item in di:
			sum += item**2
			di2.append(item**2)
		
		#we have everything to calculate spearman coff
		s = 1 - float(sum*6)/float(n*(n*n -1))
		return s





if __name__ == '__main__':
    unittest.main()

