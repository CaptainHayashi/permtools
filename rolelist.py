#!/usr/bin/env python3

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
Lists all roles available in the system.

Each is listed, one per line, in alphabetical status-type-name order, in the
format 'alias:name:description:status:type'.

Usage: rolelist.py
"""

import database

if __name__ == '__main__':
    with database.session_scope() as session:
        roles = (
            session
                .query(database.Role)
                .order_by(
                    database.Role.status,
                    database.Role.role_type,
                    database.Role.name
                )
        )

    for role in roles:
        print(
            role.alias,
            role.name,
            role.description,
            role.status,
            role.role_type,
            sep=':'
        )
