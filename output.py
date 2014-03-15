# Copyright (C) 2014 University Radio York
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Output formatting utilities for permtools.
"""

RECORD_SEPARATOR = '\n'
FIELD_SEPARATOR = ':'


def record_join(records):
    """Joins a list of record strings with the record separator.

    This does not format the records themselves: see field_join().

    Args:
        records: A list of strings representing records.

    Returns:
        The string that is the joining of the given record strings with
        the record separator.
    """
    return RECORD_SEPARATOR.join(records)


def field_join(record):
    """Joins a record tuple together with the field separator.

    Each part of the record is converted to a string.

    Args:
        record: A tuple representing a record to output.

    Returns:
        The string that is the joining of the string representation of each item
        in the record with the field separator.
    """
    return FIELD_SEPARATOR.join(str(field) for field in record)


def record_field_format(data):
    """Outputs a list of record tuples in a delimiter-separated value format.

    See field_join() and record_join(), which this function uses.

    Args:
        data: A list of tuples to format for output.

    Returns:
        A string where each record is separated by a newline and each field in
        the record is converted to a string and separated by the field
        separator.
    """
    return record_join(field_join(record) for record in data)
