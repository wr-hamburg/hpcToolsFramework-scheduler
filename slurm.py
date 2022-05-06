from utils import parse_Popen
import subprocess


def query_slurm(job_id_to_find: str):
    """Finds runtime and start time of a slurm job by its job id.

    Args:
        job_id_to_find (str): Id of the slurm job.

    Returns:
        Tuple(): Return the runtime of the job followed by the initial start time. For example:  Tuple("1:14:29", "2022-03-19T13:54:56")
    """
    output = (
        subprocess.Popen(
            ["squeue", "-h", '--format="%A | %M | %V"'], stdout=subprocess.PIPE
        )
        .communicate()[0]
        .decode("utf-8")
    )
    parsed_output = parse_Popen(output)

    for e in parsed_output:
        slurm_info = e.split("|")
        job_id = slurm_info[0]
        if str(job_id.strip()) == str(job_id_to_find):
            return (slurm_info[1], slurm_info[2])