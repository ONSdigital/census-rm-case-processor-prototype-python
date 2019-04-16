import json
from unittest import mock

from app import settings
from app.message_processor import MessageProcessor
from app.models import Case, CaseEvent, UacQidLink

dummy_collex_id = "n66de4dc-3c3b-11e9-b210-d663bd873d93"
sample_data = {
    "type": "CreateCaseSample",
    "arid": "XXXXX",
    "estabArid": "foo",
    "uprn": "XXXXXXXXXXXXX",
    "addressType": "CE",
    "estabType": "XXX",
    "addressLevel": "foo",
    "abpCode": "foo",
    "organisationName": "foo",
    "addressLine1": "1 main street",
    "addressLine2": "upper upperingham",
    "addressLine3": "",
    "townName": "upton",
    "postcode": "UP103UP",
    "latitude": "50.863849",
    "longitude": "-1.229710",
    "oa": "foo",
    "lsoa": "foo",
    "msoa": "foo",
    "lad": "foo",
    "rgn": "E999",
    "htcWillingness": "foo",
    "htcDigital": "foo",
    "treatmentCode": "foo",
    "collectionExerciseId": dummy_collex_id,
    "actionPlanId": "foo"
}


def test_process_case_create(db_session):
    m_inbound_channel = mock.Mock()
    m_outbound_channel = mock.Mock()
    processor = MessageProcessor(m_inbound_channel, m_outbound_channel)

    processor(m_inbound_channel, mock.Mock(), None, json.dumps(sample_data))

    case = (
        db_session.query(Case)
            .filter(Case.collection_exercise_id==dummy_collex_id)
            .first()
    )

    # check that rows have been added to the database
    assert case
    assert len(case.uac_qid_links) == 1
    assert len(case.uac_qid_links[0].events) == 1

    # check that a valid JSON object was emitted
    _, args, body = m_outbound_channel.method_calls[0]
    exchange, routing_key = args

    assert exchange == settings.RABBIT_CASE_EVENT_EXCHANGE
    assert routing_key == 'event.case.update'
    assert isinstance(body, dict)
