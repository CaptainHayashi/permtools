#!/usr/bin/env python3

"""
Lists all permissions available in the system.

Each is listed, one per line, in alphabetical short-name order, in the format
'SHORT_NAME:Long Name'.

Usage: permlist.py
"""

import database

if __name__ == '__main__':
    with database.session_scope() as session:
        permissions = (
            session
                .query(database.Permission)
                .order_by(database.Permission.short_name)
        )

    for permission in permissions:
        print(permission.short_name, permission.description, sep=':')
