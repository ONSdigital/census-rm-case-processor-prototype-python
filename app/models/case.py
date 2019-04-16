from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, Sequence
from sqlalchemy.types import TIMESTAMP, Enum, String

from .base import Base
from .casestate import CaseState


class Case(Base):
    __tablename__ = 'case'

    caserefseq = Sequence('caserefseq', metadata=Base.metadata)

    case_ref = Column('caseref', String(16), caserefseq, server_default=caserefseq.next_value(), primary_key=True)
    case_id = Column(UUID, nullable=False)
    arid = Column('arid', String)
    estab_arid = Column('estabarid', String)
    uprn = Column('uprn', String)
    address_type = Column('addresstype', String)
    estab_type = Column('estabtype', String)
    address_level = Column('addresslevel', String)
    abp_code = Column('abpcode', String)
    organisation_name = Column('organisationname', String)
    address_line_1 = Column('addressline1', String)
    address_line_2 = Column('addressline2', String)
    address_line_3 = Column('addressline3', String)
    town_name = Column('townname', String)
    postcode = Column('postcode', String)
    latitude = Column('latitude', String)
    longitude = Column('longitude', String)
    oa = Column('oa', String)
    lsoa = Column('lsoa', String)
    msoa = Column('msoa', String)
    lad = Column('lad', String)
    rgn = Column('rgn', String)
    htc_willingness = Column('htcwillingness', String)
    htc_digital = Column('htcdigital', String)
    treatment_code = Column('treatmentcode', String)
    collection_exercise_id = Column('collectionexerciseid', String)
    action_plan_id = Column('actionplanid', String)

    state = Column('state', Enum(CaseState))

    uac_qid_links = relationship("UacQidLink")
