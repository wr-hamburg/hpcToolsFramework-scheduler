from database import Database
from datetime import datetime
import sys


def update_status(timestamp_id: str, status: str):
    """Update the status of a job.

    Parameters
    ----------
    timestamp_id : str
        The timestamp identifier of the job.
    status : str
        The status to be set.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with Database() as db:
        # update job status
        query_1 = (
            f"UPDATE jobs SET status='{status}' WHERE timestamp_id='{timestamp_id}'"
        )
        db.query(query_1)

        # update times
        if status == "Running":
            query_2 = f"UPDATE jobs SET start_time='{timestamp}' WHERE timestamp_id='{timestamp_id}'"
            db.query(query_2)
        elif status == "Finished":
            query_2 = f"UPDATE jobs SET finish_time='{timestamp}' WHERE timestamp_id='{timestamp_id}'"
            db.query(query_2)


if __name__ == "__main__":
    timestamp_id = sys.argv[1]
    status = sys.argv[2]
    update_status(timestamp_id, status)