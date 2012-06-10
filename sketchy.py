# Tools for locality-sensitive hashing.
#
# https://github.com/andrewclegg/sketchy
#
# Tested on Jython 2.5.2, should work on cpython 2.5+ except for the
# Hamming distance methods which need bit() from 2.6. Feel free to
# add your own retro versions. Haven't tested it on Python 3 yet.

import random
import sys
from array import array # Consider some sort of bitfield instead?

# Kludge around the function decorator that Pig injects, with a dummy.
if 'outputSchema' not in globals():
    def outputSchema(x):
        return lambda(y): y

planes = None

""" Create 'size' planes in a 'dim'-dimensional space, with a new random
    number generator using 'seed'."""
def make_planes(size, dim, seed):
    random.seed(seed)
    p = []
    for i in xrange(size):
        p.append(array('b', (random.choice((-1, 1)) for i in xrange(0, dim))))
    return p

""" Calculate dot product of a sparse vector 'sv' against a dense vector 'dv'.
    The sparse vector format is described below. No bounds checking is done,
    so make sure it doesn't exceed the size of 'dv'."""
def sparse_dot_product(sv, dv):
    tot = 0
    for (idx, val) in sv:
        tot += val * dv[idx]
    return tot

""" Calculates the Random Projection hash for a sparse vector 'sv' against a
    set of random planes defined by the other variables, using one bit for each
    plane. The vector should pe provided as a bag of (dimension, value) tuples.
    Only numeric values are supported, so you need to map words, categories etc.
    yourself first."""
@outputSchema('lsh:long') # TODO make this dynamic based on size
def sparse_random_projection(sv, size, dim, seed):
    # Create the planes if they don't already exist in this process
    global planes
    if planes is None:
        planes = make_planes(size, dim, seed)
    dps = [sparse_dot_product(sv, plane) for plane in planes]
    return sum([2**i if dps[i] > 0 else 0 for i in xrange(0, len(dps))])




if 'Java' in sys.version:
    import java.lang.Integer as Integer
    import java.lang.Long as Long
    def hamming32(i1, i2):
        return Integer.bitCount(i1^i2)
    def hamming64(l1, l2):
        return Long.bitCount(l1^l2)
else:
    def hamming32(i1, i2):
        return bin(i1^i2).count('1')
    hamming64 = hamming32

