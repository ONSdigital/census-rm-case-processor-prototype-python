import pytest
import mock
from contextlib import contextmanager

from sqlalchemy import create_engine

from app import db, settings


@pytest.fixture(scope='session', autouse=True)
def setup_db():
    db.create_database(settings.DATABASE_URI, run_alembic=False)


@pytest.fixture(scope='function')
def db_session():
    """Sets up the DB engine using the local postgres instance

    Hijacks the transaction decorator to control the transaction as
    part of the test
    """
    session = db.Session()

    @contextmanager
    def _dummy_transaction():
        yield session

    with mock.patch('app.db.transaction', _dummy_transaction):
        try:
            yield session
        finally:
            session.rollback()
            session.close()
