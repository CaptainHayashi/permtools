"""
Common database functions and models for permtools.
"""

import contextlib

import sqlalchemy
import sqlalchemy.ext.declarative

with open('dbpasswd', 'r') as dbpasswd:
    engine = sqlalchemy.create_engine(dbpasswd.read())

Session = sqlalchemy.orm.sessionmaker(bind=engine)
Base = sqlalchemy.ext.declarative.declarative_base()


# Table joining Permission and Role in a many-to-many relationship.
role_permission = sqlalchemy.Table(
    'auth_officer',
    Base.metadata,
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

class Permission(Base):
    """A permission token in the permissions system."""

    __tablename__ = 'l_action'

    id = sqlalchemy.Column(
        'typeid', sqlalchemy.Integer, primary_key=True, nullable=False
    )
    description = sqlalchemy.Column(
        'descr', sqlalchemy.String(255), nullable=False
    )
    short_name = sqlalchemy.Column(
        'phpconstant', sqlalchemy.String(100), nullable=False
    )


class Role(Base):
    """A role in the permissions system."""

    __tablename__ = 'officer'

    id = sqlalchemy.Column(
        'officerid', sqlalchemy.Integer, primary_key=True, nullable=False
    )
    name = sqlalchemy.Column(
        'officer_name', sqlalchemy.String(255), nullable=False
    )
    alias = sqlalchemy.Column(
        'officer_alias', sqlalchemy.String(255)
    )
    team = sqlalchemy.Column(
        'teamid', sqlalchemy.Integer
    )
    ordering = sqlalchemy.Column(
        'ordering', sqlalchemy.SmallInteger
    )
    description = sqlalchemy.Column(
        'descr', sqlalchemy.String(255)
    )
    status = sqlalchemy.Column(
        sqlalchemy.CHAR(1)
    )
    role_type = sqlalchemy.Column(
        'type', sqlalchemy.CHAR(1)
    )

    permissions = sqlalchemy.orm.relationship(
        'Permission',
        secondary=role_permission,
        backref='roles'
    )


@contextlib.contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def get_permissions(session):
    """Gets all permissions from the database.

    Args:
        session: The current database session.

    Returns:
        A list of all Permission objects, ordered by short name.
    """
    return session.query(
        Permission
    ).order_by(
        Permission.short_name
    ).all()


def get_permission_by_short_name(session, short_name):
    """Gets a permission from the database given its short name.

    Args:
        session: The current database session.
        short_name: The short_name whose corresponding Permission is sought.

    Returns:
        A Permission object representing the permission with the given short
        name.
    """
    return session.query(
        Permission
    ).filter(
        Permission.short_name == short_name
    ).one()


def get_role_by_alias(session, alias):
    """Gets a role from the database given its alias.

    Args:
        session: The current database session.
        alias: The alias whose corresponding Role is sought.

    Returns:
        A Role object representing the role with the given alias.
    """
    return session.query(
        Role
    ).options(
        sqlalchemy.orm.subqueryload('permissions')
    ).filter(
        Role.alias == alias
    ).one()


def grant_permission(session, role_alias, permission_short_name):
    """Grants the permission to the role with the given alias.

    Args:
        session: The current database session.
        role_alias: The alias whose corresponding Role is to receive the
            permission.
        permission_short_name: The short name of the permission to grant to the
            Role.

    Returns:
        True if the permission was successfully granted.
    """
    role = get_role_by_alias(session, role_alias)
    permission = get_permission_by_short_name(session, permission_short_name)
    role.permissions.append(permission)
    session.commit()

