import datetime
import logging
import uuid

from jsonpointer import resolve_pointer
from structlog import wrap_logger

from app import models

from .base import BaseReceiver

logger = wrap_logger(logging.getLogger(__name__))


class CreateCaseReceiver(BaseReceiver):
    event_type = 'CreateCaseSample'

    def process_event(self, message):
        logger.info(f'Processing message: {message}')

        case = self.create_case(message)
        self.message_processor.session.add(case)

        uac_qid_link = self.create_uac_qid_link(case)
        self.message_processor.session.add(uac_qid_link)

        case_event = self.create_case_event(case, uac_qid_link)
        self.message_processor.session.add(case_event)

        # TODO: real values
        case_event = self.create_common_event('CaseCreated', case_event.event_date, {
            "collectionCase" : {
                "id": case.case_id,
                "caseRef": case.case_ref,
                "survey": "Census",
                "collectionExerciseId": case.collection_exercise_id,
                "sampleUnitRef": "",
                "address": {
                    "address_line1": case.address_line_1,
                    "address_line2": case.address_line_2,
                    "address_line3": case.address_line_3,
                    "town_name": case.town_name,
                    "postcode": case.postcode,
                    "region": "E", # TODO
                    "latitude": case.latitude,
                    "longitude": case.longitude,
                    "uprn": case.uprn,
                    "arid": case.arid,
                    "address_type": case.address_type,
                    "estab_type": case.estab_type
                },
                "state": models.CaseState.ACTIONABLE.value,
                "actionable_from":"2011-08-12T20:17:46.384Z" # TODO
            }
        })
        self.message_processor.emit_case_event('event.case.update', case_event)


    def create_case(self, create_case_sample):
        # create case with test values
        return models.Case(
            case_id=str(uuid.uuid4()),
            arid=create_case_sample['arid'],
            estab_arid=create_case_sample['estabArid'],
            uprn=create_case_sample['uprn'],
            address_type=create_case_sample['addressType'],
            estab_type=create_case_sample['estabType'],
            address_level=create_case_sample['addressLevel'],
            abp_code=create_case_sample['abpCode'],
            organisation_name=create_case_sample['organisationName'],
            address_line_1=create_case_sample['addressLine1'],
            address_line_2=create_case_sample['addressLine2'],
            address_line_3=create_case_sample['addressLine3'],
            town_name=create_case_sample['townName'],
            postcode=create_case_sample['postcode'],
            latitude=create_case_sample['latitude'],
            longitude=create_case_sample['longitude'],
            oa=create_case_sample['oa'],
            lsoa=create_case_sample['lsoa'],
            msoa=create_case_sample['msoa'],
            lad=create_case_sample['lad'],
            rgn=create_case_sample['rgn'],
            htc_willingness=create_case_sample['htcWillingness'],
            htc_digital=create_case_sample['htcDigital'],
            treatment_code=create_case_sample['treatmentCode'],
            collection_exercise_id=create_case_sample['collectionExerciseId'],
            action_plan_id=create_case_sample['actionPlanId'])


    def create_uac_qid_link(self, created_case):
        return models.UacQidLink(
            id=str(uuid.uuid4()),
            uac='Get UAC...',
            qid='99999', # get QID,
            case=created_case
        )


    def create_case_event(self, created_case, uac_qid_link):
        return models.CaseEvent(
            id=str(uuid.uuid4()),
            event_date=datetime.datetime.utcnow(),
            event_description='Case created',
            uac_qid_link=uac_qid_link
        )

    def create_common_event(self, event_type, event_date, payload):
        event = {
            'type': event_type,
            'source': 'CaseService',
            'channel': 'TODO',
            'dateTime': F'{event_date.isoformat()}Z',
            'transactionId': 'TODO'
        }

        return {
            'event': event,
            'payload': payload
        }
