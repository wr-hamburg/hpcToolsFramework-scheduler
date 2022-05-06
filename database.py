import logging
import psycopg2  # https://www.psycopg.org/docs/
import psycopg2.extras
from constants import DB_NAME
from utils import run_command


class Database:
    def __init__(self, dbname=DB_NAME, host="localhost"):
        """Initiates database.

        Args:
            dbname (str, optional): Name of the database. Defaults to "hpc_tools_framework".
            host (str, optional): Name of the database server host. Defaults to "localhost".
        """
        self.dbname = dbname
        self.user = run_command("whoami")
        self.host = host

    def connect(self):
        """Connect the current instance to the database.
        """
        self.connection = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            host=self.host,
            cursor_factory=psycopg2.extras.RealDictCursor,
        )
        logging.info("Connected to database.")

    def disconnect(self):
        """Diconnect the current instance from the database. 
        """
        if self.connection:
            self.connection.close()
            logging.info("Connection to database closed.")

    def __enter__(self):
        """Inplace connection to the database.

        Returns:
            Instance: To the database connected instance. 
        """
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        #TODO
        """Inplace exit of the database.

        Args:
            exc_type (_type_): _description_ 
            exc_value (_type_): _description_
            exc_tb (_type_): _description_
        """
        self.disconnect()

    def query(self, query: str):
        """Perform query on the database.

        Args:
            query (str): The query to execute on the database. 

        Returns:
           Cursor: The curser on the database / the query result. 
        """
        cur = self.connection.cursor()
        cur.execute(query)
        self.connection.commit()
        return cur
