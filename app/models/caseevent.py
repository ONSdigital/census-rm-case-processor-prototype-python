from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import TIMESTAMP, String

from .base import Base


class CaseEvent(Base):
    __tablename__ = 'caseevent'

    id = Column(UUID, primary_key=True)
    event_date = Column('eventdate', TIMESTAMP)
    event_description = Column('eventdescription', String)

    uac_qid_link_id = Column(UUID, ForeignKey('uacqidlink.id'))
    uac_qid_link = relationship("UacQidLink", back_populates="events")
