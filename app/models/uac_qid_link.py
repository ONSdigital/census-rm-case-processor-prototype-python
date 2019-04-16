from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, ForeignKey, Sequence
from sqlalchemy.types import TIMESTAMP, BigInteger, Integer, String

from .base import Base


class UacQidLink(Base):
    __tablename__ = 'uacqidlink'

    uacqidlinkseq = Sequence('uacqidlinkseq', metadata=Base.metadata)

    id = Column(UUID, primary_key=True)
    unique_number = Column('uacqidlinkseq', Integer, server_default=uacqidlinkseq.next_value())
    qid = Column('qid', BigInteger)
    uac = Column('uac', String)

    caseref = Column(String(16), ForeignKey('case.caseref'))
    case = relationship("Case", back_populates="uac_qid_links")

    events = relationship("CaseEvent")
