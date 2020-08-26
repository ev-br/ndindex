from numpy import intp

from .array import ArrayIndex
from .ndindex import asshape

class IntegerArray(ArrayIndex):
    """
    Represents an integer array index.

    If `idx` is an n-dimensional integer array with shape `s = (s1, ..., sn)`
    and `a` is any array, `a[idx]` replaces the first dimension of `a` with
    dimensions of size `s1, ..., sn`, where each entry is indexed according to
    the entry in `idx` as an integer index.

    Integer arrays can also appear as part of tuple indices. In that case,
    they replace the axis being indexed. If more than one integer array
    appears inside of a tuple index, they are broadcast together and iterated
    as one. Furthermore, if an integer array appears in a tuple index, all
    integer indices in the tuple are treated as scalar integer arrays and are
    also broadcast. In general, an :any:`Integer` index semantically behaves
    the same as a scalar (`shape=()`) `IntegerArray`.

    A list of integers may also be used in place of an integer array. Note
    that NumPy treats a direct list of integers as a tuple index, but this
    behavior is deprecated and will be replaced with integer array indexing in
    the future. ndindex always treats lists as arrays.

    >>> from ndindex import IntegerArray
    >>> import numpy as np
    >>> idx = IntegerArray([[0, 1], [1, 2]])
    >>> a = np.arange(10)
    >>> a[idx.raw]
    array([[0, 1],
           [1, 2]])

    .. note::

       `IntegerArray` does *not* represent an array, but rather an *array
       index*. It does not have most methods that `numpy.ndarray` has, and
       should not be used in array contexts. See the document on
       :ref:`type-confusion` for more details.

    """
    dtype = intp
    """
    The dtype of `IntegerArray` is `np.intp`, which is typically either
    `np.int32` or `np.int64` depending on the platform.
    """

    def reduce(self, shape=None, axis=0):
        """
        Reduce an `IntegerArray` index on an array of shape `shape`.

        The result will either be `IndexError` if the index is invalid for the
        given shape, an `IntegerArray` index where the values are all
        nonnegative, or, if `self` is a scalar array index (`self.shape ==
        ()`), an `Integer` whose value is nonnegative.

        >>> from ndindex import IntegerArray
        >>> idx = IntegerArray([-5, 2])
        >>> idx.reduce((3,))
        Traceback (most recent call last):
        ...
        IndexError: index -5 is out of bounds for axis 0 with size 3
        >>> idx.reduce((9,))
        IntegerArray([4, 2])

        See Also
        ========

        .NDIndex.reduce
        .Tuple.reduce
        .Slice.reduce
        .ellipsis.reduce
        .Newaxis.reduce
        .Integer.reduce
        .BooleanArray.reduce

        """
        from .integer import Integer

        if self.shape == ():
            return Integer(self.array).reduce(shape, axis=axis)

        if shape is None:
            return self

        shape = asshape(shape, axis=axis)

        size = shape[axis]
        new_array = self.array.copy()
        out_of_bounds = (new_array >= size) | ((-size > new_array) & (new_array < 0))
        if out_of_bounds.any():
            raise IndexError(f"index {new_array[out_of_bounds].flat[0]} is out of bounds for axis {axis} with size {size}")

        new_array[new_array < 0] += size
        return IntegerArray(new_array)

    def newshape(self, shape):
        # The docstring for this method is on the NDIndex base class
        shape = asshape(shape)

        # reduce will raise IndexError if it should be raised
        self.reduce(shape)
        return self.shape + shape[1:]

    def isempty(self, shape=None):
        if shape is not None:
            return 0 in self.newshape(shape)

        return 0 in self.shape