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
