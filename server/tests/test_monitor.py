from datetime import datetime
import uuid

from app.services.monitor import Monitor
from app.models.endpoint import (
    Endpoint,
    EndpointStatus,
    EndpointType,
    HttpMethod,
)
from app.models.group import Group
from app.models.incident import Incident
from app.scanner.result import ScanResult


def create_endpoint(db):
    group = Group(
        id=uuid.uuid4(),
        name="Test Group",
        slug="test-group",
        type="customer",
        description="test",
    )

    db.add(group)
    db.commit()

    endpoint = Endpoint(
        id=uuid.uuid4(),
        group_id=group.id,
        name="Test Endpoint",
        type=EndpointType.HTTPS,
        url="example.com",
        method=HttpMethod.GET,
        status=EndpointStatus.UNKNOWN,
    )

    db.add(endpoint)
    db.commit()
    db.refresh(endpoint)

    return endpoint


def test_monitor_updates_endpoint_and_creates_history(db):
    endpoint = create_endpoint(db)

    result = ScanResult(
        endpoint_id=endpoint.id,
        status=EndpointStatus.UP,
        status_code=200,
        response_time=120,
        message=None,
    )

    monitor = Monitor(db)

    monitor.process_results([result])

    db.refresh(endpoint)

    assert endpoint.status == EndpointStatus.UP
    assert endpoint.response_time == 120
    assert endpoint.last_check is not None

    assert len(endpoint.histories) == 1

    history = endpoint.histories[0]

    assert history.endpoint_id == endpoint.id
    assert history.latency == 120
    assert history.availability == 1.0
    assert history.error == 200


def test_monitor_creates_incident_when_endpoint_goes_down(db):
    endpoint = create_endpoint(db)

    endpoint.status = EndpointStatus.UP
    db.commit()

    result = ScanResult(
        endpoint_id=endpoint.id,
        status=EndpointStatus.DOWN,
        status_code=500,
        response_time=None,
        message="Server down",
    )

    monitor = Monitor(db)

    monitor.process_results([result])

    db.refresh(endpoint)

    assert endpoint.status == EndpointStatus.DOWN

    assert len(endpoint.incidents) == 1

    incident = endpoint.incidents[0]

    assert incident.occurred_at is not None
    assert incident.ended_at is None
    assert incident.occurred_at_status_code == 500
    assert incident.error_message == "Server down"


def test_monitor_closes_existing_incident_on_recovery(db):
    endpoint = create_endpoint(db)

    endpoint.status = EndpointStatus.DOWN
    db.commit()

    incident = Incident(
        endpoint_id=endpoint.id,
        occurred_at=datetime.now(),
        occurred_at_status_code=500,
        error_message="Timeout",
    )

    db.add(incident)
    db.commit()
    db.refresh(incident)

    result = ScanResult(
        endpoint_id=endpoint.id,
        status=EndpointStatus.UP,
        status_code=200,
        response_time=100,
        message=None,
    )

    monitor = Monitor(db)

    monitor.process_results([result])

    db.refresh(incident)

    assert endpoint.status == EndpointStatus.UP
    assert incident.ended_at is not None
    assert incident.ended_at_status_code == 200