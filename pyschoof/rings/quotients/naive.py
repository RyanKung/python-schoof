# -*- coding: utf-8 -*-
# Copyright (c) 2010--2012  Peter Dinges <pdinges@acm.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


"""
A naive implementation of quotient rings (factor rings, residue class rings).

@package   rings.quotients.naive
@author    Peter Dinges <pdinges@acm.org>
"""

from rings import CommutativeRing

from support.types import template
from support.operators import operand_casting
from support.profiling import profiling_name, local_method_names
from support.rings import extended_euclidean_algorithm

# FIXME: Having ring and modulus as parameters is redundant. Obviously we have
#        ring == modulus.__class__


@operand_casting
@local_method_names
@profiling_name("{_ring}/{_modulus}")
class QuotientRing(CommutativeRing, metaclass=template("_ring", "_modulus")):
    """
    A ring of residue classes of ring elements modulo a fixed ring element; the
    residue classes (quotient ring elements) support infix notation for ring
    operations, as well as mixed argument types.

    This is a template class that must be instantiated with the source ring
    and modulus.  Use it, for example, as follows:
    @code
    # Instantiate the template; Z4 is a class (here: integer congruence classes)
    Z4 = QuotientRing( rings.integers.naive.Integers, 4 )
    x = Z4(1)      # Create a residue class: (1 mod 4)
    y = Z4(3)      # Another residue class: (2 mod 4)
    z = x+y        # z is (0 mod 4)
    z == Z4(2) * 2 # This true because 4 == 0 modulo 4
    type(z) is Z4  # This is also true
    @endcode

    Other examples of QuotientRing template instances are:
    @code
    Z17 = QuotientRing( rings.integers.naive.Integers, 17 )    # Z/17Z

    # The ring (Z/2Z[x]) / (x^3 + x + 1) is isomorphic to GF8,
    # the field with 8 elements
    GF2  = fields.finite.naive.FiniteField( 2 )
    GF2x = rings.polynomials.naive.Polynomials( GF2 )
    GF8 = QuotientRing( GF2x, GF2x(1, 1, 0, 1) ) 
    @endcode

    A quotient ring, factor ring, or residue class ring, is a ring
    @f$ R/(m) @f$, where @f$ R @f$ is the source ring, and @f$ (m) @f$
    denotes the ideal generated by the element @f$ m\in R @f$.  The ring
    operations carry over to quotient classes in a natural way: if
    @f$ x + y = z @f$ in @f$ R @f$, then @f$ [x] + [y] = [z] @f$
    in @f$ R/(m) @f$ (by the canonical homomorphism).

    With the quotient ring operations being defined in terms of source ring
    operations, elements of the source ring must implement:
    - __bool__(): Zero testing (@c True if not zero)
    - __eq__(): Equality testing with the @c == operator (@c True if equal)
    - __add__(): Addition with the @c + operator; @c self is the left summand
    - __neg__(): Negation with the @c - unary minus operator (the additive inverse)
    - __mul__(): Multiplication with the @c * operator; @c self is the
      left factor
    - __divmod__(): Division with remainder; @c self is the dividend (left element)

    @note  The implementation emphasizes simplicity over speed; it omits
           possible optimizations.

    @note  The class uses the operand_casting() decorator: @c other operands in
           binary operations will first be treated as QuotientRing elements.
           If that fails, the operation will be repeated after @p other was fed
           to the constructor __init__().  If that fails, too, then the
           operation returns @c NotImplemented (so that @p other.__rop__()
           might be invoked).

    @see   For example, Robinson, Derek J. S.,
           "An Introduction to Abstract Algebra", p. 106.
    """

    #- Instance Methods -----------------------------------------------------------

    def __init__(self, representative):
        """
        Construct a new residue class @p representative modulo modulus().

        If the @p representative already is an element of this QuotientRing
        class, then the new element is a copy of @p representative.
        """
        if isinstance(representative, self.__class__):
            self.__remainder = representative.__remainder
        elif isinstance(representative, self._modulus.__class__):
            self.__remainder = representative % self._modulus
        else:
            m = self._modulus
            self.__remainder = m.__class__(representative) % m

    def remainder(self):
        """
        Return the remainder of the residue class (QuotientRing element)
        @p self.  This is an element of the source ring(), not a residue class.
        """
        return self.__remainder

    def __bool__(self):
        """
        Test whether the residue class (QuotientRing element) is non-zero:
        return @c True if, and only if, the remainder modulo modulus() is
        non-zero. Return @c False if the remainder is zero.

        Implicit conversions to boolean (truth) values use this method, for
        example when @c x is an element of a QuotientRing:
        @code
        if x:
            do_something()
        @endcode
        """
        return bool(self.__remainder)

    def __eq__(self, other):
        """
        Test whether another residue class (QuotientRing element) @p other is
        equivalent to @p self; return @c True if that is the case.  The infix
        operator @c == calls this method.

        Two residue classes @f$ [x], [y] @f$ are equal if, and only if, the
        difference of two representatives is a multiple of the modulus():
        @f$ x-y = m\cdot z @f$. 
        """
        # The representative is always the remainder; an equality test suffices
        return self.__remainder == other.remainder()

    def __add__(self, other):
        """
        Return the sum of @p self and @p other. The infix operator @c + calls
        this method.

        The sum of two residue classes (QuotientRing elements) @f$ [x], [y] @f$
        is the residue class @f$ [x + y] @f$. 
        """
        return self.__class__(
            self.__remainder + other.remainder()
        )

    def __neg__(self):
        """
        Return the additive inverse of @p self, which is @f$ [-x] @f$
        for a residue class (QuotientRing element) @f$ [x] @f$. The negation
        operator @c -x (unary minus) calls this method.
        """
        return self.__class__(-self.__remainder)

    def __mul__(self, other):
        """
        Return the product of @p self and @p other. The infix operator @c *
        calls this method.

        The product of two residue classes (QuotientRing elements)
        @f$ [x], [y] @f$ is the residue class @f$ [x \cdot y] @f$. 
        """
        return self.__class__(
            self.__remainder * other.remainder()
        )

    def __truediv__(self, other):
        """
        Return the quotient of @p self and @p other: multiply @p self with
        @c other.multiplicative_inverse(), so that
        @code
        (self / other) * other == self
        @endcode
        The infix operator @c / calls this method.

        @exception ZeroDivisionError   if @p other is not a unit, that is, has
                                       no multiplicative inverse.
        """
        return self * other.multiplicative_inverse()

    def __rtruediv__(self, other):
        """
        Return the quotient of @p other and @p self: multiply @p other with
        @c self.multiplicative_inverse(), so that
        @code
        (other / self) * self == other
        @endcode
        The infix operator @c / calls this method if other.__truediv__()
        returned @c NotImplemented.

        @exception ZeroDivisionError   if @p other is not a unit, that is, has
                                       no multiplicative inverse.
        """
        return other * self.multiplicative_inverse()

    def multiplicative_inverse(self):
        """
        Return an residue class (QuotientRing element) @c n such that
        @c n * self is one().

        @exception ZeroDivisionError   if @p self is not a unit, that is, has
                                       no multiplicative inverse.
        """
        if not self.__remainder:
            raise ZeroDivisionError

        inverse, ignore, gcd = \
            extended_euclidean_algorithm(self.__remainder, self._modulus)

        if gcd == self._ring.one():
            return self.__class__(inverse)
        else:
            message = "element has no inverse: representative and modulus " \
                      "are not relatively prime"
            raise ZeroDivisionError(message)

    #- Class Methods-----------------------------------------------------------

    @classmethod
    def modulus(cls):
        """
        Return the quotient ring's modulus; this is an element of the
        source ring(), not a residue class (QuotientRing element).
        """
        return cls._modulus

    @classmethod
    def ring(cls):
        """
        Return the source ring.
        """
        return cls._ring

    @classmethod
    def zero(cls):
        """
        Return the quotient ring's neutral element of addition: the residue
        class (QuotientRing element) of ring().zero()
        """
        return cls(cls._ring.zero())

    @classmethod
    def one(cls):
        """
        Return the quotient ring's neutral element of multiplication: the
        residue class (QuotientRing element) of ring().one()
        """
        return cls(cls._ring.one())