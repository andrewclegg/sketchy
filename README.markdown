sketchy
=======

A simple implementation of locality-sensitive hashing in Python, with support
for Pig.

Say again?
----------

You know how normal hashes are designed to _avoid_ collisions?
Locality-sensitive hashes are designed to _cause_ collisions. In fact, the more
similar the input data is, the more similar the resulting hashes will be, with
a small and predictable error rate.

This makes them a very useful tool for large scale data mining, as a component
in:

* fuzzy-matching database records or similar documents
* nearest-neighbours clustering and classification
* duplicate detection
* content recommendation

et cetera.

You can choose the hash size in bits, and this lets you trade off space and
time costs against accuracy and granularity.

My implementation isn't heavily optimized, apart from a few places that stood
out in a profiler, but is designed to run easily on Hadoop, e.g. via Pig.
However it scales roughly linearly with the amount of data so can happily
handle millions of records on a single machine. It targets Python 2.5 for
Jython compatibility, and uses no extra libraries.

How does it work?
-----------------

This particular variant of LSH uses _sketches_, aka random projection, which
are rough lower-dimensional representations of a point in higher-dimensional
space.

It works by slicing up the space with a number of surfaces (hyperplanes), and
seeing which side of each hyperplane the data point is on. This can be
represented with just one bit per hyperplane. The reasoning is, genuinely
similar items will be on the same side of most hyperplanes. The resulting
hashes make up a Hamming code, i.e. the more bits two hashes have in common,
the more similar their input data was.

The input for each item is a vector of numbers, which are understood as
co-ordinates in the high-dimensional space. If you have data of another kind,
like text or categories, you must map them into numeric form first, e.g. with a
database, dictionary lookup or kernel function.

**Important:** Don't leave things like numeric IDs in your data, as user 3318
isn't "similar to" user 3319, but the algorithm doesn't know that. The usual
approach is to give each user a whole row or column, with a 0/1 flag or a count
in each cell, e.g. in a users-vs-movies matrix for recommenders.

The original method is described here:

http://www.cs.princeton.edu/courses/archive/spr04/cos598B/bib/CharikarEstim.pdf

These pages were also useful when I was implementing it:

http://metaoptimize.com/qa/questions/8930/basic-questions-about-locally-sensitive-hashinglsh

http://www.coolsnap.net/kevin/?p=23

http://en.wikipedia.org/wiki/Locality-sensitive_hashing#Random_projection

There are other LSH methods out there and I hope to add some of them later.

How do I use it?
----------------

See oldsketchy.py for a demo. In fact, most of the file is demo. The
nuts-and-bolts are only a few lines of code. Just copy and paste the bits you
need. There are comments explaining what's going on all the way through.

The newer version of sketchy.py is a properly-tested module that also functions
as a UDF under Pig. It's a work in progress and hasn't been properly tested
yet.

The use case I had in mind when I wrote it was for neighbour-finding /
similarity-search on Hadoop. You could read in a dataset from HDFS, feed it
through sketchy on the mappers to get a hash for each record, and then join on
matching hashes to get candidate matches. This gets round the classic data
locality problem that stops some all-against-all search methods from
parallelizing well.

This would probably work best with a small-ish hash size, so your hash space
isn't too sparse.

I haven't tried this yet though. If you find this useful, I'd love to hear about
it.

**Important:** If you do run it on a cluster, make sure to use the same random
number seed everywhere. Otherwise, each process will generate a different set
of hyperplanes, and the results will be garbage.

Contact
-------

https://twitter.com/#!/andrew_clegg

https://github.com/andrewclegg/sketchy

License
-------

oldsketchy.py is in the public domain, everything else is (c) Andrew Clegg 2012
and distributed under the Apache 2.0 License.

http://www.apache.org/licenses/LICENSE-2.0.html

