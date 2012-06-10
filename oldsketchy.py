#!/usr/bin/env python2.7

# Original sketchy demo by @andrew_clegg, May 2012, public domain.
#
# https://github.com/andrewclegg/sketchy

# See README for background. This will work fine on Python 2.5+, including
# Jython. Jython actually seems slightly faster, for larger datasets at
# least, but tends to use more memory.

import sys
import random
from collections import defaultdict
from itertools import izip, imap

# A few knobs you can tweak...

# Hash size in bits -- higher gives more accurate results, but is more expensive.
size = 32
assert(size <= 32) # Can't go higher than this unless you change or remove ham_dist

# Number of features (columns) in the demo data.
dim = 10

# Number of items (rows) in the demo data.
items = 1000000

# Some random demo data, just dim*items ints from 0-10.
test_data = [[random.randint(0, 10) for i in xrange(0, dim)] for j in xrange(0, items)]

# Size of the similar items neighbourhood for demo purposes (max number of bits different).
ham_neighbourhood = size / 8

# For testing only -- returns the product of the magnitude (length) of two vectors.
def magnitude_prod(vec1, vec2):
    tot1 = 0
    tot2 = 0
    for i in xrange(dim): # Beware global variable. These funcs get hit a lot.
        val1 = vec1[i]
        val2 = vec2[i]
        tot1 += val1**2
        tot2 += val2**2
    return (tot1 * tot2)**0.5

# For testing only -- returns the cosine similarity of two vectors.
def cos_sim(vec1, vec2):
    return dot_product(vec1, vec2) / magnitude_prod(vec1, vec2)

# For testing only -- returns the euclidean distance between two points.
def euc_dist(vec1, vec2):
    tot = 0
    for i in xrange(dim): # Beware global variable. These funcs get hit a lot.
        val = vec1[i] - vec2[i]
        tot += val**2
    return (tot)**0.5

# For testing only -- returns the hamming distance between two bitfields (as numbers).
# It's from here:
# http://stackoverflow.com/questions/109023/best-algorithm-to-count-the-number-of-set-bits-in-a-32-bit-integer#109025
# and I have no idea why it works.
def ham_dist(a, b):
    i = a ^ b
    i = i - ((i >> 1) & 0x55555555)
    i = (i & 0x33333333) + ((i >> 2) & 0x33333333)
    return (((i + (i >> 4) & 0xF0F0F0F) * 0x1010101) & 0xffffffff) >> 24

# In case you need it -- converts a list of 0s and 1s to a number. No sanity checking!
def to_int(bitlist):
    return sum([bit * 2**power for power, bit in enumerate(bitlist)])

################ HERE'S WHERE THE FUN STARTS ################

# Returns the dot product of two vectors.
def dot_product(vec1, vec2):
    tot = 0
    for i in xrange(len(vec1)):
        tot += vec1[i] * vec2[i]
    return tot

# Returns 'size' hyperplanes in a 'dim'-dimensional space.
def make_planes(size, dim):
    return [[random.choice((-1, 1)) for i in xrange(0, dim)]
        for j in xrange(0, size)]

# Calculates the hash for a vector of data, using one bit for each plane.
def lsh(vec, planes):
    dps = [dot_product(vec, plane) for plane in planes]
    return sum([2**i if dps[i] > 0 else 0 for i in xrange(0, len(dps))])

# Generate the required number of planes in a space of the right dimensionality.
planes = make_planes(size, dim)

# Calculate the hash for each row in the demo data.
sketch_table = [(lsh(row, planes), row) for row in test_data]
test_data = None

################# ALL THE REST IS TEST CODE #################

# Actually calculating the hashes (above) is fast compared to all the stuff
# below here for producing metrics. Chop it out and see it fly.

sketch_dict = defaultdict(list)
for (sketch, row) in sketch_table:
    sketch_dict[sketch].append(row)

in_bin_cos_tot = 0
in_bin_cos_cnt = 0
in_bin_euc_tot = 0
in_bin_euc_cnt = 0
singletons = 0

for sketch, rows in sketch_dict.items():
    bin_size = len(rows)
    if bin_size > 1:
        #print 'Bin %d has %d elements' % (sketch, bin_size)
        row0 = rows[0]
        cos = [cos_sim(row0, rows[i]) for i in xrange(1, bin_size)]
        euc = [euc_dist(row0, rows[i]) for i in xrange(1, bin_size)]
        #avg_sim = sum(sims) / len(sims)
        #print 'Average cosine similarity first -> rest = %f' % avg_sim
        in_bin_cos_tot += sum(cos)
        in_bin_cos_cnt += len(cos)
        in_bin_euc_tot += sum(euc)
        in_bin_euc_cnt += len(euc)
    else:
        singletons += 1

neighbourhood_cos_tot = 0
neighbourhood_cos_cnt = 0
neighbourhood_euc_tot = 0
neighbourhood_euc_cnt = 0
global_cos_tot = 0
global_cos_cnt = 0
global_euc_tot = 0
global_euc_cnt = 0

subset = random.sample(sketch_table, min(500, items / 1000))
for sketch1, vec1 in subset:
    for sketch2, vec2 in subset:
        if vec1 is not vec2:
            cos = cos_sim(vec1, vec2)
            global_cos_tot += cos
            global_cos_cnt += 1
            euc = euc_dist(vec1, vec2)
            global_euc_tot += euc
            global_euc_cnt += 1
            ham = ham_dist(sketch1, sketch2)
            if ham_dist(sketch1, sketch2) <= ham_neighbourhood:
                neighbourhood_cos_tot += cos
                neighbourhood_cos_cnt += 1
                neighbourhood_euc_tot += euc
                neighbourhood_euc_cnt += 1

bin_sizes = map(len, sketch_dict.values())
print '%d items in %d bins' % (items, len(sketch_dict.values()))
print 'Largest bin: %d items' % max(bin_sizes)
print 'Smallest bin: %d items' % min(bin_sizes)
print 'Singleton bins: %d' % singletons

if in_bin_cos_cnt > 0:
    print 'Average within-bin first->rest cosine similarity = %f' \
        % (in_bin_cos_tot / in_bin_cos_cnt)
if in_bin_euc_cnt > 0:
    print 'Average within-bin first->rest euclidean distance = %f' \
        % (in_bin_euc_tot / in_bin_euc_cnt)
if neighbourhood_cos_cnt > 0:
    print 'Average neighbourhood cosine similarity = %f (pairs = %d, max hamming = %d)' \
        % (neighbourhood_cos_tot / neighbourhood_cos_cnt, neighbourhood_cos_cnt, ham_neighbourhood)
if neighbourhood_euc_cnt > 0:
    print 'Average neighbourhood euclidean distance = %f (pairs = %d, max hamming = %d)' \
        % (neighbourhood_euc_tot / neighbourhood_euc_cnt, neighbourhood_euc_cnt, ham_neighbourhood)
if global_cos_cnt > 0:
    print 'Average global cosine similarity = %f (pairs = %d)' \
        % (global_cos_tot / global_cos_cnt, global_cos_cnt)
if global_euc_cnt > 0:
    print 'Average global euclidean distance = %f (pairs = %d)' \
        % (global_euc_tot / global_euc_cnt, global_euc_cnt)


