from database import Database
from datetime import datetime, timezone
from decorators import log_error


@log_error
def insert_job(
    timestamp_id: str,
    makefile_path: str,
    jobscript_path: str,
    status: str,
    program_id: int,
    queue_time: str = None,
    start_time: str = None,
    finish_time: str = None,
):
    """Insert a job into the database.

    Parameters
    ----------
    timestamp_id : str
        The timestamp identifier of the job.
    makefile_path : str
        The path to the makefile.
    jobscript_path : str
        The path to the jobscript.
    status : str
        The status of the job.
    program_id : int
        The program identifier.
    queue_time : str, optional
        The queue time, by default None
    start_time : str, optional
        The start time of the job, by default None
    finish_time : str, optional
        The finish time of the job, by default None
    """
    query = f"INSERT INTO jobs (timestamp_id, makefile_path, jobscript_path, status, program_id, queue_time, start_time, finish_time) VALUES ('{timestamp_id}','{makefile_path}','{jobscript_path}','{status}','{program_id}',NULL,NULL,NULL) RETURNING id"
    with Database() as db:
        result = db.query(query).fetchone()
        print(result["id"], end="\n")


@log_error
def insert_program(name: str, makefile_path: str, program_path: str, directory: str):
    """Inserts a program in the program table.

    Args:
        name (str): Name of the program.
        makefile_path (str): Path to the makefile.
        program_path (str): Path to the program.
        directory (str): Directory of the program.
    """

    query = f"INSERT INTO programs (name, makefile_path, program_path, directory) VALUES ('{name}', '{makefile_path}', '{program_path}', '{directory}') RETURNING id"
    with Database() as db:
        result = db.query(query).fetchone()
        print(result["id"], end="\n")


@log_error
def query_programs():
    """Select all programs."""
    query = f"SELECT * FROM programs;"
    with Database() as db:
        programs = db.query(query).fetchall()
        print([dict(**program) for program in programs], end="\n")


@log_error
def query_jobs_by_status(status: str):
    """Get all jobs with a specified status.

    Args:
        status (str): Status the program should have.
    """
    query = f"SELECT * FROM jobs WHERE status = '{status}';"
    with Database() as db:
        jobs = db.query(query).fetchall()
        print([dict(**job) for job in jobs], end="\n")


@log_error
def query_jobs_by_tool(toolname: str):
    """Query all jobs using a certain tool.

    Args:
        toolname (str): Name of the tool to be used.
    """
    query = f"SELECT * FROM jobs JOIN programs ON jobs.program_id = programs.id WHERE programs.toolname = '{toolname}';"
    with Database() as db:
        jobs = db.query(query).fetchall()
        print([dict(**job) for job in jobs], end="\n")


@log_error
def query_program_by_name(program_name: str):
    """Checks if a program is already existing in the program table.

    Args:
        program_name (str): Name of the program to check.
    """
    query = f"SELECT * FROM programs WHERE programs.name = '{program_name}';"
    with Database() as db:
        program = db.query(query).fetchone()
        if program:
            print(dict(**program), end="\n")
        else:
            print("", end="\n")


@log_error
def query_job_and_program_by_timestamp(timestamp: str):
    """Gets a join of a job and a program by timestamp.

    Args:
        timestamp (str): The timestamp to search for.
    """
    query = f"SELECT * from 'jobs' JOIN programs ON jobs.program_id = programs.id WHERE jobs.timestamp_id = '{timestamp}';"
    with Database() as db:
        jobs = db.query(query).fetchall()
        print([dict(**job) for job in jobs], end="\n")


@log_error
def query_job(job_id: str):
    query = f"SELECT * from 'jobs' WHERE slurm_job_id = {job_id};"
    with Database() as db:
        jobs = db.query(query).fetchall()
        print([dict(**job) for job in jobs], end="\n")
