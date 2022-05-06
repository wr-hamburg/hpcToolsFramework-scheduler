DB_NAME = "hpc_tools_framework"
"""The name of the database."""

DB_PSQL_INCLUDES = ["pg_commit_ts", "PG_VERSION", "postgresql.auto.conf"]
"""Files which are expected to be in the postgres directory. Used to check if the directory might be broken. Can be extended. These are the once which are at least required."""