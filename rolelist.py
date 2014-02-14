#!/usr/bin/env python3

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
