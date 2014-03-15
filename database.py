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
Common database functions and models for permtools.
"""

import contextlib

import sqlalchemy

with open('dbpasswd', 'r') as dbpasswd:
    engine = sqlalchemy.create_engine(dbpasswd.read())

metadata = sqlalchemy.MetaData()


# Table joining Permission and Role in a many-to-many relationship.
role_permission = sqlalchemy.Table(
    'auth_officer',
    metadata,
    sqlalchemy.Column(
        'officerid',
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey('officer.officerid')
    ),
    sqlalchemy.Column(
        'lookupid',
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey('l_action.typeid')
    )
)

permission = sqlalchemy.Table(
    'l_action',
    metadata,
    sqlalchemy.Column(
        'typeid', sqlalchemy.Integer, primary_key=True, nullable=False
    ),
    sqlalchemy.Column(
        'descr', sqlalchemy.String(255), nullable=False
    ),
    sqlalchemy.Column(
        'phpconstant', sqlalchemy.String(100), nullable=False
    )
)

role = sqlalchemy.Table(
    'officer',
    metadata,
    sqlalchemy.Column(
        'officerid', sqlalchemy.Integer, primary_key=True, nullable=False
    ),
    sqlalchemy.Column(
        'officer_name', sqlalchemy.String(255), nullable=False
    ),
    sqlalchemy.Column(
        'officer_alias', sqlalchemy.String(255)
    ),
    sqlalchemy.Column(
        'teamid', sqlalchemy.Integer
    ),
    sqlalchemy.Column(
        'ordering', sqlalchemy.SmallInteger
    ),
    sqlalchemy.Column(
        'descr', sqlalchemy.String(255)
    ),
    sqlalchemy.Column(
        'status', sqlalchemy.CHAR(1)
    ),
    sqlalchemy.Column(
        'type', sqlalchemy.CHAR(1)
    )
)


def all_roles():
    """Gets all roles from the database.

    This executes one database query.

    Returns:
        A list of all roles in the database.
        The list is ordered by status, then role type, then name, in ascending
        alphabetical order.
        Roles are represented as a tuple of alias, name, description,
        status and role type.
    """
    query = sqlalchemy.sql.select(
        [
            null_to_empty_string(role.c.officer_alias),
            role.c.officer_name,
            null_to_empty_string(role.c.descr),
            role.c.status,
            role.c.type
        ]
    ).order_by(
        role.c.status,
        role.c.type,
        role.c.officer_name
    )
    results = engine.execute(query)
    roles = results.fetchall()
    results.close()
    return roles


def all_permissions():
    """Gets all permissions from the database.

    This executes one database query.

    Returns:
        A list of permissions, ordered by short name.
        Permissions are represented as a tuple of short name and description.
    """
    query = sqlalchemy.sql.select(
        [permission.c.phpconstant, permission.c.descr]
    ).order_by(
        permission.c.phpconstant
    )
    results = engine.execute(query)
    permissions = results.fetchall()
    results.close()
    return permissions


def permissions_for_roles(role_alias_list):
    """Gets the set of permissions granted to the given roles.

    This executes one database query.

    Args:
        role_alias_list: A list of role aliases (for example, station.manager).

    Returns:
        A list of permission names (for example, AUTH_ADDMEMBER).
        This list will be sorted in ascending alphabetical order.
        If a permission is held by more than one of the given roles, it will
        only be returned once.
    """
    query = sqlalchemy.sql.select(
        [permission.c.phpconstant],
        distinct=True
    ).select_from(
        permission.join(role_permission).join(role)
    ).where(
        role.c.officer_alias.in_(role_alias_list)
    ).order_by(
        permission.c.phpconstant
    )
    results = engine.execute(query)
    permissions = [row[permission.c.phpconstant] for row in results]
    results.close()

    return permissions


def grant_permissions(role_alias, permission_short_name_list):
    """Grants the permission to the role with the given alias.

    This will execute one database query.

    Args:
        role_alias: The alias whose corresponding role is to receive the
            permission.
        permission_short_name: The list of short names of the new permissions to
            grant to the role.

    Returns:
        A list of the numeric ID of each permission granted.
    """
    select_query = sqlalchemy.select(
        [
            role.c.officerid,
            permission.c.typeid
        ]
    ).where(
        (role.c.officer_alias == role_alias)
        & permission.c.phpconstant.in_(permission_short_name_list)
        & sqlalchemy.not_(
            sqlalchemy.tuple_(role.c.officerid, permission.c.typeid).in_(
                sqlalchemy.select(
                    [ role_permission.c.officerid, role_permission.c.lookupid ]
                )
            )
        )
    )

    query = role_permission.insert().from_select(
        [role_permission.c.officerid, role_permission.c.lookupid],
        select_query
    ).returning(role_permission.c.lookupid)

    results = engine.execute(query)
    ids = [row[0] for row in results.fetchall()]
    results.close()
    return ids


def null_to_empty_string(column):
    """Converts a column reference to one replacing nulls with empty strings.

    Args:
        column: A column reference.

    Returns:
        A SQLAlchemy construct that can be used in place of the given column,
        that replaces any NULL values with ''.
    """
    null = None  # Stop automatic code checkers from complaining about == None
    return sqlalchemy.sql.case(
        [
            (column == null, ''),
            (column != null, column)
        ]
    )
