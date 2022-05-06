from constants import DB_NAME, DB_PSQL_INCLUDES
from utils import run_command
import logging
import time


def health_check():
    all_healthy = True

    try:
        run_command('[ -d "./../database" ] && echo "exists"')
        database_dir_includes = run_command(f"ls ./../database")
        for file in DB_PSQL_INCLUDES:
            if database_dir_includes.find(file) == -1:
                print("The database directory does not contain all files needed.")
                all_healthy = False
                break
    except:
        print("No database directory found.")
        all_healthy = False
    return all_healthy


def force_delete_database():
    db_backup_name = None
    try:
        db_backup_name = f"backup{DB_NAME}_db_{time.time()}.sql"
        run_command(f"pg_dump -d {DB_NAME} > ../{db_backup_name} ")
        print(f"Created backup with name {db_backup_name}")
    except:
        print(f"Can not create backup database.")
    try:
        run_command("killall postgres")
    except:
        print("No postgres processes found to kill")
    try:
        run_command(f"rm -rf .\\..\\database")
    except:
        print("No dir to delete")

    tmp_db_name = time.time()
    try:
        run_command(f"createdb {tmp_db_name}")
        run_command(f"psql {tmp_db_name}")
        run_command(f"DROP DATABASE [IF EXISTS] {DB_NAME}")
        run_command("\q")
    except:
        print("Could not create temporary database to delete")

    return tmp_db_name


def init_database():
    print("Init.", end="\n")
    try:
        # check if database already exists else create it
        output = run_command(f"psql -l | grep {DB_NAME} | wc -l")
        if output == "0":
            print("Create database server.", end="\n")
            # create postgres database
            run_command("initdb -D ./../database")
            # TODO sometimes this does not work
            run_command("pg_ctl start -D ./../database -l logfile")
            print("Start database server.", end="\n")
            run_command(f"createdb {DB_NAME}")
            print(f"Create database {DB_NAME}.", end="\n")
            # create tables from sql file
            run_command(f"psql -f schema.sql -d {DB_NAME}")
            print(f"Import schema.", end="\n")

    except Exception as e:
        logging.critical(e, exc_info=True)
        print(f"ERROR: {e}", end="\n")
