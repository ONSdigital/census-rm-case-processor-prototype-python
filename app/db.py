import functools
import logging
from contextlib import contextmanager

import backoff
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from structlog import wrap_logger

from . import settings

logger = wrap_logger(logging.getLogger(__name__))

Session = sessionmaker()


def create_database(db_connection, run_alembic=True, **engine_kwargs):
    from app import models

    engine = create_engine(
        db_connection,
        **engine_kwargs)
    Session.configure(bind=engine)

    logger.info("Creating database")

    if run_alembic:
        alembic_cfg = Config("alembic.ini")
        alembic_cfg.attributes['configure_logger'] = False

        logger.info("Running Alembic database upgrade")
        command.upgrade(alembic_cfg, "head")
    else:
        logger.info("Creating database tables.")
        models.Base.metadata.create_all(engine)

    logger.info("Ok, database tables have been created.")


@backoff.on_exception(
    backoff.expo, OperationalError, max_value=16, max_tries=10)
def initialise_db():
    return create_database(
        settings.DATABASE_URI,
        pool_size=settings.DB_POOL_SIZE,
        max_overflow=settings.DB_MAX_OVERFLOW,
        pool_recycle=settings.DB_POOL_RECYCLE)


@contextmanager
def transaction():
    session = Session()

    try:
        yield session
        session.commit()
    except:
        logger.info('Rolling back DB transaction')

        session.rollback()
        raise
    finally:
        session.close()
