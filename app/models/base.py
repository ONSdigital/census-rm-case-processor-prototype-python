from sqlalchemy.schema import MetaData
from sqlalchemy.ext.declarative import declarative_base

metadata = MetaData(schema='casesvcv2python')

Base = declarative_base(metadata=metadata)
