Python3 Implementation of Schoof's Algorithm
============================================

This is an implementation of Schoof's algorithm for counting the
points on elliptic curves over finite fields (Schoof, René. Elliptic
curves over finite fields and the computation of square roots mod
p. *Mathematics of Computation*, 44(170):483–494, 1985).

Elliptic curve cryptographic algorithms base their security guarantees
on the number of points on the used elliptic curve.  Because naive
point counting is infeasible, having a fast counting algorithm is
important to swiftly decide whether a curve is safe to use in
cryptography or not.  René Schoof's algorithm for counting the points
on an elliptic curve over a finite field is the foundation for the
(asymptotically) fastest [Schoof–Elkies–Atkin][sea-algorithm] counting
algorithm.


**Implementation.**
The implementation is written in [Python 3][python] and is kept as
simple as possible.  Its goal is to give insight into the mathematics
of the algorithm without the use of (too) high-level concepts.  For a
(pretty) gentle introduction into why and how Schoof's algorithm
works, please read my diploma thesis titled
[*An Elementary Derivation and Implementation of Schoof's Algorithm for Counting Points on Elliptic Curves*][thesis].
In the thesis, I try to explain *how one might get the idea for the
algorithm*.  This understanding of *why* things look the way they do
is often neglected in mathematics.

Schoof's algorithm uses arithmetic on elliptic curves, finite fields,
rings of polynomials, and quotient rings.  This repository therefore
contains Python modules for all these concepts that can be used on
their own.


Installation
-------------


```
pip install pyschoof

```


Program Execution
-----------------

The implementations work without any installation; they may be
executed directly from the checked out repository.  However, they
expect a set up Python 3.1 run-time environment as explained above.

The root directory contains the point counting programs: the file
`naive_schoof.py` is the implementation discussed in
\autoref{sec:implementation}; the file `reduced_computation_schoof.py`
is the version with better constants using a smarter computation order
and Hasse's theorem.  Curves for counting are specified as
space-separated triples *p*, *A*, and *B*: *p* is the prime size of
the galois field *GF[p]*, and *A* and *B* are the curve parameters.

### Example

Suppose you want to count the number of points on the elliptic curve
over *GF[23]* with parameters *A=4* and *B=2*.  If the current
directory in the terminal is the repository root, then
executing `pyschoof 23 4 2` yields the output

~~~~~
Counting points on y^2 = x^3 + 4x + 2 over GF<23>: 21
~~~~~


### Command Line Parameters

The program supports the command line options described below, which
for instance allow to read the curves from a file, or to create
execution profiles for performance analysis.

* `--version`: Show program's version number and exit.
* `-h`, `--help`: Show a help message and exit.
* `-i` *f*, `--input-file=`*f*: Read the curve parameters from file
  *f*.  Lines in *f* must contain either a comment, or a
  space-separated triple of curve parameters *p*, *A*, and *B*.
  Comment lines start with a hash (`#`); these and empty lines are
  skipped.
* `-o` *f*, `--output-file=`*f*: Write the results to file *f* instead
  of showing them on the terminal.  Each line of input generates one
  corresponding line of output.
* `-t` *s*, `--timelimit=`*s*: Terminate the program if processing an
  input triple takes longer than *s* seconds.  The program ends if the
  time limit expires; no subsequent lines will be read from an input
  file.  Thus, sort the parameters in input files ascending in length
  of the prime *p* to avoid triggering the time limit too early.
* `-p`, `--create-profile`: Create an execution profile for each
  processed input triple.  The profile consists of a call profile
  generated with the `cProfile` Python module, and a file with data
  about elapsed time and used memory.
* `-d` *d*, `--profile-directory=`*d*: If profiling is enabled with
  the `-p` flag, then the collected data is written to the directory
  *d*.  The default value is the current directory.


Profiling Tools
---------------

The `tools/` directory contains several programs to post-process
profiles resulting from a set `-p` flag.  For example, it includes a
call profile converter that outputs [Callgrind][callgrind] files.  Use
[KCacheGrind][kcachegrind] to interactively inspect Callgrind files.


Further Documentation
---------------------

The implementation comes with extensive [API documentation][api] that
explains the purpose and usage of all classes.

Furthermore, the directory `_test` contains unit tests to verify
correct arithmetic.  The unit tests are designed to be easily extended
to further implementations of the same objects.  Thus, mistakes in new
designs should be simpler to locate.  To run the unit tests, execute
`python3 -m _test` in the repository root directory.


License
-------
Copyright (c) 2017 Ryan Kung <ryankung@ieee.org>

Copyright (c) 2010--2012 Peter Dinges <pdinges@acm.org>.

The software in this repository is free software: you can redistribute
it and/or modify it under the terms of the GNU General Public License
as published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

The software is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the [GNU General Public License][gpl3]
along with this program.  If not, see <http://www.gnu.org/licenses/>.


[api]: http://pdinges.github.com/python-schoof
[callgrind]: http://valgrind.org/info/tools.html "Callgrind is part of the Valgrind tool suite"
[gpl3]: http://opensource.org/licenses/GPL-3.0 "GNU General Public License, version 3"
[kcachegrind]: http://kcachegrind.sourceforge.net/html/Home.html "Interactive viewer for Callgrind files."
[python]: http://python.org "Python Programming Language"
[python-using]: http://docs.python.org/py3k/using/index.html "Python Setup and Usage"
[sea-algorithm]: http://en.wikipedia.org/wiki/Schoof%E2%80%93Elkies%E2%80%93Atkin_algorithm "Schoof-Elkies-Atkin algorithm for counting points on elliptic curves over finite fields."
[thesis]: http://www.elwedgo.de/fileadmin/elwedgo.de/portfolio/diploma_thesis_math/dinges-elementary_schoof_derivation-thesis.pdf
