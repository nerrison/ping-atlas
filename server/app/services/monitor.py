from datetime import datetime

from sqlalchemy.orm import Session

from app.models.endpoint import Endpoint, EndpointStatus
from app.models.history import History
from app.models.incident import Incident


class Monitor:

    def __init__(self, db: Session):
        self.db = db


    def process_results(self, results):

        for result in results:

            endpoint = (
                self.db.query(Endpoint)
                .filter(
                    Endpoint.id == result.endpoint_id
                )
                .first()
            )

            if endpoint is None:
                continue


            old_status = endpoint.status


            # update endpoint
            endpoint.status = result.status
            endpoint.response_time = result.response_time
            endpoint.last_check = datetime.now()


            # create history
            history = History(
                endpoint_id=endpoint.id,
                latency=result.response_time or 0,
                availability=(
                    1.0
                    if result.status == EndpointStatus.UP
                    else 0.0
                ),
                error=(
                    result.status_code
                    if result.status_code
                    else 0
                ),
                check_time=datetime.now(),
            )

            self.db.add(history)


            # incident handling
            self.handle_incident(
                endpoint,
                old_status,
                result,
            )


        self.db.commit()



    def handle_incident(
        self,
        endpoint,
        old_status,
        result,
    ):

        # endpoint went down
        if (
            result.status == EndpointStatus.DOWN
            and old_status != EndpointStatus.DOWN
        ):

            incident = Incident(
                endpoint_id=endpoint.id,
                occurred_at=datetime.now(),
                occurred_at_status_code=(
                    result.status_code or 0
                ),
                error_message=result.message,
            )

            self.db.add(incident)



        # endpoint recovered
        elif (
            result.status == EndpointStatus.UP
            and old_status == EndpointStatus.DOWN
        ):

            incident = (
                self.db.query(Incident)
                .filter(
                    Incident.endpoint_id == endpoint.id,
                    Incident.ended_at.is_(None)
                )
                .first()
            )

            if incident:
                incident.ended_at = datetime.now()
                incident.ended_at_status_code = result.status_code