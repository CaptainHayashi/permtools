#!/usr/bin/env python3

"""
Lists all permissions assigned to the role with the given alias.

Each is listed, one per line, in ascending alphabetical order, in the
format 'SHORT_NAME'.

Usage: roleperms.py ALIAS
"""

import sys
import database

if __name__ == '__main__':
    with database.session_scope() as session:
        role = database.get_role_by_alias(session, sys.argv[1])
        for permission in role.permissions:
            print(permission.short_name)
