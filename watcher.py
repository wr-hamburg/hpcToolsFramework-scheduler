import logging
import os
from database_queries import *
import subprocess
from utils import parse_Popen

# logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(message)s", filename="watcher.log"
)


def schedule_jobs(db: Database):
    """Checks the database for the jobs and takes the apropiate steps to run, update and cels the jobs.

    Args:
        db (Database): The database.
    """
    programs = db.query("SELECT * FROM programs;").fetchall()
    programs = [dict(**program) for program in programs]
    for program in programs:
        running_jobs = db.query(
            f"SELECT * FROM jobs WHERE program_id = '{program['id']}' AND status = 'Running';"
        ).fetchall()
        if running_jobs:
            # do not start new jobs for programs which already have running jobs
            continue

        # select next pending job
        next_queued_job = db.query(
            f"SELECT * FROM jobs WHERE program_id = '{program['id']}' AND status = 'Pending'"
        ).fetchone()
        if next_queued_job:
            next_queued_job = dict(**next_queued_job)
            # clean program
            os.system(f"make clean -C ../../{program['directory']}")  
            # compile program
            makefile_name = next_queued_job["makefile_path"].split("/")[-1]
            os.system(f"make -C ../../{program['directory']} -f {makefile_name}")
            # schedule job
            os.system(
                f'sbatch ../../{next_queued_job["jobscript_path"]}'
            )
            # update state of scheduled job
            db.query(
                f"UPDATE jobs SET status = 'Running' WHERE id='{next_queued_job['id']}'"
            )
            logging.info(
                f"Started Job {next_queued_job['timestamp_id']} for program {program['name']}."
            )


def end_job(
    program_dir: str,
    db_job_id: int,
    status: str,
    slurm_job_id: int = None,
    scancel: bool = False,
):
    """Cancels a specific jobs by removing the compiled binary and updateing the status in the database.

    Args:
        db (Database): The Database.
        program_dir (str): The directory of the program.
        db_job_id (str): The id of the job in the database.
        status (str): The new status to set. Either the job was canceled or has finished.
        slurm_job_id (int): The SLURM id of the job.
        scancel (bool, optional): Boolean wether to canncel the job in SLURM. may be used when canceling a stuck job. Defaults to False.
    """

    if scancel:
        os.system(f"scancel {slurm_job_id}")

    # TODO check name of status
    db.query(f"UPDATE jobs SET status='{status}' WHERE id='{db_job_id}")
    os.system(f"make clean -C ../../{program_dir}")
    logging.info(f"Ended job with db job id {db_job_id}.")
    # TODO download output if possible


def check_slurm(db: Database):
    squeue_output = (
        subprocess.Popen(
            ["squeue", "-h", '--format=" %A | %T | %j"'], stdout=subprocess.PIPE
        )
        .communicate()[0]
        .decode("utf-8")
    )
    squeue_output = parse_Popen(squeue_output)

    for line in squeue_output:
        slurm_info = line.split("|")
        job_id = slurm_info[0]
        job_status = slurm_info[1]
        job_name = slurm_info[2]

        print(job_id, job_status, job_name)
        timestamp = job_name[job_name.rfind(".") :]

        # TODO will fail because database is not initilized
        program_job_join = db.query(
            f"SELECT * from jobs JOIN programs ON jobs.program_id = programs.id WHERE jobs.timestamp_id = '{timestamp}';"
        )

        # TODO maybe extend https://slurm.schedmd.com/squeue.html#SECTION_JOB-STATE-CODES
        if job_status in [
            "FAILED",
            "BOOT_FAIL",
            "CANCELLED",
            "NODE_FAIL",
            "OUT_OF_MEMORY",
            "SUSPENDED",
        ]:
            end_job(
                program_job_join["programs.directory"],
                program_job_join["jobs.id"],
                "Error",
                job_id,
                True,
            )
        elif job_status == "TIMEOUT":
            end_job(
                program_job_join["programs.directory"],
                program_job_join["jobs.id"],
                "Timeout",
                job_id,
                True,
            )
        elif job_status in [
            "RUNNING",
            "REQUEUE_FED",
            "REQUEUE_HOLD",
            "REQUEUED",
            "RESIZING",
            "STAGE_OUT",
        ]:
            output = query_job(job_id)


if __name__ == "__main__":
    with Database() as db:
        check_slurm(db)
        schedule_jobs(db)
