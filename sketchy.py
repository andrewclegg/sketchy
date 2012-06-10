import random
from array import array

# Possible improvements:
#
# - Bit-field instead of array to hold the hyperplanes

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


