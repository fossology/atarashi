# cython: language_level=3

"""
Copyright 2022 Sushant Kumar (sushantmishra02102002@gmail.com)

SPDX-License-Identifier: GPL-2.0

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
version 2 as published by the Free Software Foundation.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

from libc.stdlib cimport calloc, free


cdef Py_ssize_t TWO = 0
cdef Py_ssize_t ONE = 1
cdef Py_ssize_t ROW = 2


cpdef unsigned long damerau_levenshtein_distance(seq1, seq2):
    """
        Return the edit distance. This implementation is based on Michael Homer's implementation
        (https://web.archive.org/web/20150909134357/http://mwh.geek.nz:80/2009/04/26/python-damerau-levenshtein-distance/)
        and runs in O(N*M) time using O(M) space. This code implements the "optimal string alignment distance"
        algorithm, as described in Wikipedia here:
        https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance#Optimal_string_alignment_distance
        Note that `seq1` and `seq2` can be any sequence type. This not only includes `str` but also includes `list`,
        `tuple`, `range`, and more.
        Examples:
        >>> damerau_levenshtein_distance('smtih', 'smith')
        1
        >>> damerau_levenshtein_distance('saturday', 'sunday')
        3
        >>> damerau_levenshtein_distance('orange', 'pumpkin')
        7
        >>> damerau_levenshtein_distance([1, 2, 3, 4, 5, 6], [7, 8, 9, 7, 10, 11, 4])
        7
    """

    cdef Py_ssize_t first_difference = 0
    while first_difference < len(seq1) and \
          first_difference < len(seq2) and \
          seq1[first_difference] == seq2[first_difference]:
        first_difference += 1

    seq1 = seq1[first_difference:]
    seq2 = seq2[first_difference:]

    if seq1 is None:
        return len(seq2)
    if seq2 is None:
        return len(seq1)

    if len(seq2) < len(seq1):
        seq1, seq2 = seq2, seq1

    cdef Py_ssize_t i, j
    cdef Py_ssize_t offset = len(seq2) + 1
    cdef unsigned long delete_cost, add_cost, subtract_cost, edit_distance

    cdef unsigned long * storage = <unsigned long * >calloc(3 * offset, sizeof(unsigned long))
    if not storage:
        raise MemoryError()

    try:
        for i in range(1, offset):
            storage[ROW * offset + (i - 1)] = i

        for i in range(len(seq1)):
            for j in range(offset):
                storage[TWO * offset + j] = storage[ONE * offset + j]
                storage[ONE * offset + j] = storage[ROW * offset + j]
            for j in range(len(seq2)):
                storage[ROW * offset + j] = 0
            storage[ROW * offset + len(seq2)] = i + 1

            for j in range(len(seq2)):
                delete_cost = storage[ONE * offset + j] + 1
                add_cost = storage[ROW * offset + (j - 1 if j > 0 else len(seq2))] + 1
                subtract_cost = storage[ONE * offset + (j - 1 if j > 0 else len(seq2))] + (seq1[i] != seq2[j])
                storage[ROW * offset + j] = min(delete_cost, add_cost, subtract_cost)
                
                if i > 0 and j > 0 and seq1[i] == seq2[j - 1] and seq1[i - 1] == seq2[j] and seq1[i] != seq2[j]:
                    storage[ROW * offset + j] = min(storage[ROW * offset + j],
                                                         storage[TWO * offset + j - 2 if j > 1 else len(seq2)] + 1)

        return storage[ROW * offset + (len(seq2) - 1)]
    finally:
        free(storage)
